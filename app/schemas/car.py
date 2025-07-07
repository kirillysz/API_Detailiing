from pydantic import BaseModel, ConfigDict
from typing import Optional


class CarBase(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None

    owner_id: int

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None

class CarRead(CarBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
