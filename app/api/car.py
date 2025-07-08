from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.core.security import verify_access_token

from app.schemas.car import CarCreate, CarRead

from app.crud.car import CarCRUD
from app.crud.user import UserCRUD

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cars", tags=["cars"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

car_crud = CarCRUD()
user_crud = UserCRUD()

@router.post("/add", response_model=CarRead)
async def add(
    car_data: CarCreate, 
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        payload = verify_access_token(token)
        user_id = int(payload.get("sub"))

        user = await user_crud.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        car_dict = car_data.model_dump()
        car_dict["owner_id"] = user_id

        db_car = await CarCRUD.add_car(db=db, car_data=car_dict)
        if not db_car:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create car record"
            )
        
        return db_car
    
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
