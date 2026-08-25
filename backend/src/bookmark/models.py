from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base, BaseTimestamps
from src.novel.models import Novel

if TYPE_CHECKING:
    from src.bookmark.schemas import BookmarkCreate, BookmarkItemCreate  # noqa


class Bookmark(Base[BookmarkCreate]):
    __tablename__: str = "bookmarks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    is_public: Mapped[bool] = mapped_column(default=True)

    items: Mapped[list[BookmarkItem]] = relationship(
        back_populates="bookmark", cascade="all, delete-orphan", lazy="selectin"
    )


class BookmarkItem(Base[BookmarkItemCreate], BaseTimestamps):
    __tablename__: str = "bookmark_novels"

    novel_id: Mapped[int] = mapped_column(
        ForeignKey("novels.id", ondelete="CASCADE"), primary_key=True
    )
    bookmark_id: Mapped[int] = mapped_column(
        ForeignKey("bookmarks.id", ondelete="CASCADE"), primary_key=True
    )

    bookmark: Mapped[Bookmark] = relationship(Bookmark, foreign_keys=[bookmark_id])
    novel: Mapped[Novel] = relationship(Novel, foreign_keys=[novel_id], lazy="joined")
