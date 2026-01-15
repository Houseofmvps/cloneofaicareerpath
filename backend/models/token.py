"""Token response model"""
from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str
