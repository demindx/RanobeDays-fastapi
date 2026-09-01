from typing import Annotated

from pydantic import BaseModel, StringConstraints

BookmarkName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)
]


class BookmarkCreate(BaseModel):
    name: BookmarkName
    is_public: bool = True


class BookmarkUpdate(BaseModel):
    name: BookmarkName | None = None
    is_public: bool | None = None


class BookmarkItemCreate(BaseModel):
    novel_id: int


class BookmarkItemResponse(BaseModel): ...


class BookmarkResponse(BaseModel):
    name: BookmarkName
    items: list[BookmarkItemResponse]
