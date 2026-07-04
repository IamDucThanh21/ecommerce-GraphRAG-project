from fluvius.domain.state import DataAccessManager
from ecom_schema import EcomConnector


class ECOMDiscussStateManager(DataAccessManager):
    __connector__ = EcomConnector
    __automodel__ = True
