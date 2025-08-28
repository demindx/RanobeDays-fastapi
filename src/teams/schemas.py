from pydantic import BaseModel

from src.teams.models import TeamType


class TeamCreate(BaseModel):
    creator_id: int
    name: str
    type: TeamType


class TeamUpdate(BaseModel):
    name: str | None
    type: TeamType | None


class TeamResponse(BaseModel):
    name: str
    type: TeamType

    class Config:
        from_attributes = True
