from datetime import datetime

from pydantic import BaseModel

from src.novel.models import NovelStatus, NovelType


class NovelCreate(BaseModel):
    title: str
    age_limit: int
    team_id: int
    description: str
    publish_date: datetime
    type: NovelType


class NovelUpdate(BaseModel):
    title: str | None = None
    age_limit: int | None = None
    description: str | None = None
    publish_date: datetime | None = None
    type: NovelType | None = None
    status: NovelStatus | None = None


class NovelResponse(BaseModel):
    title: str
    description: str
    type: NovelType
    publish_date: datetime

    class Config:
        from_attributes = True
