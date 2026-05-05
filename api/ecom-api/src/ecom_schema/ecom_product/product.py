from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import ProductStatusEnum

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_variant import ProductVariant
    from .product_image import ProductImage
    from .product_line import ProductLine
    from .product_spec_value import ProductSpecValue
    from .promotion import Promotion
    from .customer_review import CustomerReview


class Product(Base):
    """Product information."""
    __tablename__ = "product"
    __table_args__ = (
        Index("ix_product_created_at", "created_at"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    line_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_line._id"), nullable=False
    )
    status: Mapped[ProductStatusEnum] = mapped_column(
        SQLEnum(
            ProductStatusEnum,
            name="productstatusenum",
            schema=SCHEMA,
        ),
        nullable=False
    )
    llm_spec_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    line: Mapped["ProductLine"] = relationship(back_populates="products")
    promotions: Mapped[List["Promotion"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    reviews: Mapped[List["CustomerReview"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    variants: Mapped[List["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    images: Mapped[List["ProductImage"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    spec_values: Mapped[List["ProductSpecValue"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

