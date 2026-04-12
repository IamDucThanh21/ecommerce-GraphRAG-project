"""SQLAlchemy ORM for ecom_product product_spec_flat domain."""

from __future__ import annotations

from typing import Any, Dict, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

SCHEMA = "ecom_product"


class ProductSpecFlat(Base):
    """Flattened product specifications (cached for performance)."""
    
    __tablename__ = "product_spec_flat"

    product_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    specs_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
