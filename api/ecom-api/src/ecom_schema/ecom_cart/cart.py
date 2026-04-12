"""SQLAlchemy ORM for ecom_cart cart domain."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, String, Index, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_cart"

if TYPE_CHECKING:
    from .cart_item import CartItem
    from .cart_discount import CartDiscount


class Cart(Base):
    """Shopping cart."""
    
    __tablename__ = "cart"
    __table_args__ = (
        Index("ix_cart_user_id", "user_id"),
    )

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # ACTIVE, ABANDONED, COMPLETED
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    total_discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    final_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    created_at: Mapped[sa.DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    items: Mapped[List["CartItem"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan"
    )
    discounts: Mapped[List["CartDiscount"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan"
    )
