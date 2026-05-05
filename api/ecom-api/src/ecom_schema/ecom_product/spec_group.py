"""SQLAlchemy ORM for ecom_product spec_group domain."""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_attribute import SpecAttribute
    from .product_category import ProductCategory


class SpecGroup(Base):
    """Specification group for product attributes."""
    
    __tablename__ = "spec_group"
    __table_args__ = (
        Index("ix_spec_group_category_id", "category_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_category._id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    category: Mapped[Optional["ProductCategory"]] = relationship(
        back_populates="spec_groups"
    )
    attributes: Mapped[List["SpecAttribute"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
