"""SQLAlchemy ORM for product brand entities."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_line import ProductLine


class ProductBrand(Base):
    __tablename__ = "product_brand"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    lines: Mapped[List["ProductLine"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan"
    )
