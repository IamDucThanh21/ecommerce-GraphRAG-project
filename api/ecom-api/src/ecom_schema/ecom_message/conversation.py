"""SQLAlchemy ORM for ecom_message conversation domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_message"

if TYPE_CHECKING:
    from .message import Message


class Conversation(Base):
    """Conversation table for AI messaging."""
    
    __tablename__ = "conversation"
    __table_args__ = (
        Index("ix_conversation_user_id", "user_id"),
        Index("ix_conversation_created_at", "created_at"),
    )

    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )
