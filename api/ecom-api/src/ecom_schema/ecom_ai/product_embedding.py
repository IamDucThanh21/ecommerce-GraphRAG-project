"""SQLAlchemy ORM for ecom_ai product_embedding domain."""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

SCHEMA = "ecom_ai"


class ProductEmbedding(Base):
    """Product embeddings for AI/semantic search."""
    
    __tablename__ = "product_embedding"

    product_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    embedding: Mapped[bytes] = mapped_column(nullable=False)  # Vector stored as bytea
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
