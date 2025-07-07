from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

class UserCRUD:
    @staticmethod
    async def check_existing(db: AsyncSession, user_data: dict) -> UserRead:
        query = select(User).where(
            or_(
                User.email == user_data.get("email"),
                User.phone == user_data.get("phone")
            )
        )
        result = await db.execute(query)
        existing_user = result.scalars().first()

        return UserRead.model_validate(existing_user, from_attributes=True)

    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict) -> UserRead:
        is_exists = await UserCRUD.check_existing(db, user_data)
        if is_exists:
            raise HTTPException(status_code=409, detail="User already exists")

        new_user = User(**user_data)
        db.add(new_user)
        
        await db.commit()
        await db.refresh(new_user)

        return UserRead.model_validate(new_user, from_attributes=True)

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> UserRead:
        user = await UserCRUD.get_user_by_id(db, user_id)
        if not user:
            return HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh()

        return user


    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserRead:
        query = select(User).where(
            User.id == user_id
        )
        result = await db.execute(query)
        existing_user = result.scalars().first()

        return UserRead.model_validate(existing_user, from_attributes=True)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> UserRead:
        query = select(User).where(
            User.email == email
        )
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        
        return UserRead.model_validate(user, from_attributes=True)
