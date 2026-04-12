"""SQLAlchemy ORM and DB connector for product_domain."""

from __future__ import annotations

from datetime import time
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import Enum, ForeignKey, Index, Integer, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_product"

class ProductCategory(Base):
    __tablename__ = "product_category"

    name : Mapped[str] = mapped_column(String(255), nullable=False)
    description : Mapped[str] = mapped_column(String(255), nullable=True)
