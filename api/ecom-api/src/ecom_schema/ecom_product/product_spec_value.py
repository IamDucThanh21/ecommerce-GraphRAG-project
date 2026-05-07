"""SQLAlchemy ORM for product specification values (actual values for a product)."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Boolean, Numeric, Text, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .product_spec_group import ProductSpecGroup
    from .spec_attribute_template import SpecAttributeTemplate


class ProductSpecValue(Base):
    """Product specification values. Stores multiple value types (text/number/boolean) to support both display and filtering."""
    
    __tablename__ = "product_spec_value"
    __table_args__ = (
        Index("ix_product_spec_value_spec_group_id", "product_spec_group_id"),
        Index("ix_product_spec_value_attribute_template_id", "attribute_template_id"),
        Index("ix_product_spec_value_key_number_filterable", "key", "value_number", 
              postgresql_where=sa.text("is_filterable = true")),
        Index("ix_product_spec_value_key_text_filterable", "key", "value_text", 
              postgresql_where=sa.text("is_filterable = true")),
    )

    product_spec_group_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.product_spec_group._id"), nullable=False
    )
    attribute_template_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.spec_attribute_template._id"), nullable=True
    )
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    value_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value_number: Mapped[Optional[float]] = mapped_column(Numeric(15, 4), nullable=True)
    value_unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    value_boolean: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_filterable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    spec_group: Mapped["ProductSpecGroup"] = relationship(back_populates="spec_values")
    attribute_template: Mapped[Optional["SpecAttributeTemplate"]] = relationship(back_populates="spec_values")

