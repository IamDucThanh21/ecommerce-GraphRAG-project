import logging
from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase, Driver

from .config import get_neo4j_config

logger = logging.getLogger(__name__)


def setup(verify: bool = True) -> Driver:
    uri, user, password = get_neo4j_config()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    if verify:
        try:
            driver.verify_connectivity()
            logger.info("Neo4j connectivity verified")
        except Exception as exc:
            logger.exception("Failed to verify Neo4j connectivity: %s", exc)
            raise
    return driver


def run_query(driver: Driver, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    # parameters = parameters or {}
    with driver.session() as session:
        result = session.run(query)
        rows = [dict(r) for r in result]
    return rows

# def run_cypher(driver: Driver, query: str) -> list[dict]:
#     """Execute a Cypher query and return rows as list of dicts."""
#     with driver.session() as session:
#         result = session.run(query)
#         rows = [dict(r) for r in result]
#     return rows
