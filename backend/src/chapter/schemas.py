from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChapterCreate(BaseModel):
    title: str
    number: int
    content: str

    novel_id: int
    team_id: int


class ChapterUpdate(BaseModel):
    title: str | None = None
    number: int | None = None
    content: str | None = None

    is_published: bool | None = None


class ChapterResponse(BaseModel):
    id: int
    novel_id: int
    title: str
    number: int
    content: str
    is_published: bool
    created_at: datetime

    model_config: ConfigDict = ConfigDict(from_attributes=True)
