from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class BaseTimestamps:
    created_at: Mapped[datetime | None] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(
        default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
