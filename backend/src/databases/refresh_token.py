import sqlalchemy

from datetime import datetime, timezone


from sqlalchemy import Boolean, DateTime, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.databases.database import Base


from src.databases.models import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=(lambda: datetime.now(timezone.utc)),
    )

    user: Mapped["User"] = relationship()
