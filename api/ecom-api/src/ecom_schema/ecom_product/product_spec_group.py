"""SQLAlchemy ORM for product specification group (instance of template on a product)."""

from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy import String, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product import Product
    from .spec_group_template import SpecGroupTemplate
    from .product_spec_value import ProductSpecValue


class ProductSpecGroup(Base):
    """Instance of a spec group for a specific product. Can be created from template or freely added by admin."""
    
    __tablename__ = "product_spec_group"
    __table_args__ = (
        Index("ix_product_spec_group_product_id", "product_id"),
        Index("ix_product_spec_group_group_template_id", "group_template_id"),
    )

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product._id"), nullable=False
    )
    group_template_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.spec_group_template._id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["Product"] = relationship(back_populates="spec_groups")
    group_template: Mapped[Optional["SpecGroupTemplate"]] = relationship(back_populates="product_spec_groups")
    spec_values: Mapped[List["ProductSpecValue"]] = relationship(
        back_populates="spec_group", cascade="all, delete-orphan"
    )
