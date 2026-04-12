from fluvius.domain import Domain, SQLDomainLogStore

from .state import ECOMStateManager
from .aggregate import TTPTourAggregate

from . import config

class TTPTourServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMStateManager
    __aggregate__ = TTPTourAggregate
    __log_store__ = SQLDomainLogStore

class TourServiceResponse(TTPTourServiceDomain.Response):
    pass

class TourServiceMessage(TTPTourServiceDomain.Message):
    pass
