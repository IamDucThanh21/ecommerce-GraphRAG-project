"""SQLAlchemy ORM for specification attribute template (per group template)."""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Integer, Boolean, Index, ForeignKey, UniqueConstraint, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import SpecDataTypeEnum

SCHEMA = "ecom_product"

if TYPE_CHECKING:
    from .spec_group_template import SpecGroupTemplate
    from .product_spec_value import ProductSpecValue


class SpecAttributeTemplate(Base):
    """Specification attribute template. Defines the structure, type, and filterability of a spec attribute per group."""
    
    __tablename__ = "spec_attribute_template"
    __table_args__ = (
        UniqueConstraint("group_template_id", "key", name="uq_spec_attribute_template_group_key"),
        Index("ix_spec_attribute_template_group_id", "group_template_id"),
    )

    group_template_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.spec_group_template._id"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    data_type: Mapped[SpecDataTypeEnum] = mapped_column(
        SAEnum(SpecDataTypeEnum, name="specdatatypeenum", schema=SCHEMA),
        nullable=False
    )
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_filterable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    group_template: Mapped["SpecGroupTemplate"] = relationship(back_populates="attribute_templates")
    spec_values: Mapped[List["ProductSpecValue"]] = relationship(
        back_populates="attribute_template", cascade="all, delete-orphan"
    )
