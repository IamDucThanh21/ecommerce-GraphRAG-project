"""SQLAlchemy ORM for ecom_product product_spec_value domain."""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Integer, Boolean, Numeric, Text, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_attribute import SpecAttribute


class ProductSpecValue(Base):
    """Product specification values."""
    
    __tablename__ = "product_spec_value"
    __table_args__ = (
        Index("ix_product_spec_value_product_id", "product_id"),
        Index("ix_product_spec_value_attribute_id", "attribute_id"),
    )

    product_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    attribute_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.spec_attribute._id"), nullable=False
    )
    value_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value_number: Mapped[Optional[float]] = mapped_column(Numeric(15, 4), nullable=True)
    value_boolean: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    value_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    attribute: Mapped["SpecAttribute"] = relationship(back_populates="values")
