from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from app.models.car import Car
from app.schemas.car import CarRead

class CarCRUD:
    @staticmethod
    async def check_existing(db: AsyncSession, car_data: dict) -> CarRead:
        if not car_data.get("vin"):
            return None
        
        query = select(Car).where(
            (Car.vin == car_data.get("vin")) & 
            (Car.owner_id != car_data.get("owner_id"))
        )
        result = await db.execute(query)
        existing_car = result.scalars().first()

        if existing_car:
            return CarRead.model_validate(existing_car, from_attributes=True)
        
        return None
            
    @staticmethod
    async def add_car(db: AsyncSession, car_data: dict) -> CarRead:
        existing_car = await CarCRUD.check_existing(db, car_data)
        if existing_car:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This vehicle is already registered to another customer"
            )
        
        new_car = Car(**car_data)
        db.add(new_car)

        await db.commit()
        await db.refresh(new_car)

        return CarRead.model_validate(new_car, from_attributes=True)
