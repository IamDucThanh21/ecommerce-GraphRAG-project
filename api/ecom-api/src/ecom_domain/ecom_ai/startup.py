"""Application startup — initialize Neo4j driver and Gemini AI client once.

Usage in your app entrypoint:
    from ecom_ai.startup import setup, get_driver, get_ai_client

    await setup()          # call once at startup
    driver = get_driver()  # call anywhere after setup
    ai_client = get_ai_client()
"""
import logging
from typing import Optional

from .ai_client import AIClient, init_client
from .neo4j_client import setup as neo4j_setup
from neo4j import Driver

logger = logging.getLogger(__name__)

# Module-level singletons
_driver: Optional[Driver] = None
_ai_client: Optional[AIClient] = None


# ── Setup ─────────────────────────────────────────────────────────────────────

def setup_neo4j() -> Driver:
    """Initialize and verify Neo4j driver. Raises on failure."""
    global _driver
    logger.info("Connecting to Neo4j...")
    _driver = neo4j_setup(verify=True)   # verify=True calls driver.verify_connectivity()
    logger.info("Neo4j connected.")
    return _driver


def setup_gemini() -> AIClient:
    """Initialize Gemini AI client. Raises if API key is missing."""
    global _ai_client
    logger.info("Initializing Gemini AI client...")
    _ai_client = init_client()

    if not _ai_client.api_key:
        raise RuntimeError(
            "Gemini API key not found. "
            "Set GEMINI_API_KEY env var or add [ai] GEMINI_API_KEY to config.ini"
        )
    if not _ai_client._model:
        raise RuntimeError("Gemini model failed to initialize. Check your API key and model name.")

    logger.info("Gemini AI client ready. Model: %s", _ai_client.model_name)
    return _ai_client


def setup() -> dict:
    """Run full startup sequence: Neo4j first, then Gemini.

    Returns a status dict so callers can log or display the result.
    Raises immediately on any failure — app should not start in a broken state.
    """
    driver = setup_neo4j()
    ai_client = setup_gemini()

    return {
        "neo4j": "connected",
        "gemini": "ready",
        "gemini_model": ai_client.model_name,
    }


# ── Getters ───────────────────────────────────────────────────────────────────

def get_driver() -> Driver:
    """Return the initialized Neo4j driver. Raises if setup() was not called."""
    if _driver is None:
        raise RuntimeError("Neo4j driver not initialized. Call setup() at startup.")
    return _driver


def get_ai_client() -> AIClient:
    """Return the initialized Gemini AI client. Raises if setup() was not called."""
    if _ai_client is None:
        raise RuntimeError("Gemini AI client not initialized. Call setup() at startup.")
    return _ai_client


# ── Health check ──────────────────────────────────────────────────────────────

def health() -> dict:
    """Check current status of both clients without raising.

    Safe to call at any time — does not throw, returns status strings.
    Use this for a /health endpoint or a startup probe.
    """
    neo4j_status = "not_initialized"
    gemini_status = "not_initialized"

    if _driver is not None:
        try:
            _driver.verify_connectivity()
            neo4j_status = "connected"
        except Exception as exc:
            neo4j_status = f"error: {exc}"

    if _ai_client is not None:
        if _ai_client._model and _ai_client.api_key:
            gemini_status = f"ready ({_ai_client.model_name})"
        else:
            gemini_status = "error: model not configured"

    return {
        "neo4j": neo4j_status,
        "gemini": gemini_status,
    }


def teardown() -> None:
    """Close the Neo4j driver gracefully. Call on app shutdown."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.info("Neo4j driver closed.")