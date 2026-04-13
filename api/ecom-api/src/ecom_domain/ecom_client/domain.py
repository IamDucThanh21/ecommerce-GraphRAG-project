from fluvius.domain import Domain, SQLDomainLogStore

from .state import ECOMStateManager
from .aggregate import EcomClientAggregate

from . import config

class ECOMClientServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMStateManager
    __aggregate__ = EcomClientAggregate
    __log_store__ = SQLDomainLogStore

class TourServiceResponse(ECOMClientServiceDomain.Response):
    pass

class TourServiceMessage(ECOMClientServiceDomain.Message):
    pass
