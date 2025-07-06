from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import UserCRUD
from app.core.security import hash_password, create_access_token

router = APIRouter(prefix="/users")
user_crud = UserCRUD()

@router.post("/create", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)

    user_data = user.model_dump()
    user_data["password"] = hashed_password
    
    try:
        db_user = await user_crud.create_user(
            db=db,
            user_data=user_data
        )
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
