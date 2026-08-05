from __future__ import annotations

import logging
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.chunking import CharacterWindowChunker
from app.config import Settings
from app.embeddings import (
    DeterministicHashEmbeddingProvider,
    EmbeddingProvider,
    OpenAICompatibleEmbeddingProvider,
)
from app.evaluation import EvaluationService, PostgresEvaluationRepository
from app.extraction import ControlledTextExtractor
from app.models import (
    ChunkingStrategyResource,
    CitationResponse,
    EvaluationRunRequest,
    EvaluationRunResource,
    EvaluationRunSummary,
    EvaluationTestCaseCreate,
    EvaluationTestCaseResource,
    IngestionRequest,
    IngestionResponse,
    IngestionStatus,
    RelevanceLabelRequest,
    SearchRequest,
    SearchResponse,
)
from app.repository import PostgresRagRepository
from app.services import IngestionService, RetrievalService
from app.storage import LocalDocumentStorage

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger("rag-service")
settings = Settings.from_environment()
repository = PostgresRagRepository(settings.database_url)

embedding_provider: EmbeddingProvider
if settings.embedding_provider == "openai-compatible":
    embedding_provider = OpenAICompatibleEmbeddingProvider(
        settings.openai_compatible_base_url,
        settings.openai_compatible_api_key,
        settings.openai_compatible_model,
        settings.embedding_dimension,
    )
else:
    embedding_provider = DeterministicHashEmbeddingProvider(
        settings.embedding_dimension, settings.embedding_model
    )

ingestion_service = IngestionService(
    repository,
    CharacterWindowChunker(settings.chunk_size, settings.chunk_overlap),
    embedding_provider,
    LocalDocumentStorage(settings.storage_root),
    ControlledTextExtractor(),
)
retrieval_service = RetrievalService(repository, embedding_provider)
evaluation_service = EvaluationService(
    PostgresEvaluationRepository(settings.database_url), embedding_provider
)

app = FastAPI(
    title="RAG Agent Service — Internal API",
    version="0.2.0",
    description="Private ingestion, exact-retrieval and retrieval-evaluation boundary.",
    docs_url="/internal/docs",
    openapi_url="/internal/openapi.json",
)


@app.exception_handler(Exception)
async def unhandled_error(request: Request, error: Exception) -> JSONResponse:
    correlation_id = request.headers.get("x-correlation-id", "unavailable")
    logger.exception("request_failed correlation_id=%s path=%s", correlation_id, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "code": "RAG_INTERNAL_ERROR",
            "message": "The RAG service could not complete the operation.",
            "details": {},
            "correlation_id": correlation_id,
        },
    )


@app.get("/healthz", tags=["health"])
def health() -> dict[str, str]:
    if not repository.ping():
        raise HTTPException(status_code=503, detail="pgvector is unavailable")
    return {"status": "ok", "service": "rag-agent-service"}


@app.post("/internal/v1/ingestions", response_model=IngestionResponse, tags=["ingestion"])
def create_ingestion(payload: IngestionRequest) -> IngestionResponse:
    return ingestion_service.ingest(payload)


@app.get("/internal/v1/ingestions/{job_id}", response_model=IngestionStatus, tags=["ingestion"])
def get_ingestion(job_id: UUID) -> IngestionStatus:
    status = ingestion_service.status(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="ingestion job not found")
    return status


@app.post("/internal/v1/retrieval/search", response_model=SearchResponse, tags=["retrieval"])
def search(payload: SearchRequest) -> SearchResponse:
    return retrieval_service.search(payload)


@app.get(
    "/internal/v1/citations/{citation_id}", response_model=CitationResponse, tags=["retrieval"]
)
def citation(citation_id: UUID) -> CitationResponse:
    resource = retrieval_service.citation(citation_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="citation not found")
    return resource


@app.get(
    "/internal/v1/evaluations/strategies",
    response_model=list[ChunkingStrategyResource],
    tags=["evaluation"],
)
def evaluation_strategies() -> list[ChunkingStrategyResource]:
    return evaluation_service.list_strategies()


@app.post(
    "/internal/v1/evaluations/test-cases",
    response_model=EvaluationTestCaseResource,
    tags=["evaluation"],
)
def create_evaluation_test_case(
    payload: EvaluationTestCaseCreate,
) -> EvaluationTestCaseResource:
    return evaluation_service.create_test_case(payload)


@app.get(
    "/internal/v1/evaluations/test-cases",
    response_model=list[EvaluationTestCaseResource],
    tags=["evaluation"],
)
def evaluation_test_cases() -> list[EvaluationTestCaseResource]:
    return evaluation_service.list_test_cases()


@app.post(
    "/internal/v1/evaluations/runs",
    response_model=EvaluationRunResource,
    tags=["evaluation"],
)
def create_evaluation_run(payload: EvaluationRunRequest) -> EvaluationRunResource:
    try:
        return evaluation_service.run(payload)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.get(
    "/internal/v1/evaluations/runs",
    response_model=list[EvaluationRunSummary],
    tags=["evaluation"],
)
def evaluation_runs() -> list[EvaluationRunSummary]:
    return evaluation_service.list_runs()


@app.get(
    "/internal/v1/evaluations/runs/{run_id}",
    response_model=EvaluationRunResource,
    tags=["evaluation"],
)
def evaluation_run(run_id: UUID) -> EvaluationRunResource:
    run = evaluation_service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="evaluation run not found")
    return run


@app.patch(
    "/internal/v1/evaluations/runs/{run_id}/results/{result_id}/relevance",
    response_model=EvaluationRunResource,
    tags=["evaluation"],
)
def label_evaluation_result(
    run_id: UUID, result_id: UUID, payload: RelevanceLabelRequest
) -> EvaluationRunResource:
    try:
        run = evaluation_service.label(run_id, result_id, payload)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    if run is None:
        raise HTTPException(status_code=404, detail="evaluation run not found")
    return run
