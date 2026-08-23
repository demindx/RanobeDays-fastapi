from pydantic import BaseModel, ConfigDict

from src.teams.models import TeamType, TeamUserRole
from src.users.schemas import UserResponse


class TeamCreate(BaseModel):
    creator_id: int
    name: str
    type: TeamType


class TeamUpdate(BaseModel):
    name: str | None = None
    type: TeamType | None = None


class TeamResponse(BaseModel):
    id: int
    name: str
    type: TeamType

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamUsersResponse(BaseModel):
    user: UserResponse
    role: TeamUserRole

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamAddUser(BaseModel):
    user_id: int
    role: TeamUserRole
