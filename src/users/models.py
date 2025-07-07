from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserRoleEnum(Enum):
    ADMIN = "admin"
    COMMON = "common"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    login: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))

    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRoleEnum]

    user_profile: Mapped["UserProfile"] = relationship(back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    readed_chapters: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="user_profile", single_parent=True)
