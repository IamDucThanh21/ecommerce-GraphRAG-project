from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

from pydantic import BaseModel, Field
from sqlalchemy import (
    CheckConstraint,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
    Enum as SQLEnum,
    UniqueConstraint,
    text,
    create_engine,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .types import ResourceTypeEnum, ReactionTypeEnum

from . import Base

SCHEMA = "ecom_discuss"

class Comment(Base):
    """
    Generic comment, attachable to any resource (product, post, ...).
    `star` is only meaningful when resource_type = 'product'.
    """

    __tablename__ = "comment"
    __table_args__ = (
        CheckConstraint("star IS NULL OR (star >= 1 AND star <= 5)", name="ck_comment_star"),
        CheckConstraint("depth >= 0 AND depth <= 1", name="ck_comment_depth"),
        Index("idx_comment_resource", "resource_type", "resource_id"),
        Index("idx_comment_parent", "parent_id"),
        Index("idx_comment_user", "user_id"),
        {"schema": SCHEMA},
    )

    resource_type: Mapped[ResourceTypeEnum] = mapped_column(
        SQLEnum(ResourceTypeEnum, name="resourcetypeenum", schema=SCHEMA),
        nullable=False,
    )
    resource_id: Mapped[setattr] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    user_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,  # nullable: admin reply has no end-user
    )

    name_user: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.comment._id", ondelete="CASCADE"),
        nullable=True,
    )
    depth: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Only set when resource_type = 'product'
    star: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships
    replies: Mapped[list[Comment]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys=[parent_id],
    )
    parent: Mapped[Optional[Comment]] = relationship(
        "Comment",
        back_populates="replies",
        remote_side="Comment._id",
        foreign_keys=[parent_id],
    )
    reactions: Mapped[list[CommentReaction]] = relationship(
        "CommentReaction",
        back_populates="comment",
        cascade="all, delete-orphan",
    )


class CommentReaction(Base):
    """
    Reactions on a comment (like, love, haha, sad, ...).
    Generic — applies regardless of the comment's resource_type.
    """

    __tablename__ = "comment_reaction"
    __table_args__ = (
        UniqueConstraint("comment_id", "user_id", name="uq_comment_reaction_user"),
        Index("idx_comment_reaction_comment", "comment_id"),
        Index("idx_comment_reaction_user", "user_id"),
        {"schema": SCHEMA},
    )

    comment_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.comment._id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    reaction_type: Mapped[ReactionTypeEnum] = mapped_column(
        SQLEnum(ReactionTypeEnum, name="reactiontypeenum", schema=SCHEMA),
        nullable=False,
    )

    comment: Mapped[Comment] = relationship("Comment", back_populates="reactions")

class ReviewTagGroup(Base):
    """Admin-defined category, e.g. 'Hiệu năng', 'Thời lượng pin'."""

    __tablename__ = "review_tag_group"
    __table_args__ = (
        Index("idx_review_tag_group_category", "category_id"),
        {"schema": SCHEMA},
    )


    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

    # Cross-schema reference (ecom_product.product_category) — no DB-level
    # FK constraint since ecom_discuss and ecom_product are separate
    # bounded contexts. Integrity enforced at the application/service layer.
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    options: Mapped[list[ReviewTagOption]] = relationship(
        "ReviewTagOption",
        back_populates="group",
        cascade="all, delete-orphan",
    )

class ReviewTagOption(Base):
    """Admin-defined option within a group, e.g. 'Siêu mạnh mẽ', 'Yếu'."""

    __tablename__ = "review_tag_option"
    __table_args__ = (
        Index("idx_review_tag_option_group", "group_id"),
        {"schema": SCHEMA},
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.review_tag_group._id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

    group: Mapped[ReviewTagGroup] = relationship(
        "ReviewTagGroup", back_populates="options"
    )

class CustomerReviewTag(Base):
    """
    Maps a user's selected tag option to a comment.
    review_id points to comment._id (same schema, resource_type='product').
    """

    __tablename__ = "customer_review_tag"
    __table_args__ = (
        UniqueConstraint("review_id", "option_id", name="uq_review_tag"),
        Index("idx_customer_review_tag_review", "review_id"),
        {"schema": SCHEMA},
    )

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.comment._id", ondelete="CASCADE"),
        nullable=False,
    )
    option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.review_tag_option._id", ondelete="CASCADE"),
        nullable=False,
    )

    comment: Mapped["Comment"] = relationship("Comment")