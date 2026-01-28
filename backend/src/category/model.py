from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base

if TYPE_CHECKING:
    from src.chapters.schemas import ChapterCreate  # noqa: F401


class CategoryTypeEnum(Enum):
    TAG = "tag"
    GENRE = "genre"


class Category(Base["ChapterCreate"]):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    type: Mapped[CategoryTypeEnum]
