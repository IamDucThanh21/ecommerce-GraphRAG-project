"""Data definitions for ecom_discuss.

Define DTOs, events, and state schemas here. Left empty for user to implement.
"""

from typing import Optional
from fluvius.data import DataModel, UUID_TYPE
from pydantic import Field

from .types import ReactionTypeEnum, ResourceTypeEnum

# ── Comment ──────────────────────────────────────────────────────────

class CreateCommentData(DataModel):
    """Create a comment on a product or post. Tags only apply when
    resource_type='product' and are bundled in the same call."""

    resource_type: str = Field(
        default=ResourceTypeEnum.PRODUCT.value, description="Type of resource being commented on (product, post).", 
    )
    resource_id: UUID_TYPE = Field(
        ..., description="ID of the product/post being commented on."
    )
    content: str = Field(..., description="Comment text.", min_length=1)
    star: Optional[int] = Field(
        None,
        description="Star rating 1-5. Only allowed when resource_type='product'.",
        ge=1,
        le=5,
    )
    tag_option_ids: Optional[list[UUID_TYPE]] = Field(
        None,
        description="Selected review tag option IDs (product reviews only).",
    )


class ReplyCommentData(DataModel):
    """Admin reply to an existing top-level comment."""

    parent_id: UUID_TYPE = Field(..., description="ID of the comment being replied to.")
    content: str = Field(..., description="Reply text.", min_length=1)


class UpdateCommentData(DataModel):
    """Update own comment content/star (not allowed on admin replies)."""

    content: Optional[str] = Field(None, min_length=1)
    star: Optional[int] = Field(None, ge=1, le=5)
    tag_option_ids: Optional[list[UUID_TYPE]] = Field(
        None, description="Replace tag selections with this set."
    )


class DeleteCommentData(DataModel):
    """Soft-delete a comment (and its replies via cascade)."""
    pass


# ── Comment Reaction ─────────────────────────────────────────────────

class ReactToCommentData(DataModel):
    """React to a comment. One reaction per user per comment;
    calling again with a different type replaces the previous one."""

    comment_id: UUID_TYPE = Field(..., description="Comment being reacted to.")
    reaction_type: ReactionTypeEnum = Field(..., description="Type of reaction.")


class RemoveReactionData(DataModel):
    """Remove the caller's reaction from a comment."""

    comment_id: UUID_TYPE = Field(..., description="Comment to remove reaction from.")


# ── Review Tag Group (admin) ────────────────────────────────────────

class CreateReviewTagGroupData(DataModel):
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: Optional[int] = Field(0, description="Display order.")
    category_id: UUID_TYPE = Field(..., description="Comment to remove reaction from.")


class UpdateReviewTagGroupData(DataModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sort_order: Optional[int] = None


class DeleteReviewTagGroupData(DataModel):
    pass


# ── Review Tag Option (admin) ───────────────────────────────────────

class CreateReviewTagOptionData(DataModel):
    group_id: UUID_TYPE = Field(..., description="Parent tag group.")
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: Optional[int] = Field(0, description="Display order.")


class UpdateReviewTagOptionData(DataModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sort_order: Optional[int] = None


class DeleteReviewTagOptionData(DataModel):
    pass