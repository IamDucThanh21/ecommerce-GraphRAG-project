from fluvius.domain.state import DataAccessManager
from ecom_schema import EcomConnector

class ECOMMessageStateManager(DataAccessManager):
    """State manager for the ECOM Client service, handling data access."""
    __connector__ = EcomConnector
    __automodel__ = True
