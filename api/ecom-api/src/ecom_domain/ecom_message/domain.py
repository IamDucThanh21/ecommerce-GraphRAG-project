from fluvius.domain import Domain, SQLDomainLogStore

from .state import ECOMMessageStateManager
from .aggregate import EcomMessageAggregate

from . import config

class ECOMMessageServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMMessageStateManager
    __aggregate__ = EcomMessageAggregate
    __log_store__ = SQLDomainLogStore


class ConversationServiceResponse(ECOMMessageServiceDomain.Response):
    """Response class for conversation service operations."""
    pass

class ConversationServiceMessage(ECOMMessageServiceDomain.Message):
    """Message class for conversation service operations."""
    pass

class MessageServiceResponse(ECOMMessageServiceDomain.Response):
    """Response class for message service operations."""
    pass

class MessageServiceMessage(ECOMMessageServiceDomain.Message):
    """Message class for message service operations."""
    pass