from fluvius.domain import Domain, SQLDomainLogStore
# from fluvius.domain.aggregate import Aggregate

from .state import ECOMDiscussStateManager
from .aggregate import ECOMDiscussAggregate

from ._meta import config


class ECOMDiscussServiceDomain(Domain):
    __namespace__ = config.NAMESPACE
    __statemgr__ = ECOMDiscussStateManager
    __aggregate__ = ECOMDiscussAggregate
    __log_store__ = SQLDomainLogStore


class EcomDiscussResponse(ECOMDiscussServiceDomain.Response):
    pass

class EcomDiscussMessage(ECOMDiscussServiceDomain.Message):
    pass


class CommentServiceResponse(ECOMDiscussServiceDomain.Response):
    pass

class CommentServiceMessage(ECOMDiscussServiceDomain.Message):
    pass


class CommentReactionServiceResponse(ECOMDiscussServiceDomain.Response):
    pass

class CommentReactionServiceMessage(ECOMDiscussServiceDomain.Message):
    pass


class ReviewTagGroupServiceResponse(ECOMDiscussServiceDomain.Response):
    pass

class ReviewTagGroupServiceMessage(ECOMDiscussServiceDomain.Message):
    pass


class ReviewTagOptionServiceResponse(ECOMDiscussServiceDomain.Response):
    pass

class ReviewTagOptionServiceMessage(ECOMDiscussServiceDomain.Message):
    pass
