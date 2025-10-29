from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, ForeignKey, String
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
from src.core.models import Base ,BaseTimestamps


class NovelType(Enum):
    ORIGINAL = "original"
    TRANSLATION = "translation"


class NovelStatus(Enum):
    FROZEN = "frozen"
    CONTINUES = "continues"
    COMPLETED = "completed"
    ABADONED = "abadoned"


class Novel(Base, BaseTimestamps):
    __tablename__ = "novel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    cover_path: Mapped[str] = mapped_column(String(255))

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    embedding: Mapped[Vector] = mapped_column(Vector())
    description: Mapped[str] = mapped_column()

    publish_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    type: Mapped[NovelType] = mapped_column()
    status: Mapped[NovelStatus] = mapped_column()

    age_limit: Mapped[int] = mapped_column()

    is_approved: Mapped[bool] = mapped_column(default=False)
