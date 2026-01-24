from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base, BaseTimestamps

if TYPE_CHECKING:
    from src.chapter.schemas import ChapterCreate  # noqa: F401


class Chapter(Base["ChapterCreate"], BaseTimestamps):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(100))
    number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text())

    is_published: Mapped[bool] = mapped_column(default=False)

    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id"))
