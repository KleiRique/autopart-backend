from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app import models
from app.ai_agent import parse_store_reply, decide_best_quote
from app.ws import manager

router = APIRouter()

@router.post("")
async def waha_webhook(req: Request, db: AsyncSession = Depends(get_session)):
    body = await req.json()
    text = body.get("text") or (body.get("message", {}) or {}).get("text")
    from_number = body.get("from") or body.get("sender")
    conv_id = body.get("conv_id")
    if not (text and from_number and conv_id):
        return {"ignored": True}

    msg = models.Message(conversation_id=int(conv_id), role="store", content=text)
    db.add(msg); await db.commit()

    parsed = parse_store_reply(text)
    if parsed:
        store = (await db.execute(select(models.Store).where(models.Store.whatsapp_number == from_number))).scalar_one_or_none()
        if store:
            quote = models.Quote(conversation_id=int(conv_id), store_id=store.id, **parsed)
            db.add(quote); await db.commit(); await db.refresh(quote)
            await manager.send(str(conv_id), {"type": "quote", "data": {"store_id": store.id, **parsed}})

        quotes = (await db.execute(select(models.Quote).where(models.Quote.conversation_id == int(conv_id)))).scalars().all()
        if len(quotes) >= 3:
            best = await decide_best_quote([{"store_id": q.store_id, "price": q.price, "delivery_days": q.delivery_days} for q in quotes])
            if best:
                conv = await db.get(models.Conversation, int(conv_id))
                conv.status = "handoff"; await db.commit()
                await manager.send(str(conv_id), {"type": "decision", "data": best})
    return {"ok": True}
