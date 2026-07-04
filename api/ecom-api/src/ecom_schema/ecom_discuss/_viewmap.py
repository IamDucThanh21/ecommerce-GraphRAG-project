# """View mapping for ecom_discuss.

# Exposes a minimal VIEW_MAP used by view utilities. Only comment is
# currently provided; add more mappings as features are added.
# """

from __future__ import annotations

from typing import List, Optional
from sqlalchemy import ARRAY, Boolean, DateTime, Float, Integer, JSON, String, Text, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from . import SCHEMA, ViewBase
from .types import ResourceTypeEnum
import enum


class CommentDetailView(ViewBase):
    __tablename__ = "_comment_detail"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    resource_type: Mapped[Optional[ResourceTypeEnum]] = mapped_column(
        SQLEnum(
            ResourceTypeEnum,
            name="resourcetypeenum",
            schema=SCHEMA
        )
    )
    resource_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    name_user: Mapped[Optional[str]] = mapped_column(String(255))
    parent_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)
    star: Mapped[Optional[int]] = mapped_column(Integer)
    reply_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reaction_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reaction_summary: Mapped[Optional[dict]] = mapped_column(JSONB)
    tags: Mapped[Optional[list]] = mapped_column(JSONB)

class ReviewTagOptionListView(ViewBase):
    __tablename__ = "_review_tag_option_list"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    _created: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _updated: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _creator: Mapped[Optional[str]] = mapped_column(String(255))
    _updater: Mapped[Optional[str]] = mapped_column(String(255))
    _deleted: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    _etag: Mapped[Optional[str]] = mapped_column(String(64))
    _realm: Mapped[Optional[str]] = mapped_column(String(255))
    group_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    option_name: Mapped[Optional[str]] = mapped_column(String(100))
    option_sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    group_name: Mapped[Optional[str]] = mapped_column(String(100))
    group_sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))

class CommentSummaryView(ViewBase):
    __tablename__ = "_comment_summary"
    __table_args__ = {"schema": SCHEMA, "info": {"is_view": True}}

    _id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    resource_type: Mapped[Optional[str]] = mapped_column(String(50))
    num_comments: Mapped[int] = mapped_column(Integer, nullable=False)
    average_star: Mapped[Optional[float]] = mapped_column(Numeric(4, 2))
    groups: Mapped[Optional[list]] = mapped_column(JSONB)