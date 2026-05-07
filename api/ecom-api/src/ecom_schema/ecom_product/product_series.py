"""SQLAlchemy ORM for product series entities."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, Index, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_line import ProductLine
    from .product import Product


class ProductSeries(Base):
    """Series within a product line. E.g.: iPhone 17 Series, Galaxy S25."""
    
    __tablename__ = "product_series"
    __table_args__ = (
        UniqueConstraint("line_id", "slug", name="uq_product_series_line_slug"),
        Index("ix_product_series_line_id", "line_id"),
    )

    line_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_line._id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    line: Mapped["ProductLine"] = relationship(back_populates="series")
    products: Mapped[List["Product"]] = relationship(
        back_populates="series", cascade="all, delete-orphan"
    )
