from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol
from uuid import UUID


class DocumentStorage(Protocol):
    def write(self, version_id: UUID, filename: str, content: str) -> Path | None: ...


class LocalDocumentStorage:
    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, version_id: UUID, filename: str, content: str) -> Path:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(filename).name).strip(".-")
        if not safe_name:
            safe_name = "document.txt"
        destination = self.root / f"{version_id}-{safe_name}"
        destination.write_text(content, encoding="utf-8", newline="\n")
        return destination
