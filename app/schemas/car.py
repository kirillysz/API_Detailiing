from pydantic import BaseModel

class CarBase(BaseModel):
    id: int
    model: str
    license_plate: str

    class Config:
        from_attributes = True