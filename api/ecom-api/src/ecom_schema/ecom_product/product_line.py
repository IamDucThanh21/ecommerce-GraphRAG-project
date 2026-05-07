"""SQLAlchemy ORM for product line entities."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, Index, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_brand import ProductBrand
    from .product_series import ProductSeries
    from .product import Product


class ProductLine(Base):
    """Product line (e.g., iPhone, iPad, Galaxy S, Galaxy Tab). Belongs to a brand."""
    
    __tablename__ = "product_line"
    __table_args__ = (
        UniqueConstraint("brand_id", "slug", name="uq_product_line_brand_slug"),
        Index("ix_product_line_brand_id", "brand_id"),
    )

    brand_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_brand._id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    brand: Mapped["ProductBrand"] = relationship(back_populates="lines")
    series: Mapped[List["ProductSeries"]] = relationship(
        back_populates="line", cascade="all, delete-orphan"
    )
    products: Mapped[List["Product"]] = relationship(
        back_populates="line", cascade="all, delete-orphan"
    )
