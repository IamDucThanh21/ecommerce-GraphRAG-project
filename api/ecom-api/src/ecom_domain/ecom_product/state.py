from fluvius.domain.state import DataAccessManager
from ecom_schema import EcomConnector


class ECOMProductStateManager(DataAccessManager):
    __connector__ = EcomConnector
    __automodel__ = True
