"""SQLAlchemy ORM for product_variant domain."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Numeric, String, Integer, Index, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import ProductVariantStatusEnum

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product import Product
    from .product_image import ProductImage


class ProductVariant(Base):
    """Product variants with different SKU, price, stock, and attributes (color, storage, etc.)."""
    
    __tablename__ = "product_variant"
    __table_args__ = (
        UniqueConstraint("sku", name="uq_product_variant_sku"),
        Index("ix_product_variant_product_id", "product_id"),
        Index("ix_product_variant_sku", "sku"),
    )

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
    )
    sku: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[ProductVariantStatusEnum] = mapped_column(
        SQLEnum(ProductVariantStatusEnum, name="productvariantstatusenum", schema=SCHEMA),
        nullable=False,
        default=ProductVariantStatusEnum.ACTIVE
    )

    product: Mapped["Product"] = relationship(back_populates="variants")
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="variant", cascade="all, delete-orphan"
    )

