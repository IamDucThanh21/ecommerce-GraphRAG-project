"""SQLAlchemy ORM for ecom_cart discount domain."""

from __future__ import annotations

from decimal import Decimal
from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Numeric, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

SCHEMA = "ecom_cart"


class Discount(Base):
    """Discount codes."""
    
    __tablename__ = "discount"
    __table_args__ = (
        Index("ix_discount_code", "code"),
    )

    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # PERCENTAGE, FIXED, BOGO
    value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    max_discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    min_order_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
