from pydantic import BaseModel


class ChapterCreate(BaseModel):
    title: str
    number: int
    content: str

    novel_id: int


class ChapterUpdate(BaseModel):
    title: str | None = None
    number: int | None = None
    content: str | None = None

    is_published: bool | None = None


class ChapterResponse(BaseModel):
    title: str
    number: int
    content: str

    is_published: bool

    class Config:
        from_attributes = True
