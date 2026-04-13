from fluvius.query import DomainQueryManager, DomainQueryResource
from fluvius.query.field import (
    StringField, BooleanField, DateField, UUIDField, PrimaryID, EnumField,
    ArrayField, IntegerField, JSONField, FloatField, DatetimeField, DateField
)
from typing import Optional, Dict, Any

from .state import ECOMStateManager
from .domain import ECOMClientServiceDomain
import uuid

class ECOMClientQueryManager(DomainQueryManager):
    """Query manager for ECOM Client service, handling query operations"""

    __data_manager__ = ECOMStateManager

    class Meta(DomainQueryResource.Meta):
        prefix = ECOMClientServiceDomain.Meta.namespace
        tags = ECOMClientServiceDomain.Meta.tags

resource = ECOMClientQueryManager.register_resource
endpoint = ECOMClientQueryManager.register_endpoint