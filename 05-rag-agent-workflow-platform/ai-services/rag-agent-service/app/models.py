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


class SourceDocument(BaseModel):
    document_id: UUID
    document_version_id: UUID
    content: str


class ChunkingStrategyResource(BaseModel):
    strategy_id: str = Field(pattern=r"^[a-z0-9-]{3,40}$")
    label: str = Field(min_length=3, max_length=80)
    description: str = Field(min_length=10, max_length=300)
    chunk_size: int = Field(ge=120, le=2000)
    overlap: int = Field(ge=0, le=500)
    boundary: Literal["natural-character-window"]


class EvaluationTestCaseCreate(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    relevant_document_ids: list[UUID] = Field(min_length=1, max_length=50)
    rationale: str = Field(min_length=5, max_length=500)

    @field_validator("query", "rationale")
    @classmethod
    def normalize_visible_text(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("value must contain visible text")
        return normalized

    @field_validator("relevant_document_ids")
    @classmethod
    def unique_relevant_documents(cls, value: list[UUID]) -> list[UUID]:
        if len(set(value)) != len(value):
            raise ValueError("relevant_document_ids must be unique")
        return value


class EvaluationTestCaseResource(EvaluationTestCaseCreate):
    test_case_id: UUID
    created_at: datetime


class EvaluationRunRequest(BaseModel):
    strategy_ids: list[str] = Field(min_length=1, max_length=5)
    test_case_ids: list[UUID] = Field(default_factory=list, max_length=100)
    document_version_ids: list[UUID] = Field(default_factory=list, max_length=100)
    top_k: int = Field(default=5, ge=1, le=10)
    correlation_id: UUID

    @field_validator("strategy_ids")
    @classmethod
    def unique_strategies(cls, value: list[str]) -> list[str]:
        normalized = [item.strip() for item in value]
        if len(set(normalized)) != len(normalized):
            raise ValueError("strategy_ids must be unique")
        return normalized

    @field_validator("test_case_ids", "document_version_ids")
    @classmethod
    def unique_identifiers(cls, value: list[UUID]) -> list[UUID]:
        if len(set(value)) != len(value):
            raise ValueError("selected identifiers must be unique")
        return value


class EvaluationHit(BaseModel):
    result_id: UUID
    rank: int = Field(ge=1)
    score: float = Field(ge=-1, le=1)
    document_id: UUID
    document_version_id: UUID
    chunk_id: UUID
    snippet: str
    locator: dict[str, Any]
    relevant: bool
    relevance_source: Literal["expected-set", "manual"] = "expected-set"
    relevance_notes: str | None = None


class EvaluationQueryResult(BaseModel):
    test_case_id: UUID
    query: str
    expected_document_ids: list[UUID]
    precision_at_k: float = Field(ge=0, le=1)
    recall_at_k: float = Field(ge=0, le=1)
    hit: bool
    reciprocal_rank: float = Field(ge=0, le=1)
    results: list[EvaluationHit]


class StrategyMetrics(BaseModel):
    strategy_id: str
    strategy_label: str
    query_count: int = Field(ge=1)
    chunk_count: int = Field(ge=0)
    precision_at_k: float = Field(ge=0, le=1)
    recall_at_k: float = Field(ge=0, le=1)
    hit_rate: float = Field(ge=0, le=1)
    mean_reciprocal_rank: float = Field(ge=0, le=1)
    error_count: int = Field(ge=0)


class EvaluationStrategyResult(BaseModel):
    metrics: StrategyMetrics
    queries: list[EvaluationQueryResult]


class EvaluationRunResource(BaseModel):
    run_id: UUID
    status: Literal["completed"]
    top_k: int
    strategy_ids: list[str]
    test_case_ids: list[UUID]
    document_version_ids: list[UUID]
    embedding_version: str
    score_semantics: str
    metric_semantics: str
    strategies: list[EvaluationStrategyResult]
    created_at: datetime
    completed_at: datetime
    elapsed_ms: float = Field(ge=0)
    correlation_id: UUID


class EvaluationRunSummary(BaseModel):
    run_id: UUID
    top_k: int
    strategy_count: int
    query_count: int
    best_strategy_id: str
    best_recall_at_k: float = Field(ge=0, le=1)
    created_at: datetime


class RelevanceLabelRequest(BaseModel):
    relevant: bool
    notes: str | None = Field(default=None, max_length=500)
    correlation_id: UUID
