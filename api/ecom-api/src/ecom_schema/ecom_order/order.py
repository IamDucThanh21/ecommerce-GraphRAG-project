"""SQLAlchemy ORM for ecom_order order domain."""

from __future__ import annotations

from decimal import Decimal
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, String, DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_order"

if TYPE_CHECKING:
    from .order_item import OrderItem


class Order(Base):
    """Customer orders."""
    
    __tablename__ = "order"
    __table_args__ = (
        Index("ix_order_user_id", "user_id"),
        Index("ix_order_created_at", "created_at"),
    )

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    final_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
