"""SQLAlchemy ORM for ecom_product spec_group domain."""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_attribute import SpecAttribute


class SpecGroup(Base):
    """Specification group for product attributes."""
    
    __tablename__ = "spec_group"
    __table_args__ = (
        Index("ix_spec_group_category", "category"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    attributes: Mapped[List["SpecAttribute"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
