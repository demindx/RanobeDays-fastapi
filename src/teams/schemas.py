from pydantic import BaseModel

from src.teams.models import TeamType, TeamUserRole


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
        from_attributes = True


class TeamAddUser(BaseModel):
    user_id: int
    role: TeamUserRole
