import uuid
from datetime import datetime

from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: str
    refresh_token: uuid.UUID


class TokenData(BaseModel):
    sub: int
    exp: datetime


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: int
    fingerprint: str
