from __future__ import annotations

import hashlib
from uuid import UUID

import pytest

from app.chunking import CharacterWindowChunker
from app.embeddings import DeterministicHashEmbeddingProvider
from app.extraction import ControlledTextExtractor
from app.models import IngestionRequest, SearchRequest
from app.normalization import normalize_text
from app.repository import InMemoryRagRepository
from app.services import IngestionService, RetrievalService

DOCUMENT_ID = UUID("00000000-0000-0000-0000-000000000101")
VERSION_ID = UUID("00000000-0000-0000-0000-000000000102")
JOB_ID = UUID("00000000-0000-0000-0000-000000000103")
CORRELATION_ID = UUID("00000000-0000-0000-0000-000000000104")


class MemoryStorage:
    def __init__(self) -> None:
        self.values: dict[UUID, str] = {}

    def write(self, version_id: UUID, filename: str, content: str) -> None:
        self.values[version_id] = content


def test_normalization_preserves_paragraphs_and_is_deterministic() -> None:
    assert normalize_text("Title\r\n\r\n\tOne   idea.\n\n\nTwo.") == "Title\n\nOne idea.\n\nTwo."


def test_normalization_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="visible"):
        normalize_text(" \n\t")


def test_chunking_preserves_provenance_and_overlap() -> None:
    text = " ".join(f"concept-{index}" for index in range(100))
    chunks = CharacterWindowChunker(160, 24).chunk(DOCUMENT_ID, VERSION_ID, text)
    assert len(chunks) > 1
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.document_version_id == VERSION_ID for chunk in chunks)
    assert all(chunk.end_offset > chunk.start_offset for chunk in chunks)
    assert len({chunk.id for chunk in chunks}) == len(chunks)


def test_deterministic_embedding_is_stable_and_normalized() -> None:
    provider = DeterministicHashEmbeddingProvider()
    first, second = provider.embed(["citation provenance", "citation provenance"])
    assert first == second
    assert len(first) == 128
    assert sum(value * value for value in first) == pytest.approx(1.0, abs=1e-8)


def test_ingestion_and_search_resolve_a_citation() -> None:
    repository = InMemoryRagRepository()
    embeddings = DeterministicHashEmbeddingProvider()
    ingestion = IngestionService(
        repository,
        CharacterWindowChunker(180, 30),
        embeddings,
        MemoryStorage(),
        ControlledTextExtractor(),
    )
    content = (
        "Retrieved instructions are untrusted evidence and never replace system policy. "
        "Every citation must resolve to one durable chunk and document version."
    )
    response = ingestion.ingest(
        IngestionRequest(
            job_id=JOB_ID,
            document_id=DOCUMENT_ID,
            document_version_id=VERSION_ID,
            filename="safety.md",
            media_type="text/markdown",
            content=content,
            content_sha256=hashlib.sha256(content.encode()).hexdigest(),
            correlation_id=CORRELATION_ID,
        )
    )
    assert response.status == "completed"
    assert response.chunk_count == 1

    retrieval = RetrievalService(repository, embeddings)
    results = retrieval.search(
        SearchRequest(
            query="How should retrieved instructions be treated?",
            top_k=3,
            correlation_id=CORRELATION_ID,
        )
    )
    assert len(results.results) == 1
    assert results.results[0].document_id == DOCUMENT_ID
    assert retrieval.citation(results.results[0].citation_id) is not None

    wrong_version = retrieval.search(
        SearchRequest(
            query="How should retrieved instructions be treated?",
            top_k=3,
            document_version_ids=[UUID("00000000-0000-0000-0000-000000000999")],
            correlation_id=CORRELATION_ID,
        )
    )
    assert wrong_version.results == []


def test_ingestion_rejects_hash_mismatch() -> None:
    repository = InMemoryRagRepository()
    service = IngestionService(
        repository,
        CharacterWindowChunker(180, 30),
        DeterministicHashEmbeddingProvider(),
        MemoryStorage(),
        ControlledTextExtractor(),
    )
    with pytest.raises(ValueError, match="hash"):
        service.ingest(
            IngestionRequest(
                job_id=JOB_ID,
                document_id=DOCUMENT_ID,
                document_version_id=VERSION_ID,
                filename="bad.txt",
                media_type="text/plain",
                content="visible",
                content_sha256="0" * 64,
                correlation_id=CORRELATION_ID,
            )
        )
    assert repository.get_ingestion(JOB_ID).status == "failed"  # type: ignore[union-attr]
