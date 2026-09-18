import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Tokens(BaseModel):
    access_token: str
    refresh_token: uuid.UUID

    model_config = ConfigDict(extra="forbid")


class TokenResponse(BaseModel):
    access_token: str

    model_config = ConfigDict(extra="forbid")


class TokenData(BaseModel):
    sub: int
    exp: datetime

    model_config = ConfigDict(extra="forbid")


class RefreshRequest(BaseModel):
    refresh_token: uuid.UUID

    model_config = ConfigDict(extra="forbid")


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: int

    model_config = ConfigDict(extra="forbid")
