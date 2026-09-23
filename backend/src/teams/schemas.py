from typing import Annotated

from pydantic import ConfigDict, StringConstraints

from src.core.schemas import SchemaBase
from src.teams.models import TeamType, TeamUserRole
from src.users.schemas import UserResponse

TeamName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]


class TeamCreate(SchemaBase):
    creator_id: int
    name: TeamName
    type: TeamType

class TeamUpdate(SchemaBase):
    name: TeamName | None = None
    type: TeamType | None = None

class TeamResponse(SchemaBase):
    id: int
    name: TeamName
    type: TeamType

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamUsersResponse(SchemaBase):
    user: UserResponse
    role: TeamUserRole

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class TeamAddUser(SchemaBase):
    user_id: int
    role: TeamUserRole
