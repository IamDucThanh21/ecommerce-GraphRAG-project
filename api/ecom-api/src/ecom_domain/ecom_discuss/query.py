from typing import List, Optional
from pydantic import BaseModel
from fluvius.data import UUID_TYPE
from fluvius.query import DomainQueryManager, DomainQueryResource, endpoint
from .state import ECOMDiscussStateManager
from .domain import ECOMDiscussServiceDomain
from fluvius.query.field import (
    StringField,
    UUIDField,
    IntegerField,
    DictField,
    BooleanField,
    JSONField,
    EnumField,
    FloatField
)
from . import scope
from .types import ResourceTypeEnum


class ECOMDiscussQueryManager(DomainQueryManager):
    """Query manager for ECOM Discuss domain (scaffold).

    Add resources/endpoints in this module as needed.
    """

    __data_manager__ = ECOMDiscussStateManager

    class Meta(DomainQueryManager.Meta):
        prefix = ECOMDiscussServiceDomain.Meta.namespace
        tags = ECOMDiscussServiceDomain.Meta.tags


resource = ECOMDiscussQueryManager.register_resource
endpoint = ECOMDiscussQueryManager.register_endpoint


# ── Comment ──────────────────────────────────────────────────────────

@resource("comment-detail")
class CommentDetailQuery(DomainQueryResource):

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        auth_required = False

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_comment_detail"
        scope_required = scope.CommentScopeSchema

    resource_type: Optional[str] = StringField("Resource Type", source="resource_type")
    resource_id: Optional[str] = StringField("Resource ID", source="resource_id")
    user_id: Optional[str] = StringField("User ID", source="user_id")
    name_user: Optional[str] = StringField("Name of User", source="name_user")
    parent_id: Optional[str] = StringField("Parent Comment ID", source="parent_id")
    depth: Optional[int] = IntegerField("Depth", source="depth")
    content: Optional[str] = StringField("Content", source="content")
    star: Optional[int] = IntegerField("Star Rating", source="star")
    reply_count: Optional[int] = IntegerField("Reply Count", source="reply_count")
    reaction_count: Optional[int] = IntegerField("Reaction Count", source="reaction_count")
    reaction_summary: Optional[dict] = JSONField("Reaction Summary", source="reaction_summary")
    tags: Optional[list] = JSONField("Tags", source="tags")


# ── Review Tag Group ─────────────────────────────────────────────────

@resource("review-tag-group")
class ReviewTagGroupQuery(DomainQueryResource):

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True
        auth_required = False

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        scope_required = scope.CategoryIdScope
        backend_model = "review_tag_group"

    name: Optional[str] = StringField("Group Name", source="name")
    sort_order: Optional[int] = IntegerField("Sort Order", source="sort_order")
    category_id: Optional[str] = StringField("Category ID", source="category_id")


# ── Review Tag Option ─────────────────────────────────────────────────

@resource("review-tag-option-list")
class ReviewTagOptionListQuery(DomainQueryResource):

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = True
        auth_required = False

        scope_required = scope.GroupTagIdScope
        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "_review_tag_option_list"

    group_id: Optional[str] = StringField("Group ID", source="group_id")
    option_name: Optional[str] = StringField("Option Name", source="option_name")
    option_sort_order: Optional[int] = IntegerField("Option Sort Order", source="option_sort_order")
    group_name: Optional[str] = StringField("Group Name", source="group_name")
    group_sort_order: Optional[int] = IntegerField("Group Sort Order", source="group_sort_order")
    category_id: Optional[str] = StringField("Category ID", source="category_id")

# ── Comment summary ─────────────────────────────────────────────────

@resource("comment-summary")
class CommentSummaryQuery(DomainQueryResource):

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = False
        allow_item_view = True
        allow_list_view = True
        allow_text_search = False
        auth_required = False
        excluded_fields = ('_creator', '_deleted', '_etag', '_updater', '_created', '_updated', '_realm')

        backend_model = "_comment_summary"

    resource_type: Optional[str] = StringField("Resource Type", source="resource_type")
    num_comments: Optional[int] = IntegerField("Number of Comments", source="num_comments")
    average_star: Optional[float] = FloatField("Average Star", source="average_star")
    groups: Optional[list] = JSONField("Tag Group Stats", source="groups")