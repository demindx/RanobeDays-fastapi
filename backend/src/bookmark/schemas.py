from pydantic import BaseModel


class BookmarkCreate(BaseModel):
    name: str
    is_public: bool = True


class BookmarkUpdate(BaseModel):
    name: str | None = None
    is_public: bool | None = None


class BookmarkItemCreate(BaseModel):
    novel_id: int


class BookmarkItemResponse(BaseModel): ...


class BookmarkResponse(BaseModel):
    name: str
    items: list[BookmarkItemResponse]
