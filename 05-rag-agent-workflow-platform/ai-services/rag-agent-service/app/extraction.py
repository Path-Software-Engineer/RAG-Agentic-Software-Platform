from __future__ import annotations

from typing import Protocol

from app.normalization import normalize_text


class DocumentExtractor(Protocol):
    def extract(self, content: str, media_type: str) -> str: ...


class ControlledTextExtractor:
    """Extracts only the UTF-8 text formats admitted by the Sprint 1 contract."""

    allowed_media_types = frozenset({"text/plain", "text/markdown"})

    def extract(self, content: str, media_type: str) -> str:
        if media_type not in self.allowed_media_types:
            raise ValueError("document media type is not supported")
        return normalize_text(content)
