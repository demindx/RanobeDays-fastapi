from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base, BaseTimestamps

if TYPE_CHECKING:
    from src.teams.models import Team, TeamUsers
    from src.users.schemas import UserProfileCreate, UserRegister  # noqa: F401


class UserRoleEnum(Enum):
    ADMIN = "admin"
    COMMON = "common"
    MANAGER = "manager"


class User(Base["UserRegister"], BaseTimestamps):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.COMMON)

    user_profile: Mapped[UserProfile] = relationship(
        back_populates="user", lazy="joined"
    )
    memberships: Mapped[list[TeamUsers]] = relationship(
        back_populates="user", lazy="selectin"
    )

    teams: Mapped[list[Team]] = relationship(
        back_populates="users", secondary="team_users", viewonly=True, lazy="selectin"
    )


class UserProfile(Base["UserProfileCreate"], BaseTimestamps):
    __tablename__: str = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    readed_chapters: Mapped[int] = mapped_column(default=0)

    nickname: Mapped[str]

    user: Mapped[User] = relationship(back_populates="user_profile", single_parent=True)
