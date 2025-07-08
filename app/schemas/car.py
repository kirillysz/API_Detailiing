from pydantic import BaseModel, ConfigDict
from typing import Optional


class CarBase(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None
    number: Optional[str] = None
    vin: Optional[str] = None
    
class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None

class CarRead(CarBase):
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)
