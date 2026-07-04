"""SQLAlchemy ORM for ecom_message conversation domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Index, String, Integer, Text, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .types import ConversationStatusEnum

SCHEMA = "ecom_message"

if TYPE_CHECKING:
    from .message import Message
    from .chat_recommendation import ConversationContextSnapshot


# class Conversation(Base):
#     """Conversation table for AI messaging."""
    
#     __tablename__ = "conversation"
#     __table_args__ = (
#         Index("ix_conversation_user_id", "user_id"),
#         Index("ix_conversation_created_at", "created_at"),
#     )

#     user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), nullable=True)
#     session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), nullable=False, server_default=sa.func.now()
#     )

#     messages: Mapped[List["Message"]] = relationship(
#         back_populates="conversation", cascade="all, delete-orphan"
#     )

class Conversation(Base):
    """Aggregate root for the conversation bounded context.
 
    Owns all messages and context snapshots within a conversation thread.
    Tracks lifecycle status and uses optimistic locking via ``version``.
    """
 
    __tablename__ = "conversation"
    __table_args__ = {"schema": SCHEMA}
 
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Reference to identity context — no FK across bounded contexts",
    )
    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        comment="Auto-generated from first message snippet or user-renamed",
    )
    status: Mapped[ConversationStatusEnum] = mapped_column(
        SQLEnum(
            ConversationStatusEnum,
            name="conversationstatusenum",
            schema=SCHEMA,
            native_enum=True,
            values_callable=lambda e: [x.value for x in e],
        ),
        default=ConversationStatusEnum.ACTIVE,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Optimistic locking — increment on each state change",
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.sequence_number",
    )
    context_snapshots: Mapped[List["ConversationContextSnapshot"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )