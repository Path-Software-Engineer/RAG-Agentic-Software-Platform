from __future__ import annotations

import re
import unicodedata


def normalize_text(value: str) -> str:
    """Return canonical, readable UTF-8 text while preserving paragraph boundaries."""
    value = unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[\t ]+", " ", line).strip() for line in value.split("\n")]
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip()
    if not normalized:
        raise ValueError("document has no visible text")
    return normalized
