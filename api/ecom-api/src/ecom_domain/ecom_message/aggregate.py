from fluvius.domain.aggregate import Aggregate, action
from fluvius.data import serialize_mapping, UUID_GENR
from uuid import UUID
from fluvius.data.exceptions import ItemNotFoundError
from fluvius.error import BadRequestError, NotFoundError
from sqlalchemy import select, or_
from ..ecom_ai.service import ask_graph
import bcrypt
import jwt
import uuid
import re
from decimal import Decimal
import json

# from ecom_schema.ecom_client.user import User, UserIdentity, UserSession
# from ecom_schema.ecom_client.profile import Profile
from .types import ConversationStatusEnum, MessageRoleEnum, RecommendationStrategyEnum

from . import logger, config
from datetime import datetime, timezone, timedelta, date, time

class EcomMessageAggregate(Aggregate):

    async def create_conversation_context(self, conversation_id):
        conversation_context = self.init_resource(
            "conversation_context_snapshot",
            _id=UUID_GENR(),
            conversation_id=conversation_id
        )
        await self.statemgr.insert(conversation_context)

    @action("conversation-created", resources="conversation")
    async def create_conversation(self, *, data, user_id):
        """Create a new conversation for the authenticated user.
 
        If no title is provided, auto-generates one as "Đoạn chat N"
        where N is the total number of existing conversations + 1.
        """
        title = data.get("title")
        if not title:
            all_conversations = await self.statemgr.find_all(
                "conversation",
                where={"user_id": str(user_id), "_deleted": None}
            )
            title = f"Đoạn chat {len(all_conversations) + 1}"

        conversation_id = UUID_GENR()
 
        conversation = self.init_resource(
            "conversation",
            data,
            _id=conversation_id,
            user_id=user_id,
            status=ConversationStatusEnum.ACTIVE.value,
            version=1,
            title=title,
        )
        await self.statemgr.insert(conversation)

        # create conversation_context instantly
        await self.create_conversation_context(conversation_id=conversation_id)

        return conversation
 
    @action("conversations-fetched", resources="conversation")
    async def get_conversations(self, *, user_id):
        """Get all active conversations for the authenticated user."""
        conversations = await self.statemgr.find_many(
            "conversation",
            where={
                "user_id": str(user_id),
                "status": ConversationStatusEnum.ACTIVE.value,
                "_deleted": None,
            }
        )
        return {"conversations": conversations, "total": len(conversations)}
 
    @action("conversation-fetched", resources="conversation")
    async def get_conversation(self, *, conversation_id, user_id):
        """Get a single conversation, verifying ownership."""
        conversation = await self.statemgr.find_one(
            "conversation",
            where={"_id": str(conversation_id), "_deleted": None}
        )
        if not conversation:
            raise NotFoundError("CHAT.001", "Conversation not found.")
 
        if str(conversation.user_id) != str(user_id):
            raise BadRequestError("CHAT.002", "Access denied to this conversation.")
 
        return conversation
 
    @action("conversation-updated", resources="conversation")
    async def update_conversation(self, *, conversation_id, user_id, data):
        """Update a conversation's title, verifying ownership."""
        conversation = await self.statemgr.find_one(
            "conversation",
            where={"_id": conversation_id, "user_id": user_id, "_deleted": None}
        )
        if not conversation:
            raise NotFoundError("CHAT.001", "Conversation not found.")
 
        updated = await self.statemgr.update(conversation, title=data.get("title"), version=(conversation.version+1))
        
        return updated
 
    @action("conversation-deleted", resources="conversation")
    async def delete_conversation(self, *, conversation_id, user_id):
        """Soft-delete a conversation by setting status to deleted, verifying ownership."""
        conversation = await self.statemgr.find_one(
            "conversation",
            where={"_id": conversation_id, "user_id": user_id, "_deleted": None}
        )
        if not conversation:
            raise NotFoundError("CHAT.001", "Conversation not found.")
 
        await self.statemgr.invalidate(conversation)

        return conversation
 
    # ── Message ───────────────────────────────────────────────────────────────
 
    @action("user-message-saved", resources="conversation")
    async def save_user_message(self, *, conversation_id, user_id, content):
        """Save the user's message, verifying conversation ownership."""
        conversation = await self.statemgr.find_one(
            "conversation",
            where={"_id": conversation_id, "user_id": user_id, "_deleted": None}
        )
        print(conversation)
        if not conversation:
            raise NotFoundError("CHAT.001", "Conversation not found.")
 
        # Get next sequence number
        messages = await self.statemgr.find_all(
            "message",
            where={"conversation_id": conversation_id}
        )
        sequence_number = len(messages) + 1
 
        message = self.init_resource(
            "message",
            {},
            _id=UUID_GENR(),
            conversation_id=conversation_id,
            sequence_number=sequence_number,
            role=MessageRoleEnum.USER.value,
            content=content,
        )
        await self.statemgr.insert(message)
 
        # # Bump conversation version on each new message
        # await self.statemgr.update(
        #     "conversation",
        #     where={"_id": str(conversation_id)},
        #     data={"version": conversation.version + 1}
        # )
        return message

    def clean_response(self, text: str) -> str:
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    
    async def get_context_snapshot(self, conversation_id: UUID):
            """Lấy context snapshot hiện tại của conversation."""
            return await self.statemgr.find_one(
                "conversation_context_snapshot",
                where={"conversation_id": conversation_id, "_deleted": None}
            )


    async def save_context_snapshot(
        self,
        conversation_id: UUID,
        context: dict,
    ):
        """
        Merge context mới vào snapshot hiện tại và update.

        Rules:
        - budget_min: lấy min(cũ, mới)
        - budget_max: lấy max(cũ, mới)
        - preferred_brands: union, không trùng lặp
        - category / use_case / currency: lấy mới nếu có
        - other_filters: merge, ghi đè nếu giá trị mới != null
        """

        # ── parse context ────────────────────────────────────────────────────────
        if isinstance(context, str):
            context = json.loads(context)

        new_category         = context.get("category")
        new_use_cases        = context.get("use_cases") or []
        new_use_case         = ", ".join(new_use_cases) if new_use_cases else None
        new_budget_min       = context.get("budget_min")
        new_budget_max       = context.get("budget_max")
        new_currency         = context.get("currency")
        new_preferred_brands = context.get("preferred_brands") or []
        new_other_filters    = context.get("other_filters") or {}

        # ── lấy snapshot hiện tại ───────────────────────────────────────────────
        existing = await self.get_context_snapshot(conversation_id)

        # ── merge ────────────────────────────────────────────────────────────────
        old_min = existing.budget_min
        if new_budget_min is not None and old_min is not None:
            merged_budget_min = min(old_min, new_budget_min)
        else:
            merged_budget_min = new_budget_min if new_budget_min is not None else old_min

        old_max = existing.budget_max
        if new_budget_max is not None and old_max is not None:
            merged_budget_max = max(old_max, new_budget_max)
        else:
            merged_budget_max = new_budget_max if new_budget_max is not None else old_max

        old_brands    = existing.preferred_brands or []
        merged_brands = list(old_brands)
        for brand in new_preferred_brands:
            if brand not in merged_brands:
                merged_brands.append(brand)

        old_filters    = existing.other_filters or {}
        merged_filters = dict(old_filters)
        for key, val in new_other_filters.items():
            if val is not None:
                merged_filters[key] = val
            elif key not in merged_filters:
                merged_filters[key] = val

        # ── build data dict và update ────────────────────────────────────────────
        data = {
            "category":         new_category or existing.category,
            "use_case":         new_use_case or existing.use_case,
            "budget_min":       merged_budget_min,
            "budget_max":       merged_budget_max,
            "currency":         new_currency or existing.currency,
            "preferred_brands": merged_brands or None,
            "other_filters":    merged_filters,
        }

        await self.statemgr.update(existing, **data)
    
    def _snapshot_to_dict(self, snapshot) -> dict:
        """Convert ORM snapshot object sang dict để truyền vào ask_graph."""
        return {
            "category":         snapshot.category,
            "use_case":         snapshot.use_case,
            "budget_min":       snapshot.budget_min,
            "budget_max":       snapshot.budget_max,
            "currency":         snapshot.currency,
            "preferred_brands": snapshot.preferred_brands or [],
            "other_filters":    snapshot.other_filters or {},
        }

    @action("bot-reply-saved", resources="conversation")
    async def save_bot_reply(self, *, conversation_id, sequence_number, user_content):
        """Generate a stub bot reply and save it as an assistant message."""
        # NOTE: hardcoded stub — replace with chatbot API call later

        prior_context = await self.get_context_snapshot(conversation_id=conversation_id)
        prior_context_dict = self._snapshot_to_dict(prior_context)

        try:
            result = ask_graph(user_content, prior_context=prior_context_dict)
            bot_content = result["answer"]
            product_ids = result.get("product_ids", [])
            context = result["context"]
            cypher = result.get("cypher")

            answer = self.clean_response(bot_content)
            await self.save_context_snapshot(conversation_id=conversation_id, context=context)

        except Exception:
            bot_content = "Xin lỗi, tôi không thể trả lời ngay bây giờ."
            product_ids = []
            cypher = None

        # bot_content = "trả về cái này là oke nhé ae"
        print(cypher)
        message = self.init_resource(
            "message",
            {},
            _id=UUID_GENR(),
            conversation_id=conversation_id,
            sequence_number=sequence_number,
            role=MessageRoleEnum.ASSISTANT.value,
            content=answer,
        )
        await self.statemgr.insert(message)

        # Persist recommendation + recommendation_item rows (best-effort)
        if product_ids:
            try:
                recommendation = self.init_resource(
                    "recommendation",
                    {},
                    _id=UUID_GENR(),
                    message_id=message._id,
                    conversation_id=conversation_id,
                    strategy=RecommendationStrategyEnum.AI_RANKED.value,
                )
                await self.statemgr.insert(recommendation)
    
                for rank, product_id in enumerate(product_ids, start=1):
                    # print(f"product: {product_id}, type: {type(product_id)} and rank: {rank}")
                    item = self.init_resource(
                        "recommendation_item",
                        {},
                        _id=UUID_GENR(),
                        recommendation_id=recommendation._id,
                        product_id=product_id,
                        rank=rank,
                    )
                    await self.statemgr.insert(item)
            except Exception:
                logger.exception("Failed to persist recommendation items")

        return {'message': message, 
                'product_ids': product_ids}
