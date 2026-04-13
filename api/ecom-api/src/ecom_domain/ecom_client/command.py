from datetime import datetime, timedelta
from fluvius.data import serialize_mapping, UUID_GENR
from .domain import ECOMClientServiceDomain

from . import datadef
from . import config, logger
import secrets

Command = ECOMClientServiceDomain.Command

class CreateUserCommand(Command):
    """Command to create a new user."""

    class Meta:
        key = "create-new-user"
        description = "Command to create a new user in the system."
        resources = ("user",)
        resource_init = True
        auth_required = False

    async def _process(self, agg, stm, payload):
        username = "Đức Thành"

        yield agg.create_response(
            status="success",
            message="User created successfully.",
            data={
                "username": username
            }
        )

