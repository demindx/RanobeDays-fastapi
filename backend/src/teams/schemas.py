from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.teams.models import TeamType, TeamUserRole
from src.users.schemas import UserResponse

TeamName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class TeamCreate(BaseModel):
    creator_id: int
    name: TeamName
    type: TeamType


class TeamUpdate(BaseModel):
    name: TeamName | None = None
    type: TeamType | None = None


class TeamResponse(BaseModel):
    id: int
    name: TeamName
    type: TeamType

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamUsersResponse(BaseModel):
    user: UserResponse
    role: TeamUserRole

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamAddUser(BaseModel):
    user_id: int
    role: TeamUserRole
