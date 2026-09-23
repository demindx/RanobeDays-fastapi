import uuid
from datetime import datetime

from src.core.schemas import SchemaBase


class Tokens(SchemaBase):
    access_token: str
    refresh_token: uuid.UUID

class TokenResponse(SchemaBase):
    access_token: str

class TokenData(SchemaBase):
    sub: int
    exp: datetime

class RefreshRequest(SchemaBase):
    refresh_token: uuid.UUID

class RefreshSessionCreate(SchemaBase):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: int
