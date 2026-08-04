from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class IngestionRequest(BaseModel):
    job_id: UUID
    document_id: UUID
    document_version_id: UUID
    filename: str = Field(min_length=1, max_length=255)
    media_type: Literal["text/plain", "text/markdown"]
    content: str = Field(min_length=1, max_length=1_048_576)
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    correlation_id: UUID


class IngestionResponse(BaseModel):
    job_id: UUID
    status: Literal["running", "completed", "failed"]
    chunk_count: int = Field(ge=0)
    embedding_version_id: UUID | None = None
    elapsed_ms: float = Field(ge=0)
    correlation_id: UUID


class IngestionStatus(BaseModel):
    job_id: UUID
    status: Literal["running", "completed", "failed"]
    chunk_count: int = Field(ge=0)
    embedding_version_id: UUID | None = None
    error_code: str | None = None
    started_at: datetime
    completed_at: datetime | None = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    top_k: int = Field(default=5, ge=1, le=10)
    document_ids: list[UUID] = Field(default_factory=list, max_length=50)
    document_version_ids: list[UUID] = Field(default_factory=list, max_length=50)
    correlation_id: UUID

    @field_validator("query")
    @classmethod
    def query_must_have_text(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if len(normalized) < 2:
            raise ValueError("query must contain visible text")
        return normalized


class InternalSearchResult(BaseModel):
    rank: int = Field(ge=1)
    score: float = Field(ge=-1, le=1)
    document_id: UUID
    document_version_id: UUID
    chunk_id: UUID
    citation_id: UUID
    snippet: str
    locator: dict[str, Any]


class SearchResponse(BaseModel):
    query: str
    top_k: int
    embedding_version_id: UUID
    score_semantics: str
    results: list[InternalSearchResult]
    elapsed_ms: float = Field(ge=0)
    correlation_id: UUID


class CitationResponse(BaseModel):
    citation_id: UUID
    document_id: UUID
    document_version_id: UUID
    chunk_id: UUID
    score: float = Field(ge=-1, le=1)
    snippet: str
    content: str
    locator: dict[str, Any]


class ChunkRecord(BaseModel):
    id: UUID
    document_id: UUID
    document_version_id: UUID
    chunk_index: int
    chunking_version: str
    content: str
    start_offset: int
    end_offset: int
    locator: dict[str, Any]


class RepositorySearchRow(BaseModel):
    document_id: UUID
    document_version_id: UUID
    chunk_id: UUID
    content: str
    start_offset: int
    end_offset: int
    score: float
    citation_id: UUID
