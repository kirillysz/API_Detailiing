from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.auth import AuthResponse

from app.crud.user import UserCRUD
from app.core.security import hash_password, create_access_token, verify_access_token, oauth2_scheme

router = APIRouter(prefix="/users", tags=["user"])
user_crud = UserCRUD()

@router.post("/create", response_model=AuthResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)

    user_data = user.model_dump(exclude={"password"})
    user_data["password_hash"] = hashed_password

    try:
        db_user = await user_crud.create_user(
            db=db,
            user_data=user_data
        )
        if not db_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        data = {"sub": str(db_user.id)}
        token = create_access_token(data)

        return {
            "user": db_user,
            "token": {
                "access_token": token,
                "token_type": "bearer"
            }
        }


    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/me", response_model=UserRead)
async def get_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = verify_access_token(token)
        user_id = int(payload.get("sub"))

        user = await user_crud.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err))


@router.put("/update", response_model=UserRead)
async def update(
    user_update: UserUpdate, 
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = verify_access_token(token)
        user_id = int(payload.get("sub"))

        user = await user_crud.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        updated_user = await user_crud.update_user(
            db=db, user_id=user_id, user_update=user_update
        )

        return updated_user
    
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(err)
        )