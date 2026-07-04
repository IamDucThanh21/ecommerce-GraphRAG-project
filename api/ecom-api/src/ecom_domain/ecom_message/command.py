from fluvius.data import serialize_mapping, UUID_GENR
from .domain import ECOMMessageServiceDomain

from . import datadef
from . import config, logger

Command = ECOMMessageServiceDomain.Command

class CreateConversationCommand(Command):
    """Create a new conversation for the authenticated user."""
 
    Data = datadef.CreateConversationData
 
    class Meta:
        key = "create-conversation"
        description = "Create a new conversation thread."
        resource_init = True
        resources = ("conversation",)
        tags = ["chat", "conversation"]
        auth_required = True
        policy_required = False
 
    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id
 
        result = await agg.create_conversation(data=data, user_id=user_id)
 
        yield agg.create_response(
            serialize_mapping(result),
            _type="conversation-service-response",
        )

class UpdateConversationCommand(Command):
    """Update a conversation's title."""
 
    Data = datadef.UpdateConversationData
 
    class Meta:
        key = "update-conversation"
        description = "Update a conversation's title."
        resources = ("conversation",)
        tags = ["chat", "conversation"]
        auth_required = True
        policy_required = False
 
    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id
        conversation_id = agg.get_aggroot().identifier
 
        result = await agg.update_conversation(
            conversation_id = conversation_id,
            user_id=user_id,
            data=data,
        )
 
        yield agg.create_response(
            serialize_mapping(result),
            _type="conversation-service-response",
        )
 
 
class DeleteConversationCommand(Command):
    """Soft-delete (archive) a conversation."""

    class Meta:
        key = "delete-conversation"
        description = "Archive a conversation (soft delete)."
        resources = ("conversation",)
        tags = ["chat", "conversation"]
        auth_required = True
        policy_required = False
 
    async def _process(self, agg, stm, payload):
        user_id = agg.get_context().user_id
        conversation_id = agg.get_aggroot().identifier

        await agg.delete_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )
 
 
# ── Message ───────────────────────────────────────────────────────────────────
 
class SendMessageCommand(Command):
    """Send a user message and receive a bot reply."""
 
    Data = datadef.SendMessageData
 
    class Meta:
        key = "send-message"
        description = "Send a user message and get a bot response."
        resources = ("conversation",)
        tags = ["send", "message"]
        auth_required = True
        policy_required = False
 
    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id
        conversation_id = agg.get_aggroot().identifier

        print(user_id)
        print(conversation_id)
        # Step 1: save user message
        user_message = await agg.save_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=data["content"],
        )

        # Step 2: generate and save bot reply
        result = await agg.save_bot_reply(
            conversation_id=conversation_id,
            sequence_number=user_message.sequence_number + 1,
            user_content=data["content"],
        )

        bot_message = result['message']
        product_ids = result['product_ids']
 
        yield agg.create_response(
            serialize_mapping({
                "user_message": user_message,
                "bot_message": bot_message,
                "product_ids": product_ids,
            }),
            _type="message-service-response",
        )
