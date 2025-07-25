from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base


class TeamType(Enum):
    PUBLISHERS = "publishers"
    AUTHORS = "authors"
    TRANSLATORS = "translators"


class Team(Base):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    type: Mapped[TeamType]

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    is_verified: Mapped[bool] = mapped_column(default=False)
