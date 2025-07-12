from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base, BaseTimestamps


class UserRoleEnum(Enum):
    ADMIN = "admin"
    COMMON = "common"
    MANAGER = "manager"


class UserModel(Base, BaseTimestamps):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    login: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    is_active: Mapped[bool] = mapped_column(default=False)

    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.COMMON)

    user_profile: Mapped["UserProfileModel"] = relationship(back_populates="user")


class UserProfileModel(Base, BaseTimestamps):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    readed_chapters: Mapped[int] = mapped_column(default=0)

    user: Mapped["UserModel"] = relationship(
        back_populates="user_profile", single_parent=True
    )
