from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base, BaseTimestamps

if TYPE_CHECKING:
    from src.category.model import Category  # noqa: F401
    from src.novel.schemas import NovelCreate  # noqa: F401


class NovelType(Enum):
    ORIGINAL = "original"
    TRANSLATION = "translation"


class NovelStatus(Enum):
    FROZEN = "frozen"
    CONTINUES = "continues"
    COMPLETED = "completed"
    ABADONED = "abadoned"


class Novel(Base["NovelCreate"], BaseTimestamps):
    __tablename__ = "novels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    cover_path: Mapped[str] = mapped_column(String(255), default="default_cover.png")

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    embedding: Mapped[Vector] = mapped_column(Vector(), default=[0.0, 0.0, 0.1])
    description: Mapped[str] = mapped_column()

    publish_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    type: Mapped[NovelType] = mapped_column()
    status: Mapped[NovelStatus] = mapped_column(default=NovelStatus.CONTINUES)

    age_limit: Mapped[int] = mapped_column()

    is_approved: Mapped[bool] = mapped_column(default=False)

    categories: Mapped[list[Category]] = relationship(secondary="novel_categories")

    @staticmethod
    def generate_slug(target: Novel, value: str, oldvalue: str, initiator: str):
        if value and (oldvalue is not value):
            slug = value.lower().split()
            slug = "-".join(slug)

            target.slug = slug


class NovelCategories(Base[None]):
    __tablename__ = "novel_categories"

    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )


event.listen(Novel.title, "set", Novel.generate_slug, retval=False)
