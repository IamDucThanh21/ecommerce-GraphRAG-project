from fluvius.query import DomainQueryManager, DomainQueryResource
from fluvius.data import UUID_TYPE
from fluvius.query.field import (
    StringField, BooleanField, DateField, UUIDField, PrimaryID, EnumField,
    ArrayField, IntegerField, JSONField, FloatField, DatetimeField, DateField
)
from typing import Optional, Dict, Any

from .state import ECOMMessageStateManager
from .domain import ECOMMessageServiceDomain
import uuid

from .types import ConversationStatusEnum,MessageRoleEnum
from . import scope
class ECOMMessageQueryManager(DomainQueryManager):
    """Query manager for ECOM Client service, handling query operations"""

    __data_manager__ = ECOMMessageStateManager

    class Meta(DomainQueryResource.Meta):
        prefix = ECOMMessageServiceDomain.Meta.namespace
        tags = ECOMMessageServiceDomain.Meta.tags

resource = ECOMMessageQueryManager.register_resource
endpoint = ECOMMessageQueryManager.register_endpoint

@resource("conversation-list")
class CategoryBrandListQuery(DomainQueryResource):

    @classmethod
    def base_query(cls, context, scope):
        profile_id = context.profile._id
        return {
            "user_id": profile_id,
        }

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = False

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater', 'user_id')

        backend_model = "conversation"
        default_order = ("_created.desc",)

    user_id: UUID_TYPE = UUIDField("Message ID", source="user_id")
    title: Optional[str] = StringField("Brand Name", source="title")
    status: Optional[ConversationStatusEnum] = EnumField("Conversation status", enum=ConversationStatusEnum)


@resource("Message")
class CategoryBrandListQuery(DomainQueryResource):

    @classmethod
    def base_query(cls, context, scope):
        # profile_id = context.profile._id
        return {
            "conversation_id": scope["conversation_id"],
            # "user_id": profile_id,
        }

    class Meta(DomainQueryResource.Meta):
        include_all = False
        allow_meta_view = True
        allow_item_view = True
        allow_list_view = True
        allow_text_search = False
        scope_required=scope.ConversationIdScope

        excluded_fields = ('_creator', '_deleted', '_etag', '_updater')

        backend_model = "message"
        default_order = ("sequence_number.desc",)

    conversation_id: UUID_TYPE = UUIDField("Conversation ID", source="conversation_id")
    role: Optional[MessageRoleEnum] = EnumField("Role", enum=MessageRoleEnum)
    content: Optional[str] = StringField("Content", source="content")
    sequence_number: Optional[int] = IntegerField("Sequence number", source="sequence_number")

