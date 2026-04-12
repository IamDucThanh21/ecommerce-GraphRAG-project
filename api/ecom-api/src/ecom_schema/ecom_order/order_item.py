"""SQLAlchemy ORM for ecom_order order_item domain."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_order"

if TYPE_CHECKING:
    from .order import Order


class OrderItem(Base):
    """Individual items in an order."""
    
    __tablename__ = "order_item"
    __table_args__ = (
        Index("ix_order_item_order_id", "order_id"),
        Index("ix_order_item_product_variant_id", "product_variant_id"),
    )

    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.order._id"), nullable=False
    )
    product_variant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    final_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
