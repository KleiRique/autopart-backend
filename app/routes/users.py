from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app import models
from app.schemas import UserCreate, UserOut
from app.security import hash_password

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    exists = await db.scalar(select(models.User).where(models.User.email == payload.email))
    if exists: raise HTTPException(400, "Email já registrado")
    user = models.User(email=payload.email, name=payload.name, hashed_password=hash_password(payload.password))
    db.add(user); await db.commit(); await db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(models.User, user_id)
    if not user: raise HTTPException(404, "Usuário não encontrado")
    return user
