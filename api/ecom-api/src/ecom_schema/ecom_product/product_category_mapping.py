"""SQLAlchemy ORM for product-category many-to-many relationship."""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Boolean, Index, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product import Product
    from .product_category import ProductCategory


class ProductCategoryMapping(Base):
    """N:N relationship between products and categories. A product can belong to multiple categories."""
    
    __tablename__ = "product_category_mapping"
    __table_args__ = (
        UniqueConstraint("product_id", "category_id", name="uq_product_category_mapping"),
        Index("ix_product_category_mapping_product_id", "product_id"),
        Index("ix_product_category_mapping_category_id", "category_id"),
    )

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
    )
    category_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_category._id"), nullable=False
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product: Mapped["Product"] = relationship(back_populates="category_mappings")
    category: Mapped["ProductCategory"] = relationship(back_populates="product_mappings")
