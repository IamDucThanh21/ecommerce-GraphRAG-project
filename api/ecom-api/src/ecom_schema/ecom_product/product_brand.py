"""SQLAlchemy ORM for product brand entities."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_line import ProductLine
    from .product import Product


class ProductBrand(Base):
    """Brand/manufacturer (highest level in product hierarchy)."""
    
    __tablename__ = "product_brand"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_product_brand_slug"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    lines: Mapped[List["ProductLine"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )
    products: Mapped[List["Product"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )
