# SendMessage Flow — Architecture Documentation

## Overview

This document describes the end-to-end flow when a user sends a chat message
and receives an AI-generated product recommendation, powered by Gemini + Neo4j
graph database, integrated through the `ecom_message` and `ecom_ai` DDD domains.

---

## Sequence (step by step)

1. **User** sends `POST /send-message` with `{ content: "..." }`, authenticated via JWT.
2. **`SendMessageCommand`** (`ecom_message/commands.py`) receives the request, extracts
   `user_id` from auth context and `conversation_id` from the aggregate root identifier.
3. Command calls **`agg.save_user_message(...)`** — aggregate verifies the conversation
   belongs to the user, computes the next `sequence_number`, and inserts a `message`
   row with `role=user`.
4. Command calls **`agg.save_bot_reply(...)`**, passing the user's raw message content.
5. Aggregate calls **`ask_graph(user_content)`** from `ecom_ai.service` — this is the
   entry point into the AI domain.
6. **`cypher_gen.generate_cypher()`** sends the user's question + the graph schema
   (as a system prompt) to **Gemini**, which returns a raw Cypher query string.
7. **`neo4j_client.run_query()`** executes that Cypher query against the **Neo4j**
   product graph database, returning matching products as rows.
8. **`service.ask_graph()`** sends those rows back to **Gemini** a second time, asking
   it to write a concise Vietnamese recommendation referencing the actual data.
9. The resulting text becomes `bot_content`. The aggregate inserts a second `message`
   row with `role=assistant`.
10. **`SendMessageCommand`** yields a response containing both `user_message` and
    `bot_message`, returned to the user as JSON.

---

## File-by-file responsibilities

### `ecom_domain/ecom_message/` — Conversation & Message domain

| File | Mission |
|---|---|
| `commands.py` → `SendMessageCommand` | Entry point for the API call. Extracts `user_id` and `conversation_id`, orchestrates the two-step call (save user message → generate bot reply), and formats the final response. |
| `aggregate.py` → `save_user_message()` | Verifies conversation ownership, computes message ordering (`sequence_number`), persists the user's message to SQL. |
| `aggregate.py` → `save_bot_reply()` | Bridges to the AI domain by calling `ask_graph()`, then persists the returned answer as an assistant message. |
| `state.py` → `ECOMMessageStateManager` | SQL data access layer (`conversation`, `message` tables) via `EcomConnector`. |
| `domain.py` → `ECOMMessageServiceDomain` | Registers the domain with fluvius — namespace, state manager, aggregate, log store. |
| `_meta/` | Module configuration (namespace `ecom-message`, DB schema name). |

---

### `ecom_domain/ecom_ai/` — AI / Graph recommendation domain

| File | Mission |
|---|---|
| `service.py` → `ask_graph()` | **Orchestrator** of the AI pipeline. Calls `generate_cypher()` → `run_query()` → second Gemini call to produce the final answer. Returns `{answer, cypher, raw_result, conversation_id}`. |
| `cypher_gen.py` → `generate_cypher()` | Sends the **graph schema + query rules** as a system prompt and the user's question as the user prompt to Gemini via `AIClient.chat()`. Strips markdown fences from the response to produce raw Cypher. |
| `ai_client.py` → `AIClient` | Thin wrapper around `google.generativeai`. Provides `generate_content()` (single prompt) and `chat()` (system + user prompt separation). Configured once with API key + model name. |
| `neo4j_client.py` → `setup()`, `run_query()` | Creates the Neo4j driver and executes Cypher queries, returning rows as `List[Dict]`. |
| `startup.py` | **Singleton lifecycle manager.** `setup()` initializes Neo4j (`setup_neo4j()`) then Gemini (`setup_gemini()`) once at app startup. `get_driver()` / `get_ai_client()` return the singletons for use in `service.py`. `health()` reports live status without raising. `teardown()` closes the Neo4j driver on shutdown. |
| `config.py` | Resolves Neo4j + Gemini credentials — environment variables take priority, falling back to `config.ini [ecom-ai]` section via the fluvius `_meta` config system. |
| `aggregate.py` → `EcomAiAggregate.ask()` | Exposes `ask_graph()` as a fluvius aggregate action (`ask-graph` command), usable as a standalone API endpoint independent of `ecom_message`. |
| `commands.py` → `AskGraphCommand` | Standalone command (`POST /ask-graph`) for directly querying the AI pipeline without going through a conversation — useful for testing. |
| `datadef.py` → `AskGraphData` | Pydantic schema for the standalone `ask-graph` command (`{query: str}`). |
| `domain.py` → `ECOMAIServiceDomain` | Registers the AI domain with fluvius. No SQL tables of its own (`__automodel__ = False`) — persistent state lives in Neo4j. |
| `__init__.py` | Exports `ECOMAIServiceDomain` and **triggers `startup.setup()` at import time** — this is what guarantees Neo4j + Gemini are ready before any request is handled. |
| `utils.py` | Small helpers: `sanitize_text()` (strip control chars), `to_json()` (safe JSON serialization for logging/debugging). |
| `_meta/` | Module configuration — namespace `ecom-ai`, Neo4j/Gemini default values, schema name. |

---

### `ecom_manager/` — Application wiring

| File | Mission |
|---|---|
| `__init__.py` | Builds the FastAPI app via fluvius. Registers `ECOMMessageServiceDomain` and `ECOMAIServiceDomain` (among others) in the `domains` tuple. Importing `ecom_ai` here is what fires its `__init__.py` startup sequence. |
| `main.py` | ASGI entrypoint — runs `uvicorn`. |

---

## Key design notes

- **Two Gemini calls per message**: one to *generate* the Cypher query (with schema
  context), one to *interpret* the Neo4j results into natural Vietnamese.
- **Two-step aggregate actions**: `save_user_message` and `save_bot_reply` are
  separate domain actions/events (`user-message-saved`, `bot-reply-saved`),
  giving a clean audit trail in the domain event log.
- **Singletons via `startup.py`**: Neo4j driver and Gemini client are created once
  at app boot (when `ecom_ai` is imported by `ecom_manager`), not per-request —
  avoiding repeated connection/auth overhead.
- **Domain boundary**: `ecom_message` never talks to Neo4j or Gemini directly —
  it only calls `ecom_ai.service.ask_graph()`, keeping the AI/graph concern
  isolated in its own bounded context.
