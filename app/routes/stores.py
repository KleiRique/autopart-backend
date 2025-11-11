from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app import models
from app.schemas import StoreCreate, StoreOut

router = APIRouter()

@router.post("", response_model=StoreOut)
async def create_store(payload: StoreCreate, db: AsyncSession = Depends(get_session)):
    store = models.Store(owner_id=1, name=payload.name, whatsapp_number=payload.whatsapp_number, base_url=payload.base_url)
    db.add(store); await db.commit(); await db.refresh(store)
    return store

@router.get("/{user_id}", response_model=list[StoreOut])
async def get_stores(user_id: int, db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(models.Store).where(models.Store.owner_id == user_id))).scalars().all()
    return rows

@router.put("/{store_id}", response_model=StoreOut)
async def update_store(store_id: int, payload: StoreCreate, db: AsyncSession = Depends(get_session)):
    store = await db.get(models.Store, store_id)
    if not store: raise HTTPException(404, "Loja não encontrada")
    store.name = payload.name; store.whatsapp_number = payload.whatsapp_number; store.base_url = payload.base_url
    await db.commit(); await db.refresh(store); return store

@router.delete("/{store_id}")
async def delete_store(store_id: int, db: AsyncSession = Depends(get_session)):
    store = await db.get(models.Store, store_id)
    if not store: raise HTTPException(404, "Loja não encontrada")
    await db.delete(store); await db.commit(); return {"ok": True}
