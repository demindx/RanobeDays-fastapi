from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

ChapterTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
ChapterContent = Annotated[str, StringConstraints(min_length=1)]


class ChapterCreate(BaseModel):
    title: ChapterTitle
    number: int
    content: ChapterContent

    novel_id: int
    team_id: int


class ChapterUpdate(BaseModel):
    title: ChapterTitle | None = None
    number: int | None = None
    content: ChapterContent | None = None

    is_published: bool | None = None


class ChapterResponse(BaseModel):
    id: int
    novel_id: int
    title: ChapterTitle
    number: int
    content: ChapterContent
    is_published: bool
    created_at: datetime

    model_config: ConfigDict = ConfigDict(from_attributes=True)
