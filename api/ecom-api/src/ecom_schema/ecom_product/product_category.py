"""SQLAlchemy ORM for product category (recursive tree hierarchy)."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Text, Index, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_group_template import SpecGroupTemplate
    from .product_category_mapping import ProductCategoryMapping


class ProductCategory(Base):
    """Product category (recursive tree). E.g., Electronics → Phones → Android."""
    
    __tablename__ = "product_category"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_product_category_slug"),
        Index("ix_product_category_parent_id", "parent_id"),
    )

    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_category._id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    parent: Mapped[Optional["ProductCategory"]] = relationship(
        back_populates="children", remote_side="ProductCategory._id"
    )
    children: Mapped[List["ProductCategory"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    spec_group_templates: Mapped[List["SpecGroupTemplate"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
    product_mappings: Mapped[List["ProductCategoryMapping"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
