from fluvius.domain.state import DataAccessManager
from ecom_schema import EcomConnector
 
 
class ECOMAiStateManager(DataAccessManager):
    """State manager for the ECOM AI service.
 
    ecom_ai itself has no SQL tables of its own (its persistent data lives
    in Neo4j). It still needs a connector to satisfy the Domain base class
    and to log domain events / responses via the shared SQL log store.
    """
    __connector__ = EcomConnector
    __automodel__ = False
 