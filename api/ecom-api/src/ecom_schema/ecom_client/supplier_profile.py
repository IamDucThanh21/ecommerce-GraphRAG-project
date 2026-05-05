"""SQLAlchemy ORM for ecom_client supplier profile domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
import uuid

import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_client"

class SupplierProfile(Base):
    """Supplier profile information."""

    __tablename__ = "supplier_profile"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.profile._id"), nullable=False, unique=True
    )
    business_name: Mapped[Optional[str]] = mapped_column(String(255))
    business_address: Mapped[Optional[str]] = mapped_column(String(1024))
    tax_id: Mapped[Optional[str]] = mapped_column(String(255))
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationship back to profile
    profile = relationship("Profile", back_populates="supplier_profile")