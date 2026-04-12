"""SQLAlchemy ORM for ecom_ads advertisement domain."""

from __future__ import annotations

from decimal import Decimal
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, String, Text, DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_ads"

if TYPE_CHECKING:
    from .ad_targeting import AdTargeting
    from .ad_impression import AdImpression
    from .ad_click import AdClick


class Advertisement(Base):
    """Advertisement campaigns."""
    
    __tablename__ = "advertisement"
    __table_args__ = (
        Index("ix_advertisement_advertiser_id", "advertiser_id"),
        Index("ix_advertisement_status", "status"),
    )

    advertiser_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # DRAFT, ACTIVE, PAUSED, COMPLETED
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    targetings: Mapped[List["AdTargeting"]] = relationship(
        back_populates="advertisement", cascade="all, delete-orphan"
    )
    impressions: Mapped[List["AdImpression"]] = relationship(
        back_populates="advertisement", cascade="all, delete-orphan"
    )
    clicks: Mapped[List["AdClick"]] = relationship(
        back_populates="advertisement", cascade="all, delete-orphan"
    )
