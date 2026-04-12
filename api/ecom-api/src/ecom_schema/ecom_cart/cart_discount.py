"""SQLAlchemy ORM for ecom_cart cart_discount domain."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_cart"

if TYPE_CHECKING:
    from .cart import Cart
    from .discount import Discount


class CartDiscount(Base):
    """Discount applied to a cart."""
    
    __tablename__ = "cart_discount"
    __table_args__ = (
        Index("ix_cart_discount_cart_id", "cart_id"),
        Index("ix_cart_discount_discount_id", "discount_id"),
    )

    cart_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.cart._id"), nullable=False
    )
    discount_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.discount._id"), nullable=False
    )
    applied_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="discounts")
    discount: Mapped["Discount"] = relationship()
