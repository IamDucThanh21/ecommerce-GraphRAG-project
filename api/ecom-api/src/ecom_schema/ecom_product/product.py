from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import ProductStatusEnum

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_brand import ProductBrand
    from .product_line import ProductLine
    from .product_series import ProductSeries
    from .product_category_mapping import ProductCategoryMapping
    from .product_variant import ProductVariant
    from .product_image import ProductImage
    from .product_spec_group import ProductSpecGroup
    # from .promotion import Promotion
    # from .customer_review import CustomerReview


class Product(Base):
    """Core product entity. Linked to brand (required), line and series (optional), and categories via N:N mapping."""
    
    __tablename__ = "product"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_product_slug"),
        Index("ix_product_brand_id", "brand_id"),
        Index("ix_product_line_id", "line_id"),
        Index("ix_product_series_id", "series_id"),
        Index("ix_product_status", "status"),
        sa.CheckConstraint(
            "series_id IS NULL OR line_id IS NOT NULL",
            name="ck_product_series_requires_line"
        )
    )

    brand_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_brand._id"), nullable=False
    )
    line_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_line._id"), nullable=True
    )
    series_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_series._id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProductStatusEnum] = mapped_column(
        SQLEnum(ProductStatusEnum, name="productstatusenum", schema=SCHEMA),
        nullable=False,
        default=ProductStatusEnum.DRAFT
    )

    brand: Mapped["ProductBrand"] = relationship(back_populates="products")
    line: Mapped[Optional["ProductLine"]] = relationship(back_populates="products")
    series: Mapped[Optional["ProductSeries"]] = relationship(back_populates="products")
    category_mappings: Mapped[List["ProductCategoryMapping"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    variants: Mapped[List["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    images: Mapped[List["ProductImage"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    spec_groups: Mapped[List["ProductSpecGroup"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    # promotions: Mapped[List["Promotion"]] = relationship(
    #     back_populates="product", cascade="all, delete-orphan"
    # )
    # reviews: Mapped[List["CustomerReview"]] = relationship(
    #     back_populates="product", cascade="all, delete-orphan"
    # )


