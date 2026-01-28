from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base

if TYPE_CHECKING:
    from src.language.schemas import LanguageCreate  # noqa: F401


class Language(Base["LanguageCreate"]):
    __tablename__ = "languages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100))
    # code: Mapped[str] = mapped_column(String(10))
