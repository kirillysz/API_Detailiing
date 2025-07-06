from pydantic import BaseModel

class Token(BaseModel):
    access_type: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
    email: str
    
