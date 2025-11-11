from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app import models
from app.schemas import ConversationCreate, MessageIn, MessageOut, QuoteOut
from app.ai_agent import fanout_request
from app.ws import manager

router = APIRouter()

@router.post("", response_model=dict)
async def create_conversation(payload: ConversationCreate, db: AsyncSession = Depends(get_session)):
    if len(payload.store_ids) != 3:
        raise HTTPException(400, "Exatamente 3 lojas devem ser enviadas para este fluxo")
    conv = models.Conversation(mechanic_id=1, part_query=payload.part_query)
    db.add(conv); await db.commit(); await db.refresh(conv)

    stores = []
    for sid in payload.store_ids:
        s = await db.get(models.Store, sid)
        if not s: raise HTTPException(404, f"Loja {sid} não encontrada")
        stores.append({"id": s.id, "name": s.name, "whatsapp_number": s.whatsapp_number})

    await fanout_request(payload.part_query, conv.id, stores)
    return {"conversation_id": conv.id, "status": "searching"}

@router.post("/{conversation_id}/message", response_model=MessageOut)
async def add_message(conversation_id: int, payload: MessageIn, db: AsyncSession = Depends(get_session)):
    msg = models.Message(conversation_id=conversation_id, role="user", content=payload.content)
    db.add(msg); await db.commit(); await db.refresh(msg)
    await manager.send(str(conversation_id), {"type": "message", "data": {"role": "user", "content": payload.content}})
    return msg

@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def list_messages(conversation_id: int, db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(models.Message).where(models.Message.conversation_id == conversation_id))).scalars().all()
    return rows

@router.get("/{conversation_id}/quotes", response_model=list[QuoteOut])
async def list_quotes(conversation_id: int, db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(models.Quote).where(models.Quote.conversation_id == conversation_id))).scalars().all()
    return rows
