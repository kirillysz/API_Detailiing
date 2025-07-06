from app.core.database import engine, Base
from app.models.user import User
from app.models.car import Car

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)