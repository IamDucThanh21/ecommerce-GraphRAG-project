"""Lightweight handler that forwards chat messages to ecom_ai and returns replies.

Calls ask_graph() with no pre-built driver — service.py initializes
the Neo4j connection automatically from config, so Neo4j is always queried.
"""
import logging
from typing import Any, Dict, Optional

from ecom_ai.service import ask_graph

logger = logging.getLogger(__name__)


def handle_chat_message(
    text: str,
    user_id: Optional[str] = None,
    ai_client=None,
    driver=None,
) -> Dict[str, Any]:
    """Handle an incoming chat message through the full pipeline.

    Args:
        text:      User message text.
        user_id:   Optional user identifier for logging / future personalization.
        ai_client: Optional AIClient instance (useful for testing with mocks).
        driver:    Optional Neo4j driver. If None, service.py creates one from config.

    Returns:
        Dict with keys: answer, cypher, conversation_id, raw_result.
    """
    try:
        result = ask_graph(text, driver=driver, ai_client=ai_client)
    except Exception as exc:
        logger.exception("Failed to handle chat message for user=%s: %s", user_id, exc)
        return {
            "answer": "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu.",
            "error": str(exc),
        }

    return {
        "answer": result.get("answer"),
        "cypher": result.get("cypher"),
        "conversation_id": result.get("conversation_id"),
        "raw_result": result.get("raw_result"),
    }