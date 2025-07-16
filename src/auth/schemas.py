import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: str
    refresh_token: uuid.UUID


class TokenData(BaseModel):
    sub: int
    type: Literal["access", "refresh"]
    exp: datetime


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: int
    fingerprint: str
