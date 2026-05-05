"""SQLAlchemy ORM for product line entities."""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_brand import ProductBrand
    from .product_category import ProductCategory
    from .product import Product


class ProductLine(Base):
    __tablename__ = "product_line"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_brand._id"), nullable=False
    )
    category_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_category._id"), nullable=False
    )

    brand: Mapped["ProductBrand"] = relationship(back_populates="lines")
    category: Mapped["ProductCategory"] = relationship(back_populates="lines")
    products: Mapped[List["Product"]] = relationship(
        back_populates="line", cascade="all, delete-orphan"
    )
