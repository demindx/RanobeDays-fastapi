from pydantic import BaseModel

from src.teams.models import TeamType, TeamUserRole
from src.users.schemas import UserResponse


class TeamCreate(BaseModel):
    creator_id: int
    name: str
    type: TeamType


class TeamUpdate(BaseModel):
    name: str | None
    type: TeamType | None


class TeamResponse(BaseModel):
    id: int
    name: str
    type: TeamType

    class Config:
        from_attributes: bool = True


class TeamUsersResponse(BaseModel):
    user: UserResponse
    role: TeamUserRole


class TeamAddUser(BaseModel):
    user_id: int
    role: TeamUserRole
