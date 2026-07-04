import re
import json
from typing import Any


def sanitize_text(text: str) -> str:
    text = re.sub(r"[\x00-\x1f\x7f]+", " ", text)
    return text.strip()


def to_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)