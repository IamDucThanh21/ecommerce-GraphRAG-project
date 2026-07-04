from .domain import ECOMAIServiceDomain
from . import startup as _startup
 
# Initialize Neo4j driver + Gemini client once, when this domain module
# is first imported (i.e. when ecom_manager loads it into `domains`).
# Order: Neo4j first, then Gemini — raises immediately if either fails,
# so the app refuses to start in a broken state.

# _startup.setup()
 
__all__ = ["ECOMAIServiceDomain"]
 