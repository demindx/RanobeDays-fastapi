from enum import Enum
from typing import TYPE_CHECKING, Self, override

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base, BaseTimestamps
from src.users.utils import get_password_hash

if TYPE_CHECKING:
    from src.teams.models import Team
    from src.users.schemas import UserProfileCreate, UserRegister  # noqa: F401


class UserRoleEnum(Enum):
    ADMIN = "admin"
    COMMON = "common"
    MANAGER = "manager"


class User(Base[int, "UserRegister"], BaseTimestamps):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.COMMON)

    user_profile: Mapped[UserProfile] = relationship(back_populates="user")
    teams: Mapped[Team] = relationship(back_populates="users")

    @override
    @classmethod
    def from_data(cls, data: UserRegister) -> Self:
        instance = cls(**data.model_dump(exclude={"password1", "password2"}))

        instance.password_hash = get_password_hash(data.password1)

        return instance


class UserProfile(Base[int, "UserProfileCreate"], BaseTimestamps):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    readed_chapters: Mapped[int] = mapped_column(default=0)

    user: Mapped[User] = relationship(back_populates="user_profile", single_parent=True)
