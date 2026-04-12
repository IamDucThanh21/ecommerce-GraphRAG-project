"""SQLAlchemy ORM for product_variant domain."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, String, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product import Product


class ProductVariant(Base):
    """Product variants with different SKU, price, and stock."""
    
    __tablename__ = "product_variant"
    __table_args__ = (
        Index("ix_product_variant_product_id", "product_id"),
        Index("ix_product_variant_sku", "sku"),
    )

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
    )
    sku: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    product: Mapped["Product"] = relationship(back_populates="variants")
