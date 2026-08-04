from __future__ import annotations

import hashlib
import time
from uuid import UUID

from app.chunking import CharacterWindowChunker
from app.embeddings import EmbeddingProvider
from app.extraction import DocumentExtractor
from app.models import (
    CitationResponse,
    IngestionRequest,
    IngestionResponse,
    IngestionStatus,
    InternalSearchResult,
    SearchRequest,
    SearchResponse,
)
from app.repository import RagRepository
from app.storage import DocumentStorage


class IngestionService:
    def __init__(
        self,
        repository: RagRepository,
        chunker: CharacterWindowChunker,
        embeddings: EmbeddingProvider,
        storage: DocumentStorage,
        extractor: DocumentExtractor,
    ) -> None:
        self.repository = repository
        self.chunker = chunker
        self.embeddings = embeddings
        self.storage = storage
        self.extractor = extractor

    def ingest(self, request: IngestionRequest) -> IngestionResponse:
        started = time.perf_counter()
        existing = self.repository.get_ingestion(request.job_id)
        if existing and existing.status == "completed":
            return IngestionResponse(
                job_id=request.job_id,
                status="completed",
                chunk_count=existing.chunk_count,
                embedding_version_id=existing.embedding_version_id,
                elapsed_ms=round((time.perf_counter() - started) * 1000, 3),
                correlation_id=request.correlation_id,
            )
        self.repository.begin_ingestion(
            request.job_id, request.document_id, request.document_version_id
        )
        try:
            actual_hash = hashlib.sha256(request.content.encode("utf-8")).hexdigest()
            if actual_hash != request.content_sha256:
                raise ValueError("content hash does not match canonical UTF-8 bytes")
            normalized = self.extractor.extract(request.content, request.media_type)
            self.storage.write(request.document_version_id, request.filename, normalized)
            chunks = self.chunker.chunk(
                request.document_id, request.document_version_id, normalized
            )
            vectors = self.embeddings.embed([chunk.content for chunk in chunks])
            version_id = self.repository.complete_ingestion(
                request.job_id, chunks, vectors, self.embeddings
            )
            return IngestionResponse(
                job_id=request.job_id,
                status="completed",
                chunk_count=len(chunks),
                embedding_version_id=version_id,
                elapsed_ms=round((time.perf_counter() - started) * 1000, 3),
                correlation_id=request.correlation_id,
            )
        except Exception as error:
            self.repository.fail_ingestion(request.job_id, "INGESTION_FAILED", str(error))
            raise

    def status(self, job_id: UUID) -> IngestionStatus | None:
        return self.repository.get_ingestion(job_id)


class RetrievalService:
    def __init__(self, repository: RagRepository, embeddings: EmbeddingProvider) -> None:
        self.repository = repository
        self.embeddings = embeddings

    def search(self, request: SearchRequest) -> SearchResponse:
        started = time.perf_counter()
        vector = self.embeddings.embed([request.query])[0]
        embedding_version_id, rows = self.repository.search(
            request.query,
            vector,
            self.embeddings,
            request.top_k,
            request.document_ids,
            request.document_version_ids,
        )
        results = [
            InternalSearchResult(
                rank=index,
                score=max(-1.0, min(1.0, row.score)),
                document_id=row.document_id,
                document_version_id=row.document_version_id,
                chunk_id=row.chunk_id,
                citation_id=row.citation_id,
                snippet=row.content[:360],
                locator={
                    "kind": "character_range",
                    "start": row.start_offset,
                    "end": row.end_offset,
                },
            )
            for index, row in enumerate(rows, start=1)
        ]
        return SearchResponse(
            query=request.query,
            top_k=request.top_k,
            embedding_version_id=embedding_version_id,
            score_semantics="1 - cosine distance; relative ranking signal, not confidence",
            results=results,
            elapsed_ms=round((time.perf_counter() - started) * 1000, 3),
            correlation_id=request.correlation_id,
        )

    def citation(self, citation_id: UUID) -> CitationResponse | None:
        return self.repository.get_citation(citation_id)
