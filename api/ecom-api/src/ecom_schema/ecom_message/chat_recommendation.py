"""SQLAlchemy ORM for ecom_message conversation domain."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Index, String, Integer, Float, Text, Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .types import RecommendationStrategyEnum, FeedbackActionEnum

from . import Base
from .types import MessageRoleEnum, MessageIntentEnum

SCHEMA = "ecom_message"

if TYPE_CHECKING:
    from .conversation import Conversation
    from .message import Message

class ConversationContextSnapshot(Base):
    """Value object — summarized conversation context at a point in time.
 
    Replaces ``message_filters``. Stores the AI-extracted intent, constraints,
    and preferences from the conversation so far, used to guide product search.
    Treated as a value object: replaced as a whole, never partially updated.
    """
 
    __tablename__ = "conversation_context_snapshot"
    __table_args__ = {"schema": SCHEMA}
 
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.conversation._id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Product category extracted from context e.g. mobile, laptop",
        nullable=True,
    )
    use_case: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Intended use case e.g. gaming, photography, business",
        nullable=True,
    )
    budget_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    budget_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), default="USD", nullable=True)
    preferred_brands: Mapped[Optional[list]] = mapped_column(
        ARRAY(String),
        comment="e.g. ['Samsung', 'Apple']", nullable=True
    )
    other_filters: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        comment="Flexible extra constraints e.g. {os: 'Android', screen_size: '6inch+'}", nullable=True
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    conversation: Mapped["Conversation"] = relationship(
        back_populates="context_snapshots"
    )

class Recommendation(Base):
    """Aggregate root for the recommendation bounded context.
 
    Created once per assistant message that returns product suggestions.
    ``strategy`` records which matching algorithm produced this recommendation.
    """
 
    __tablename__ = "recommendation"
    __table_args__ = {"schema": SCHEMA}
 
    message_id: Mapped[RecommendationStrategyEnum] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.message._id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        comment="The assistant message that delivered this recommendation",
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Denormalized for fast conversation-level queries",
    )
    strategy: Mapped[RecommendationStrategyEnum] = mapped_column(
        SQLEnum(
            RecommendationStrategyEnum,
            name="recommendationstrategyenum",
            schema=SCHEMA,
            native_enum=True,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    message: Mapped["Message"] = relationship(back_populates="recommendation")
    items: Mapped[List["RecommendationItem"]] = relationship(
        back_populates="recommendation",
        cascade="all, delete-orphan",
        order_by="RecommendationItem.rank",
    )
 
 
class RecommendationItem(Base):
    """Entity within the Recommendation aggregate.
 
    Each row is one product suggestion with its relevance score and
    human-readable reason surfaced to the user.
    """
 
    __tablename__ = "recommendation_item"
    __table_args__ = {"schema": SCHEMA}
 
    recommendation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.recommendation._id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="1 = top pick within this recommendation",
    )
    score: Mapped[Optional[float]] = mapped_column(
        Float,
        comment="Relevance score from 0.0 to 1.0",
    )
    reason: Mapped[Optional[str]] = mapped_column(
        Text,
        comment='Explanation shown to user e.g. "Matches gaming use case, within $500 budget"',
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    recommendation: Mapped["Recommendation"] = relationship(back_populates="items")
    feedback: Mapped[List["RecommendationFeedback"]] = relationship(
        back_populates="recommendation_item",
        cascade="all, delete-orphan",
    )
 
 
class RecommendationFeedback(Base):
    """Records user reactions to individual recommendation items.
 
    Immutable event-style rows — never updated, only inserted.
    Used to improve future recommendation quality.
    """
 
    __tablename__ = "recommendation_feedback"
    __table_args__ = {"schema": SCHEMA}
 
    recommendation_item_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.recommendation_item._id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="Reference to identity context — no FK across bounded contexts",
    )
    action: Mapped[FeedbackActionEnum] = mapped_column(
        SQLEnum(
            FeedbackActionEnum,
            name="feedbackactionenum",
            schema=SCHEMA,
            native_enum=True,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
 
    # ── relationships ────────────────────────────────────────────────────────
    recommendation_item: Mapped["RecommendationItem"] = relationship(
        back_populates="feedback"
    )