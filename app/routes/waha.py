from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Message
from app.ai_agent import parse_store_reply, decide_best_quote

router = APIRouter(prefix="/waha", tags=["WAHA"])

@router.post("/webhook")
async def waha_webhook(req: Request, db: AsyncSession = Depends(get_session)):
    body = await req.json()
    text = body.get("message", {}).get("text", "")
    from_number = body.get("from", "")
    conv_id = body.get("conversation", {}).get("id")

    if not text or not from_number:
        return {"ignored": True}

    msg = Message(conversation_id=conv_id, role="store", content=text)
    db.add(msg)
    await db.commit()

    reply = await parse_store_reply(text)
    return {"reply": reply}
