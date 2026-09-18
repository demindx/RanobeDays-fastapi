from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

BookmarkName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)
]


class BookmarkCreate(BaseModel):
    name: BookmarkName
    is_public: bool = True

    model_config = ConfigDict(extra="forbid")


class BookmarkUpdate(BaseModel):
    name: BookmarkName | None = None
    is_public: bool | None = None

    model_config = ConfigDict(extra="forbid")


class BookmarkItemCreate(BaseModel):
    novel_id: int

    model_config = ConfigDict(extra="forbid")


class BookmarkItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BookmarkResponse(BaseModel):
    name: BookmarkName
    items: list[BookmarkItemResponse]

    model_config = ConfigDict(extra="forbid")
