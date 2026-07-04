from fluvius.domain.aggregate import Aggregate, action
from fluvius.data import serialize_mapping, UUID_GENR
from .types import ReactionTypeEnum, ResourceTypeEnum


class ECOMDiscussAggregate(Aggregate):
    """Aggregate root handling comment, reaction, and tag operations."""

    # ── Comment ──────────────────────────────────────────────────

    @action("comment-created", resources="comment")
    async def create_comment(self, *, data, user_id):
        """Create a top-level comment. Validates star is only set for
        resource_type='product', and bundles tag selections if provided."""

        resource_type = data.get("resource_type")
        star = data.get("star")
        tag_option_ids = data.get("tag_option_ids") or []

        if star is not None and resource_type != ResourceTypeEnum.PRODUCT.value:
            raise ValueError("star rating is only allowed when resource_type='product'.")

        if tag_option_ids and resource_type != ResourceTypeEnum.PRODUCT.value:
            raise ValueError("tags are only allowed when resource_type='product'.")

        comment_id = UUID_GENR()

        comment = self.init_resource(
            "comment",
            data,
            _id=comment_id,
            user_id=user_id,
            parent_id=None,
            depth=0,
        )
        await self.statemgr.insert(comment)

        for option_id in tag_option_ids:
            await self._attach_tag(comment_id=comment_id, option_id=option_id)

        return comment

    @action("comment-replied", resources="comment")
    async def reply_comment(self, *, data, user_id):
        """Admin reply to an existing top-level comment. depth is forced
        to parent.depth + 1 (1, since only one reply level is supported)."""
        print("đã pass qua check admin")
        parent_id = data.get("parent_id")
        parent = await self.statemgr.find_one("comment", where={"_id": str(parent_id)})
        if parent is None:
            raise ValueError(f"Parent comment {parent_id} not found.")
        if parent.get("depth", 0) >= 1:
            raise ValueError("Replies are only supported on top-level comments.")

        reply_id = UUID_GENR()

        reply = self.init_resource(
            "comment",
            {"content": data.get("content")},
            _id=reply_id,
            resource_type=parent["resource_type"],
            resource_id=parent["resource_id"],
            user_id=user_id,  # TODO: confirm whether admin replies should store user_id or stay null
            parent_id=parent_id,
            depth=parent.get("depth", 0) + 1,
            star=None,
        )
        await self.statemgr.insert(reply)

        return reply

    @action("comment-updated", resources="comment")
    async def update_comment(self, *, comment_id, data, user_id):
        """Update own comment. Replaces tag selections if tag_option_ids provided."""

        comment = await self.statemgr.find_one("comment", where={"_id": str(comment_id)})
        if comment is None:
            raise ValueError(f"Comment {comment_id} not found.")
        if str(comment.get("user_id")) != str(user_id):
            raise PermissionError("You can only update your own comment.")

        update_fields = {
            k: v for k, v in data.items()
            if k in ("content", "star") and v is not None
        }
        if update_fields:
            comment = await self.statemgr.update(comment, **update_fields)

        tag_option_ids = data.get("tag_option_ids")
        if tag_option_ids is not None:
            await self._replace_tags(comment_id=comment_id, option_ids=tag_option_ids)

        return comment

    @action("comment-deleted", resources="comment")
    async def delete_comment(self, *, comment_id, user_id):
        """Soft-delete own comment. Replies cascade via DB FK."""

        comment = await self.statemgr.find_one("comment", where={"_id": str(comment_id)})
        if comment is None:
            raise ValueError(f"Comment {comment_id} not found.")
        if str(comment.get("user_id")) != str(user_id):
            raise PermissionError("You can only delete your own comment.")

        await self.statemgr.invalidate(comment)

        return comment

    # ── Comment Reaction ─────────────────────────────────────────

    @action("comment-reacted", resources="comment_reaction")
    async def react_to_comment(self, *, data, user_id):
        """Create or replace the caller's reaction on a comment."""

        comment_id = data.get("comment_id")
        reaction_type = data.get("reaction_type")

        existing = await self.statemgr.find_one(
            "comment_reaction",
            where={
                "comment_id": str(comment_id),
                "user_id": str(user_id),
                "_deleted": None,
            },
        )

        if existing is not None:
            updated = await self.statemgr.update(existing, reaction_type=reaction_type)
            return updated

        reaction_id = UUID_GENR()
        reaction = self.init_resource(
            "comment_reaction",
            data,
            _id=reaction_id,
            user_id=user_id,
        )
        await self.statemgr.insert(reaction)

        return reaction

    @action("comment-reaction-removed", resources="comment_reaction")
    async def remove_reaction(self, *, data, user_id):
        """Remove caller's reaction from a comment."""

        comment_id = data.get("comment_id")

        existing = await self.statemgr.find_one(
            "comment_reaction",
            where={
                "comment_id": str(comment_id),
                "user_id": str(user_id),
                "_deleted": None,
            },
        )
        if existing is None:
            raise ValueError("No existing reaction to remove.")

        await self.statemgr.invalidate(existing)

        return existing

    # ── Review Tag Group (admin) ────────────────────────────────

    @action("review-tag-group-created", resources="review_tag_group")
    async def create_review_tag_group(self, *, data):
        group_id = UUID_GENR()

        group = self.init_resource(
            "review_tag_group",
            data,
            _id=group_id,
        )
        await self.statemgr.insert(group)

        return group

    @action("review-tag-group-updated", resources="review_tag_group")
    async def update_review_tag_group(self, *, group_id, data):
        group = await self.statemgr.find_one(
            "review_tag_group", where={"_id": str(group_id)}
        )
        if group is None:
            raise ValueError(f"Review tag group {group_id} not found.")

        update_fields = {k: v for k, v in data.items() if v is not None}
        updated = await self.statemgr.update(group, **update_fields)

        return updated

    @action("review-tag-group-deleted", resources="review_tag_group")
    async def delete_review_tag_group(self, *, group_id):
        group = await self.statemgr.find_one(
            "review_tag_group", where={"_id": str(group_id)}
        )
        if group is None:
            raise ValueError(f"Review tag group {group_id} not found.")

        await self.statemgr.invalidate(group)

        return group

    # ── Review Tag Option (admin) ───────────────────────────────

    @action("review-tag-option-created", resources="review_tag_option")
    async def create_review_tag_option(self, *, data):
        group_id = data.get("group_id")
        group = await self.statemgr.find_one(
            "review_tag_group", where={"_id": str(group_id)}
        )
        if group is None:
            raise ValueError(f"Review tag group {group_id} not found.")

        option_id = UUID_GENR()

        option = self.init_resource(
            "review_tag_option",
            data,
            _id=option_id,
        )
        await self.statemgr.insert(option)

        return option

    @action("review-tag-option-updated", resources="review_tag_option")
    async def update_review_tag_option(self, *, option_id, data):
        option = await self.statemgr.find_one(
            "review_tag_option", where={"_id": str(option_id)}
        )
        if option is None:
            raise ValueError(f"Review tag option {option_id} not found.")

        update_fields = {k: v for k, v in data.items() if v is not None}
        updated = await self.statemgr.update(option, **update_fields)

        return updated

    @action("review-tag-option-deleted", resources="review_tag_option")
    async def delete_review_tag_option(self, *, option_id):
        option = await self.statemgr.find_one(
            "review_tag_option", where={"_id": str(option_id)}
        )
        if option is None:
            raise ValueError(f"Review tag option {option_id} not found.")

        await self.statemgr.invalidate(option)

        return option

    # ── Internal helpers ─────────────────────────────────────────

    async def _attach_tag(self, *, comment_id, option_id):
        """Insert a single customer_review_tag row."""
        tag_id = UUID_GENR()
        tag = self.init_resource(
            "customer_review_tag",
            {},
            _id=tag_id,
            review_id=comment_id,
            option_id=option_id,
        )
        await self.statemgr.insert(tag)
        return tag

    async def _replace_tags(self, *, comment_id, option_ids):
        """Soft-delete existing tag selections for a comment, then re-attach."""
        existing_tags = await self.statemgr.find_all(
            "customer_review_tag",
            where={"review_id": str(comment_id), "_deleted": None},
        )
        for tag in existing_tags:
            await self.statemgr.invalidate(tag)

        for option_id in option_ids:
            await self._attach_tag(comment_id=comment_id, option_id=option_id)
