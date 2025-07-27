from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.users.models import User


class TeamType(Enum):
    PUBLISHERS = "publishers"
    AUTHORS = "authors"
    TRANSLATORS = "translators"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[TeamType]

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    is_verified: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list[User]] = relationship(back_populates="teams")


#TODO: add some additional info like who added what a role of memeber joined_date and etc.
class TeamUsers(Base):
    __tablename__ = "team_users"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), unique=True)
