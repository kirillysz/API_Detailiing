from pydantic import BaseModel

class CarBase(BaseModel):
    id: int
    model: str
    license_plate: str

    class Config:
        orm_mode = True