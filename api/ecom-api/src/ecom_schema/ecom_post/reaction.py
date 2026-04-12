"""SQLAlchemy ORM for ecom_content reaction domain."""

from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlalchemy import String, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

SCHEMA = "ecom_post"


class Reaction(Base):
    """User reactions to posts and comments."""
    
    __tablename__ = "reaction"
    __table_args__ = (
        Index("ix_reaction_user_id", "user_id"),
        Index("ix_reaction_post_id", "post_id"),
        Index("ix_reaction_comment_id", "comment_id"),
    )

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    post_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.post._id"), nullable=True
    )
    comment_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.comment._id"), nullable=True
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # LIKE, LOVE, HAHA, WOW, SAD, ANGRY
