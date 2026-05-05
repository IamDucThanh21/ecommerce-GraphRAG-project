from fluvius.domain import Domain, SQLDomainLogStore
from fluvius.domain.aggregate import Aggregate

from .state import ECOMProductStateManager
from .aggregate import ECOMProductAggregate

from ._meta import config


class ECOMProductServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMProductStateManager
    __aggregate__ = ECOMProductAggregate
    __log_store__ = SQLDomainLogStore

class EcomServiceResponse(ECOMProductServiceDomain.Response):
    pass

class EcomServiceMessage(ECOMProductServiceDomain.Message):
    pass