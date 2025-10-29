from datetime import datetime
from pydantic import BaseModel

from src.novel.models import NovelStatus, NovelType


class NovelCreate(BaseModel):
    title: str
    age_limit: int
    description: int
    publish_date: datetime
    type: NovelType


class NovelUpdate(BaseModel):
    title: str | None = None
    age_limit: int | None = None
    description: int | None = None
    publish_date: datetime | None = None
    type: NovelType | None = None
    status: NovelStatus | None = None

