from fluvius.domain import Domain, SQLDomainLogStore

from .state import ECOMAiStateManager
from .aggregate import EcomAiAggregate

from . import config


class ECOMAIServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMAiStateManager
    __aggregate__ = EcomAiAggregate
    __log_store__ = SQLDomainLogStore


class AiServiceResponse(ECOMAIServiceDomain.Response):
    """Response class for AI service operations."""
    pass


class AiServiceMessage(ECOMAIServiceDomain.Message):
    """Message class for AI service operations."""
    pass