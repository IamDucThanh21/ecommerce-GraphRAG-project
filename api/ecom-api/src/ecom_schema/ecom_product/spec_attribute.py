"""SQLAlchemy ORM for ecom_product spec_attribute domain."""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_group import SpecGroup
    from .product_spec_value import ProductSpecValue


class SpecAttribute(Base):
    """Specification attribute definition."""
    
    __tablename__ = "spec_attribute"
    __table_args__ = (
        Index("ix_spec_attribute_group_id", "group_id"),
    )

    group_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.spec_group._id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), nullable=False)  # STRING, NUMBER, BOOLEAN, LIST, JSON
    unit: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    group: Mapped["SpecGroup"] = relationship(back_populates="attributes")
    values: Mapped[List["ProductSpecValue"]] = relationship(
        back_populates="attribute", cascade="all, delete-orphan"
    )
