from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.car import Car
from app.schemas.car import CarBase