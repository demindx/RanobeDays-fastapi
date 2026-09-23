from typing import Annotated

from pydantic import StringConstraints

from src.core.schemas import SchemaBase

BookmarkName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)
]


class BookmarkCreate(SchemaBase):
    name: BookmarkName
    is_public: bool = True

class BookmarkUpdate(SchemaBase):
    name: BookmarkName | None = None
    is_public: bool | None = None

class BookmarkItemCreate(SchemaBase):
    novel_id: int

class BookmarkItemResponse(SchemaBase):
    pass

class BookmarkResponse(SchemaBase):
    name: BookmarkName
    items: list[BookmarkItemResponse]
