"""SQLAlchemy ORM for ecom_message message domain."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Integer, Index, String, Text, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import MessageRoleEnum, MessageIntentEnum

SCHEMA = "ecom_message"

if TYPE_CHECKING:
    from .conversation import Conversation
    from .chat_recommendation import Recommendation


# class Message(Base):
#     """Message table for conversation history."""
    
#     __tablename__ = "message"
#     __table_args__ = (
#         Index("ix_message_conversation_id", "conversation_id"),
#         Index("ix_message_created_at", "created_at"),
#     )

#     conversation_id: Mapped[str] = mapped_column(
#         UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.conversation._id"), nullable=False
#     )
#     role: Mapped[str] = mapped_column(String(50), nullable=False)  # USER, AI, SYSTEM
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     message_type: Mapped[str] = mapped_column(String(50), nullable=True)
#     status: Mapped[str] = mapped_column(String(50), nullable=True)
#     # metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), nullable=False, server_default=sa.func.now()
#     )

#     conversation: Mapped["Conversation"] = relationship(back_populates="messages")

class Message(Base):
    """Entity within the Conversation aggregate.
 
    Always accessed through its parent ``Conversation`` aggregate root.
    Captures both user utterances and assistant replies with intent tagging.
    """
 
    __tablename__ = "message"
    __table_args__ = {"schema": SCHEMA}
 
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.conversation._id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Ordering of messages within a conversation",
    )
    role: Mapped[MessageRoleEnum] = mapped_column(
        SQLEnum(
            MessageRoleEnum,
            name="messageroleenum",
            schema=SCHEMA,
            native_enum=True,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="Raw text content of the message",
    )
    intent: Mapped[Optional[MessageIntentEnum]] = mapped_column(
        SQLEnum(
            MessageIntentEnum,
            name="messageintentenum",
            schema=SCHEMA,
            native_enum=True,
            values_callable=lambda e: [x.value for x in e],
        ),
        comment="Classified intent — only populated for user role messages",
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")
    recommendation: Mapped[Optional["Recommendation"]] = relationship(
        back_populates="message",
        uselist=False,
        cascade="all, delete-orphan",
    )