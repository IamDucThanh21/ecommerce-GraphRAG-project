"""SQLAlchemy ORM and DB connector for product_domain."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, Index, String, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_variant import ProductVariant
    from .product_image import ProductImage


class Product(Base):
    """Product information."""
    __tablename__ = "product"
    __table_args__ = (
        Index("ix_product_created_at", "created_at"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # ACTIVE, INACTIVE, DISCONTINUED
    llm_spec_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    variants: Mapped[List["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    images: Mapped[List["ProductImage"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

