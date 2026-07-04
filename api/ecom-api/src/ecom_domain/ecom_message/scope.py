from pydantic import BaseModel
from fluvius.query.field import UUIDField
from fluvius.data import UUID_TYPE

class ConversationIdScope(BaseModel):
    conversation_id: UUID_TYPE = UUIDField("Conversation ID")