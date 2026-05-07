"""SQLAlchemy ORM for spec group template (template definition per category)."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_category import ProductCategory
    from .spec_attribute_template import SpecAttributeTemplate
    from .product_spec_group import ProductSpecGroup


class SpecGroupTemplate(Base):
    """Specification group template per category. E.g., category 'Phone' has groups: Display, Camera, Chipset, Battery."""
    
    __tablename__ = "spec_group_template"
    __table_args__ = (
        Index("ix_spec_group_template_category_id", "category_id"),
    )

    category_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_category._id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    category: Mapped["ProductCategory"] = relationship(back_populates="spec_group_templates")
    attribute_templates: Mapped[List["SpecAttributeTemplate"]] = relationship(
        back_populates="group_template", cascade="all, delete-orphan"
    )
    product_spec_groups: Mapped[List["ProductSpecGroup"]] = relationship(
        back_populates="group_template", cascade="all, delete-orphan"
    )
