from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.schemas.car import CarBase

class UserBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    password: str

    first_name: str
    second_name: str
    last_name: str
    
class UserCreate(UserBase):
    pass

class UserRead(BaseModel):
    id: int
    phone: str
    email: Optional[EmailStr] = None

    first_name: str
    second_name: str
    last_name: str
    
    car: List[CarBase] = []

    class Config:
        from_attributes = True