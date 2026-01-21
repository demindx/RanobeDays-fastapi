from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base, BaseTimestamps


class Chapter(Base[None], BaseTimestamps):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(100))
    number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text())

    is_published: Mapped[bool] = mapped_column(default=False)

    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id"))
