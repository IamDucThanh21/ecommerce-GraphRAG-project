# import os
# import configparser
# from pathlib import Path
# from typing import Optional, Tuple


# def _default_config_path() -> Path:
#     # Default: <repo>/api/ecom-api/env/develop/cfg/config.ini
#     return Path(__file__).resolve().parents[4] / "env" / "develop" / "cfg" / "config.ini"


# def load_config(path: Optional[Path] = None) -> configparser.ConfigParser:
#     path = Path(path) if path else _default_config_path()
#     cfg = configparser.ConfigParser()
#     if path.exists():
#         cfg.read(path)
#     return cfg


# def get_gemini_api_key() -> Optional[str]:
#     # Prefer environment variable, fall back to config file under [ai] GEMINI_API_KEY
#     key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
#     if key:
#         return key

#     cfg = load_config()
#     if cfg.has_section("ai") and cfg.has_option("ai", "GEMINI_API_KEY"):
#         return cfg.get("ai", "GEMINI_API_KEY")

#     return None


# def get_gemini_model() -> str:
#     # Environment override then config then sensible default
#     model = os.environ.get("GEMINI_MODEL")
#     if model:
#         return model
#     cfg = load_config()
#     if cfg.has_section("ai") and cfg.has_option("ai", "GEMINI_MODEL"):
#         return cfg.get("ai", "GEMINI_MODEL")
#     return "gemini-2.5-flash"


# def get_neo4j_config() -> Tuple[str, str, str]:
#     # Return (uri, user, password)
#     uri = os.environ.get("NEO4J_URI")
#     user = os.environ.get("NEO4J_USER")
#     password = os.environ.get("NEO4J_PASSWORD")

#     if uri and user and password:
#         return uri, user, password

#     cfg = load_config()
#     if cfg.has_section("neo4j"):
#         uri = uri or cfg.get("neo4j", "URI", fallback=None)
#         user = user or cfg.get("neo4j", "USER", fallback=None)
#         password = password or cfg.get("neo4j", "PASSWORD", fallback=None)

#     # sensible defaults (match existing notebook defaults)
#     uri = uri or "bolt://172.18.224.1:7687"
#     user = user or "neo4j"
#     password = password or "12345678"

#     return uri, user, password

import os
from typing import Optional, Tuple
 
from ._meta import config, logger
 
NAMESPACE = config.NAMESPACE
ECOM_AI_SCHEMA = config.ECOM_AI_SCHEMA
 
 
# ── Gemini ────────────────────────────────────────────────────────────────────
 
def get_gemini_api_key() -> Optional[str]:
    """Env var takes priority, falls back to config.ini [ecom_ai] GEMINI_API_KEY."""
    return (
        os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or config.GEMINI_API_KEY
    )
 
 
def get_gemini_model() -> str:
    return os.environ.get("GEMINI_MODEL") or config.GEMINI_MODEL or "gemini-2.5-flash"
 
 
# ── Neo4j ─────────────────────────────────────────────────────────────────────
 
def get_neo4j_config() -> Tuple[str, str, str]:
    """Env vars take priority, fall back to config.ini [ecom_ai] values."""
    uri = os.environ.get("NEO4J_URI") or config.NEO4J_URI
    user = os.environ.get("NEO4J_USER") or config.NEO4J_USER
    password = os.environ.get("NEO4J_PASSWORD") or config.NEO4J_PASSWORD
    return uri, user, password
 