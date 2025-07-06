from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessoinLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessoinLocal as session:
        yield session