from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.models.user import User
from app.schemas.user import UserRead

class UserCRUD:
    @staticmethod
    async def check_existing(db: AsyncSession, user_data: dict):
        query = select(User).where(
            or_(
                User.email == user_data.get("email"),
                User.phone == user_data.get("phone")
            )
        )
        result = await db.execute(query)
        existing_user = result.scalars().first()
        return existing_user

    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict):
        is_exists = await UserCRUD.check_existing(db, user_data)
        if is_exists:
            raise HTTPException(status_code=409, detail="User already exists")

        new_user = User(**user_data)
        db.add(new_user)
        
        await db.commit()
        await db.refresh(new_user)

        return UserRead.model_validate(new_user, from_attributes=True)

    @staticmethod
    async def get_user(db: AsyncSession, user_data: dict):
        is_exists = await UserCRUD.check_existing(db, user_data)
        if not is_exists:
            raise HTTPException(status_code=404, detail="User does not exist")

        return UserRead.model_validate(is_exists, from_attributes=True)
