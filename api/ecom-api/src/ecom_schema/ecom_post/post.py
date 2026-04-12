"""SQLAlchemy ORM for ecom_content post domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import String, Text, DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_post"

if TYPE_CHECKING:
    from .comment import Comment


class Post(Base):
    """Content posts."""
    
    __tablename__ = "post"
    __table_args__ = (
        Index("ix_post_author_id", "author_id"),
        Index("ix_post_created_at", "created_at"),
    )

    author_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
