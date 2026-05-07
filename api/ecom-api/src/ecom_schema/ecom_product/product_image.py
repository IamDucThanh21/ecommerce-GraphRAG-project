"""SQLAlchemy ORM for product_image domain."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Boolean, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product import Product
    from .product_variant import ProductVariant


class ProductImage(Base):
    """Product images (shared or variant-specific). variant_id nullable for shared product images."""
    
    __tablename__ = "product_image"
    __table_args__ = (
        Index("ix_product_image_product_id", "product_id"),
        Index("ix_product_image_variant_id", "variant_id"),
    )

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
    )
    variant_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_variant._id"), nullable=True
    )
    image_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["Product"] = relationship(back_populates="images")
    variant: Mapped[Optional["ProductVariant"]] = relationship(back_populates="images")

