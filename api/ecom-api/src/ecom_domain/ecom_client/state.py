from fluvius.domain.state import DataAccessManager
from ecom_schema import EcomConnector

class ECOMStateManager(DataAccessManager):
    """State manager for the TTP Tour service, handling data access."""
    __connector__ = EcomConnector
    __automodel__ = True
