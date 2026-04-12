"""SQLAlchemy ORM for ecom_message message domain."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, String, Text, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

SCHEMA = "ecom_message"

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(Base):
    """Message table for conversation history."""
    
    __tablename__ = "message"
    __table_args__ = (
        Index("ix_message_conversation_id", "conversation_id"),
        Index("ix_message_created_at", "created_at"),
    )

    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.conversation._id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # USER, AI, SYSTEM
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
    # metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")
