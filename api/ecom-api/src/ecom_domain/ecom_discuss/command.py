"""Command definitions for ecom_discuss domain.

Add command classes here. Left empty for user to implement.
"""

from fluvius.data import serialize_mapping, UUID_GENR
from .domain import ECOMDiscussServiceDomain

from . import datadef
from . import config, logger

Command = ECOMDiscussServiceDomain.Command

class CreateCommentCommand(Command):
    """Create a top-level comment on a product or post."""

    Data = datadef.CreateCommentData

    class Meta:
        key = "create-comment"
        description = "Create a comment on a product or post."
        resources = ("comment",)
        resource_init = True
        tags = ["discuss", "comment"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id
        # resource_id = agg.get_aggroot().identifier

        result = await agg.create_comment(data=data, user_id=user_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-service-response",
        )


class ReplyCommentCommand(Command):
    """Admin reply to a comment."""

    Data = datadef.ReplyCommentData

    class Meta:
        key = "reply-comment"
        description = "Admin reply to an existing comment."
        resources = ("comment",)
        resource_init = True
        tags = ["discuss", "comment"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        ctx = agg.get_context()
        user_id = ctx.user_id

        # print(ctx.authorization)

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.reply_comment(data=data, user_id=user_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-service-response",
        )


class UpdateCommentCommand(Command):
    """Update own comment (content/star/tags)."""

    Data = datadef.UpdateCommentData

    class Meta:
        key = "update-comment"
        description = "Update an existing comment owned by the caller."
        resources = ("comment",)
        tags = ["discuss", "comment"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id
        comment_id = agg.get_aggroot().identifier

        result = await agg.update_comment(
            comment_id=comment_id, data=data, user_id=user_id
        )

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-service-response",
        )


class DeleteCommentCommand(Command):
    """Soft-delete own comment."""

    Data = datadef.DeleteCommentData

    class Meta:
        key = "delete-comment"
        description = "Delete a comment owned by the caller."
        resources = ("comment",)
        tags = ["discuss", "comment"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        user_id = agg.get_context().user_id
        comment_id = agg.get_aggroot().identifier

        result = await agg.delete_comment(comment_id=comment_id, user_id=user_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-service-response",
        )


# ── Comment Reaction ─────────────────────────────────────────────────

class ReactToCommentCommand(Command):
    """React to a comment (creates or replaces caller's existing reaction)."""

    Data = datadef.ReactToCommentData

    class Meta:
        key = "react-to-comment"
        description = "React to a comment. Replaces any existing reaction by the caller."
        resource_init = True
        resources = ("comment_reaction",)
        tags = ["discuss", "reaction"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id

        result = await agg.react_to_comment(data=data, user_id=user_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-reaction-service-response",
        )


class RemoveReactionCommand(Command):
    """Remove caller's reaction from a comment."""

    Data = datadef.RemoveReactionData

    class Meta:
        key = "remove-reaction"
        description = "Remove the caller's reaction from a comment."
        resources = ("comment_reaction",)
        tags = ["discuss", "reaction"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        user_id = agg.get_context().user_id

        result = await agg.remove_reaction(data=data, user_id=user_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="comment-reaction-service-response",
        )


# ── Review Tag Group (admin) ────────────────────────────────────────

class CreateReviewTagGroupCommand(Command):
    """Admin: create a new tag group."""

    Data = datadef.CreateReviewTagGroupData

    class Meta:
        key = "create-review-tag-group"
        description = "Create a new review tag group (admin only)."
        resource_init = True
        resources = ("review_tag_group",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.create_review_tag_group(data=data)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-group-service-response",
        )


class UpdateReviewTagGroupCommand(Command):
    """Admin: update a tag group."""

    Data = datadef.UpdateReviewTagGroupData

    class Meta:
        key = "update-review-tag-group"
        description = "Update a review tag group (admin only)."
        resources = ("review_tag_group",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        group_id = agg.get_aggroot().identifier
        

        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")
        
        result = await agg.update_review_tag_group(group_id=group_id, data=data)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-group-service-response",
        )


class DeleteReviewTagGroupCommand(Command):
    """Admin: delete a tag group (cascades to its options)."""

    Data = datadef.DeleteReviewTagGroupData

    class Meta:
        key = "delete-review-tag-group"
        description = "Delete a review tag group (admin only)."
        resources = ("review_tag_group",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        group_id = agg.get_aggroot().identifier

        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.delete_review_tag_group(group_id=group_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-group-service-response",
        )


# ── Review Tag Option (admin) ───────────────────────────────────────

class CreateReviewTagOptionCommand(Command):
    """Admin: create a new tag option under a group."""

    Data = datadef.CreateReviewTagOptionData

    class Meta:
        key = "create-review-tag-option"
        description = "Create a new review tag option (admin only)."
        resource_init = True
        resources = ("review_tag_option",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)

        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.create_review_tag_option(data=data)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-option-service-response",
        )


class UpdateReviewTagOptionCommand(Command):
    """Admin: update a tag option."""

    Data = datadef.UpdateReviewTagOptionData

    class Meta:
        key = "update-review-tag-option"
        description = "Update a review tag option (admin only)."
        resources = ("review_tag_option",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
        option_id = agg.get_aggroot().identifier

        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.update_review_tag_option(option_id=option_id, data=data)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-option-service-response",
        )


class DeleteReviewTagOptionCommand(Command):
    """Admin: delete a tag option."""

    Data = datadef.DeleteReviewTagOptionData

    class Meta:
        key = "delete-review-tag-option"
        description = "Delete a review tag option (admin only)."
        resources = ("review_tag_option",)
        tags = ["discuss", "tag"]
        auth_required = True
        policy_required = False

    async def _process(self, agg, stm, payload):
        option_id = agg.get_aggroot().identifier

        ctx = agg.get_context()

        # TODO: replace with actual admin-check attribute once auth role is defined
        if "admin" not in ctx.authorization.iamroles:
            raise PermissionError("Only admin can reply to comments.")

        result = await agg.delete_review_tag_option(option_id=option_id)

        yield agg.create_response(
            serialize_mapping(result),
            _type="review-tag-option-service-response",
        )
