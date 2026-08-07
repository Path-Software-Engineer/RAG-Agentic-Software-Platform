from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    storage_root: str
    chunk_size: int
    chunk_overlap: int
    embedding_provider: str
    embedding_model: str
    embedding_dimension: int
    openai_compatible_base_url: str
    openai_compatible_api_key: str
    openai_compatible_model: str

    @classmethod
    def from_environment(cls) -> Settings:
        settings = cls(
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://rag_platform:local_only_change_me@localhost:55432/rag_platform",
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:56379/0"),
            storage_root=os.getenv("STORAGE_ROOT", "storage/documents"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "520")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "80")),
            embedding_provider=os.getenv("EMBEDDING_PROVIDER", "deterministic"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "deterministic-hash-v1"),
            embedding_dimension=int(os.getenv("EMBEDDING_DIMENSION", "128")),
            openai_compatible_base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL", ""),
            openai_compatible_api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY", ""),
            openai_compatible_model=os.getenv("OPENAI_COMPATIBLE_MODEL", ""),
        )
        if settings.chunk_size < 120:
            raise ValueError("CHUNK_SIZE must be at least 120")
        if settings.chunk_overlap < 0 or settings.chunk_overlap >= settings.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be non-negative and smaller than CHUNK_SIZE")
        if settings.embedding_dimension != 128:
            raise ValueError("Sprint 1 migration is locked to EMBEDDING_DIMENSION=128")
        return settings
