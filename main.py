from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.user import router as user_router
from app.api.car import router as car_router
from app.api.auth import router as auth_router

from app.core.initial_tables import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(car_router)