"""SQLAlchemy ORM for ecom_content comment domain."""

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
    from .post import Post


class Comment(Base):
    """Comments on posts."""
    
    __tablename__ = "comment"
    __table_args__ = (
        Index("ix_comment_post_id", "post_id"),
        Index("ix_comment_author_id", "author_id"),
        Index("ix_comment_parent_id", "parent_id"),
        Index("ix_comment_created_at", "created_at"),
    )

    post_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.post._id"), nullable=False
    )
    author_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.comment._id"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    post: Mapped["Post"] = relationship(back_populates="comments")
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="parent", remote_side=[parent_id], cascade="all, delete-orphan"
    )
    parent: Mapped[Optional["Comment"]] = relationship(
        back_populates="replies", remote_side=[parent_id]
    )
