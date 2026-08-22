from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.novel.models import Novel
from src.users.models import User

if TYPE_CHECKING:
    from src.teams.schemas import TeamCreate  # noqa: F401


class TeamType(Enum):
    PUBLISHERS = "publishers"
    AUTHORS = "authors"
    TRANSLATORS = "translators"


class TeamUserRole(Enum):
    CREATOR = "creator"
    MANAGER = "manager"
    NEWBIE = "newbie"


class Team(Base["TeamCreate"]):
    __tablename__: str = "teams"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    type: Mapped[TeamType]

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    is_verified: Mapped[bool] = mapped_column(default=False)

    memberships: Mapped[list[TeamUsers]] = relationship(
        back_populates="team", lazy="selectin"
    )

    users: Mapped[list[User]] = relationship(
        secondary="team_users", back_populates="teams", viewonly=True, lazy="selectin"
    )

    novels: Mapped[list[Novel]] = relationship()


class TeamUsers(Base[None]):
    __tablename__: str = "team_users"

    role: Mapped[TeamUserRole]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped[User] = relationship(
        User, foreign_keys=[user_id], back_populates="memberships", lazy="joined"
    )
    team: Mapped[Team] = relationship(
        Team, foreign_keys=[team_id], back_populates="memberships"
    )
