from pydantic import BaseModel

from src.users.models import UserRoleEnum


class UserResponse(BaseModel):
    login: str
    email: str
    password_hash: str
    role: UserRoleEnum

    class Config:
        from_attributes = True
