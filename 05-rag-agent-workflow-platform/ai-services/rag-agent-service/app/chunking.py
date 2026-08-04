from __future__ import annotations

from uuid import UUID, uuid5

from app.models import ChunkRecord

CHUNKING_VERSION = "char-window-v1"


class CharacterWindowChunker:
    def __init__(self, size: int, overlap: int) -> None:
        if size < 120 or overlap < 0 or overlap >= size:
            raise ValueError("invalid chunking boundary")
        self.size = size
        self.overlap = overlap

    def chunk(self, document_id: UUID, version_id: UUID, text: str) -> list[ChunkRecord]:
        chunks: list[ChunkRecord] = []
        start = 0
        index = 0
        while start < len(text):
            hard_end = min(start + self.size, len(text))
            end = self._preferred_boundary(text, start, hard_end)
            content = text[start:end].strip()
            if content:
                actual_start = start + len(text[start:end]) - len(text[start:end].lstrip())
                actual_end = actual_start + len(content)
                chunks.append(
                    ChunkRecord(
                        id=uuid5(
                            version_id, f"{CHUNKING_VERSION}:{index}:{actual_start}:{actual_end}"
                        ),
                        document_id=document_id,
                        document_version_id=version_id,
                        chunk_index=index,
                        chunking_version=CHUNKING_VERSION,
                        content=content,
                        start_offset=actual_start,
                        end_offset=actual_end,
                        locator={
                            "kind": "character_range",
                            "start": actual_start,
                            "end": actual_end,
                        },
                    )
                )
                index += 1
            if end >= len(text):
                break
            next_start = max(end - self.overlap, start + 1)
            start = next_start
        return chunks

    @staticmethod
    def _preferred_boundary(text: str, start: int, hard_end: int) -> int:
        if hard_end == len(text):
            return hard_end
        minimum = start + max(80, (hard_end - start) // 2)
        for marker in ("\n\n", ". ", "\n", " "):
            candidate = text.rfind(marker, minimum, hard_end)
            if candidate >= minimum:
                return candidate + len(marker)
        return hard_end
