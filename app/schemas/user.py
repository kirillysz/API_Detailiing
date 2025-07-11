from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List

from app.schemas.car import CarRead

class UserBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    password: str

    first_name: str
    second_name: str
    last_name: str

    is_active: bool = False
    
class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    id: int
    phone: str
    email: Optional[EmailStr] = None

    first_name: str
    second_name: str
    last_name: str
    
    password_hash: Optional[str] = None

    cars: List[CarRead] = []

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
