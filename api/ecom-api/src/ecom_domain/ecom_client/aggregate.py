from fluvius.domain.aggregate import Aggregate, action
from fluvius.data import serialize_mapping, UUID_GENR
from fluvius.data.exceptions import ItemNotFoundError
from decimal import Decimal

from ecom_schema.ecom_client.user import User

from . import logger
from datetime import datetime, timezone, timedelta, date, time


class EcomClientAggregate(Aggregate):
    """Aggregate for ecom client domain."""

    