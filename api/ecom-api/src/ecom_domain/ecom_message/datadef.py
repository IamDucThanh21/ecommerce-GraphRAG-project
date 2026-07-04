from typing import Optional
from fluvius.data import DataModel
from pydantic import Field


# ── Conversation ──────────────────────────────────────────────────────────────

class CreateConversationData(DataModel):
    """Data model for creating a new conversation."""

    title: Optional[str] = Field(
        None,
        description="Optional title. Auto-generated if not provided.",
        max_length=255,
    )


class UpdateConversationData(DataModel):
    """Data model for updating a conversation."""

    title: Optional[str] = Field(
        None,
        description="New title for the conversation.",
        max_length=255,
    )


class DeleteConversationData(DataModel):
    """Data model for deleting (archiving) a conversation."""

    conversation_id: str = Field(..., description="ID of the conversation to delete.")


class GetConversationData(DataModel):
    """Data model for retrieving a single conversation."""

    conversation_id: str = Field(..., description="ID of the conversation to retrieve.")


# ── Message ───────────────────────────────────────────────────────────────────

class SendMessageData(DataModel):
    """Data model for sending a user message in a conversation."""
    
    content: str = Field(..., description="Message content from the user.", min_length=1)


class GetMessagesData(DataModel):
    """Data model for retrieving messages in a conversation."""

    conversation_id: str = Field(..., description="ID of the conversation.")