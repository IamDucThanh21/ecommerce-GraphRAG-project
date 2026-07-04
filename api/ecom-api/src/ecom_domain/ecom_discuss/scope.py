from pydantic import BaseModel
from fluvius.query.field import UUIDField, StringField, EnumField
from fluvius.data import UUID_TYPE
from .types import ResourceTypeEnum


class CommentScopeSchema(BaseModel):
    resource_type: str = StringField("Resource")
    resource_id: UUID_TYPE = UUIDField("Resource ID")

class CategoryIdScope(BaseModel):
    category_id: UUID_TYPE = UUIDField("Category ID")
    
class GroupTagIdScope(BaseModel):
    group_id: UUID_TYPE = UUIDField("Group ID")
