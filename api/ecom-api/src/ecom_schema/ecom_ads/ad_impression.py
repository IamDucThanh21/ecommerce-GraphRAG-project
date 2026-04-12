"""SQLAlchemy ORM for ecom_ads ad_impression domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_ads"

if TYPE_CHECKING:
    from .advertisement import Advertisement


class AdImpression(Base):
    """Ad impression tracking."""
    
    __tablename__ = "ad_impression"
    __table_args__ = (
        Index("ix_ad_impression_advertisement_id", "advertisement_id"),
        Index("ix_ad_impression_user_id", "user_id"),
        Index("ix_ad_impression_viewed_at", "viewed_at"),
    )

    advertisement_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.advertisement._id"), nullable=False
    )
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), nullable=True)
    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    advertisement: Mapped["Advertisement"] = relationship(back_populates="impressions")
