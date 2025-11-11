import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import engine, SessionLocal
from app.models import Base, User, Store

async def run():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:  # type: AsyncSession
        res = await db.execute(select(User).where(User.email == "admin@example.com"))
        user = res.scalar_one_or_none()
        if not user:
            user = User(email="admin@example.com", name="Admin", hashed_password="$2b$12$abcdefghijklmnopqrstuv")
            db.add(user); await db.commit(); await db.refresh(user)

        stores = [("loja do Otavio", "19981174662"), ("loja da Patricia", "19998359186"), ("loja maklei", "19989735005")]
        for name, phone in stores:
            res = await db.execute(select(Store).where(Store.name == name))
            if not res.scalar_one_or_none():
                db.add(Store(owner_id=user.id, name=name, whatsapp_number=phone, base_url=None))
        await db.commit()
    print("Seed concluído.")

if __name__ == "__main__":
    asyncio.run(run())
