import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.auth.schemas import RefreshSessionCreate
from src.core.models import Base, BaseTimestamps


class RefreshSession(Base[RefreshSessionCreate], BaseTimestamps):
    __tablename__: str = "refresh_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4
    )

    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID, index=True)

    expires_in: Mapped[int] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
