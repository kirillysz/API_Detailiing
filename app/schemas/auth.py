from pydantic import BaseModel
from app.schemas.user import UserRead
from app.schemas.token import Token

class AuthResponse(BaseModel):
    user: UserRead
    token: Token