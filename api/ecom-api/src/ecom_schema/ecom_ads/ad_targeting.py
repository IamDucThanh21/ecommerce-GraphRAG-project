"""SQLAlchemy ORM for ecom_ads ad_targeting domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_ads"

if TYPE_CHECKING:
    from .advertisement import Advertisement


class AdTargeting(Base):
    """Advertisement targeting rules."""
    
    __tablename__ = "ad_targeting"
    __table_args__ = (
        Index("ix_ad_targeting_advertisement_id", "advertisement_id"),
    )

    advertisement_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.advertisement._id"), nullable=False
    )
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # DEMOGRAPHICS, INTERESTS, BEHAVIOR
    target_value: Mapped[str] = mapped_column(String(500), nullable=False)

    advertisement: Mapped["Advertisement"] = relationship(back_populates="targetings")
