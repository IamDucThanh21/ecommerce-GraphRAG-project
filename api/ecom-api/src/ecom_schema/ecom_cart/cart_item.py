"""SQLAlchemy ORM for ecom_cart cart_item domain."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_cart"

if TYPE_CHECKING:
    from .cart import Cart


class CartItem(Base):
    """Individual item in a cart."""
    
    __tablename__ = "cart_item"
    __table_args__ = (
        Index("ix_cart_item_cart_id", "cart_id"),
        Index("ix_cart_item_product_variant_id", "product_variant_id"),
    )

    cart_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.cart._id"), nullable=False
    )
    product_variant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    final_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="items")
