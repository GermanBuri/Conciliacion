from pydantic import BaseModel

from app.schemas.user import UserRead


class TokenPayload(BaseModel):
    sub: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead
