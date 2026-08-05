from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from typing import Protocol
from uuid import UUID

try:
    import psycopg  # type: ignore[import-not-found]
    from psycopg.rows import dict_row  # type: ignore[import-not-found]
except ImportError:  # Allows pure unit tests before the locked runtime is installed.
    psycopg = None
    dict_row = None

from app.embeddings import EmbeddingProvider, vector_literal
from app.models import ChunkRecord, CitationResponse, IngestionStatus, RepositorySearchRow


class RagRepository(Protocol):
    def begin_ingestion(self, job_id: UUID, document_id: UUID, version_id: UUID) -> None: ...

    def complete_ingestion(
        self,
        job_id: UUID,
        chunks: Sequence[ChunkRecord],
        vectors: Sequence[list[float]],
        provider: EmbeddingProvider,
        source_text: str,
    ) -> UUID: ...

    def fail_ingestion(self, job_id: UUID, code: str, message: str) -> None: ...

    def get_ingestion(self, job_id: UUID) -> IngestionStatus | None: ...

    def search(
        self,
        query: str,
        vector: list[float],
        provider: EmbeddingProvider,
        top_k: int,
        document_ids: list[UUID],
        document_version_ids: list[UUID],
    ) -> tuple[UUID, list[RepositorySearchRow]]: ...

    def get_citation(self, citation_id: UUID) -> CitationResponse | None: ...


class PostgresRagRepository:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def connect(self) -> psycopg.Connection[dict[str, object]]:
        if psycopg is None or dict_row is None:
            raise RuntimeError("psycopg is required for the PostgreSQL runtime")
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def ping(self) -> bool:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector') ok")
            row = cursor.fetchone()
            return bool(row and row["ok"])

    def begin_ingestion(self, job_id: UUID, document_id: UUID, version_id: UUID) -> None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO rag.ingestion_receipts(job_id, document_id, document_version_id, status)
                VALUES (%s, %s, %s, 'running')
                ON CONFLICT (job_id) DO UPDATE SET
                    status = CASE WHEN rag.ingestion_receipts.status = 'completed'
                                  THEN 'completed' ELSE 'running' END,
                    error_code = NULL, error_message = NULL
                """,
                (job_id, document_id, version_id),
            )

    def _embedding_version(
        self, cursor: psycopg.Cursor[dict[str, object]], provider: EmbeddingProvider
    ) -> UUID:
        cursor.execute(
            """
            INSERT INTO rag.embedding_versions(provider, model, dimension, preprocessing_version)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (provider, model, dimension, preprocessing_version)
            DO UPDATE SET model = EXCLUDED.model
            RETURNING id
            """,
            (provider.provider, provider.model, provider.dimension, provider.preprocessing_version),
        )
        row = cursor.fetchone()
        assert row is not None
        return UUID(str(row["id"]))

    def complete_ingestion(
        self,
        job_id: UUID,
        chunks: Sequence[ChunkRecord],
        vectors: Sequence[list[float]],
        provider: EmbeddingProvider,
        source_text: str,
    ) -> UUID:
        if len(chunks) != len(vectors):
            raise ValueError("chunk and vector counts differ")
        with self.connect() as connection, connection.cursor() as cursor:
            embedding_version_id = self._embedding_version(cursor, provider)
            if not chunks:
                raise ValueError("ingestion produced no chunks")
            cursor.execute(
                """
                INSERT INTO rag.document_sources(document_id, document_version_id, content)
                VALUES (%s, %s, %s)
                ON CONFLICT (document_version_id) DO UPDATE SET content=EXCLUDED.content
                """,
                (chunks[0].document_id, chunks[0].document_version_id, source_text),
            )
            for chunk, vector in zip(chunks, vectors, strict=True):
                cursor.execute(
                    """
                    INSERT INTO rag.chunks(
                        id, document_id, document_version_id, chunk_index, chunking_version,
                        content, start_offset, end_offset, locator
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                    ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content,
                        locator = EXCLUDED.locator
                    """,
                    (
                        chunk.id,
                        chunk.document_id,
                        chunk.document_version_id,
                        chunk.chunk_index,
                        chunk.chunking_version,
                        chunk.content,
                        chunk.start_offset,
                        chunk.end_offset,
                        json.dumps(chunk.locator),
                    ),
                )
                cursor.execute(
                    """
                    INSERT INTO rag.chunk_embeddings(chunk_id, embedding_version_id, embedding)
                    VALUES (%s, %s, %s::vector)
                    ON CONFLICT (chunk_id, embedding_version_id)
                    DO UPDATE SET embedding = EXCLUDED.embedding
                    """,
                    (chunk.id, embedding_version_id, vector_literal(vector)),
                )
            cursor.execute(
                """
                UPDATE rag.ingestion_receipts
                SET status = 'completed', chunk_count = %s, embedding_version_id = %s,
                    completed_at = now(), error_code = NULL, error_message = NULL
                WHERE job_id = %s
                """,
                (len(chunks), embedding_version_id, job_id),
            )
            return embedding_version_id

    def fail_ingestion(self, job_id: UUID, code: str, message: str) -> None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE rag.ingestion_receipts
                SET status='failed', error_code=%s, error_message=%s, completed_at=now()
                WHERE job_id=%s
                """,
                (code, message[:500], job_id),
            )

    def get_ingestion(self, job_id: UUID) -> IngestionStatus | None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM rag.ingestion_receipts WHERE job_id=%s", (job_id,))
            row = cursor.fetchone()
            return IngestionStatus.model_validate(row) if row else None

    def search(
        self,
        query: str,
        vector: list[float],
        provider: EmbeddingProvider,
        top_k: int,
        document_ids: list[UUID],
        document_version_ids: list[UUID],
    ) -> tuple[UUID, list[RepositorySearchRow]]:
        query_hash = __import__("hashlib").sha256(query.encode("utf-8")).hexdigest()
        with self.connect() as connection, connection.cursor() as cursor:
            embedding_version_id = self._embedding_version(cursor, provider)
            filters: list[str] = []
            params: list[object] = [vector_literal(vector), embedding_version_id]
            if document_ids:
                filters.append("c.document_id = ANY(%s::uuid[])")
                params.append([str(value) for value in document_ids])
            if document_version_ids:
                filters.append("c.document_version_id = ANY(%s::uuid[])")
                params.append([str(value) for value in document_version_ids])
            params.append(top_k)
            where_filters = " AND " + " AND ".join(filters) if filters else ""
            cursor.execute(
                f"""
                SELECT c.document_id, c.document_version_id, c.id AS chunk_id, c.content,
                       c.start_offset, c.end_offset,
                       GREATEST(-1, LEAST(1, 1 - (ce.embedding <=> %s::vector)))::float8 AS score
                FROM rag.chunk_embeddings ce
                JOIN rag.chunks c ON c.id = ce.chunk_id
                WHERE ce.embedding_version_id = %s {where_filters}
                ORDER BY ce.embedding <=> %s::vector, c.id
                LIMIT %s
                """,
                [*params[:-1], vector_literal(vector), params[-1]],
            )
            rows = cursor.fetchall()
            results: list[RepositorySearchRow] = []
            for row in rows:
                locator = {
                    "kind": "character_range",
                    "start": row["start_offset"],
                    "end": row["end_offset"],
                }
                snippet = str(row["content"])[:360]
                cursor.execute(
                    """
                    INSERT INTO rag.citations(query_hash, chunk_id, score, snippet, locator)
                    VALUES (%s, %s, %s, %s, %s::jsonb)
                    ON CONFLICT (query_hash, chunk_id)
                    DO UPDATE SET
                        score=EXCLUDED.score,
                        snippet=EXCLUDED.snippet,
                        locator=EXCLUDED.locator
                    RETURNING id
                    """,
                    (query_hash, row["chunk_id"], row["score"], snippet, json.dumps(locator)),
                )
                citation = cursor.fetchone()
                assert citation is not None
                results.append(
                    RepositorySearchRow(
                        **row,
                        citation_id=citation["id"],
                    )
                )
            return embedding_version_id, results

    def get_citation(self, citation_id: UUID) -> CitationResponse | None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT ci.id AS citation_id, c.document_id, c.document_version_id,
                       c.id AS chunk_id, ci.score, ci.snippet, c.content, ci.locator
                FROM rag.citations ci
                JOIN rag.chunks c ON c.id=ci.chunk_id
                WHERE ci.id=%s
                """,
                (citation_id,),
            )
            row = cursor.fetchone()
            return CitationResponse.model_validate(row) if row else None


class InMemoryRagRepository:
    """Deterministic test double; never used by runtime configuration."""

    def __init__(self) -> None:
        self.receipts: dict[UUID, IngestionStatus] = {}
        self.chunks: list[tuple[ChunkRecord, list[float]]] = []
        self.citations: dict[UUID, CitationResponse] = {}
        self.embedding_version_id = UUID("00000000-0000-0000-0000-000000000501")

    def begin_ingestion(self, job_id: UUID, document_id: UUID, version_id: UUID) -> None:
        self.receipts[job_id] = IngestionStatus(
            job_id=job_id,
            status="running",
            chunk_count=0,
            started_at=datetime.now().astimezone(),
        )

    def complete_ingestion(
        self,
        job_id: UUID,
        chunks: Sequence[ChunkRecord],
        vectors: Sequence[list[float]],
        provider: EmbeddingProvider,
        source_text: str,
    ) -> UUID:
        self.chunks = list(zip(chunks, vectors, strict=True))
        current = self.receipts[job_id]
        self.receipts[job_id] = current.model_copy(
            update={
                "status": "completed",
                "chunk_count": len(chunks),
                "embedding_version_id": self.embedding_version_id,
                "completed_at": datetime.now().astimezone(),
            }
        )
        return self.embedding_version_id

    def fail_ingestion(self, job_id: UUID, code: str, message: str) -> None:
        current = self.receipts[job_id]
        self.receipts[job_id] = current.model_copy(
            update={
                "status": "failed",
                "error_code": code,
                "completed_at": datetime.now().astimezone(),
            }
        )

    def get_ingestion(self, job_id: UUID) -> IngestionStatus | None:
        return self.receipts.get(job_id)

    def search(
        self,
        query: str,
        vector: list[float],
        provider: EmbeddingProvider,
        top_k: int,
        document_ids: list[UUID],
        document_version_ids: list[UUID],
    ) -> tuple[UUID, list[RepositorySearchRow]]:
        import hashlib
        import math
        from uuid import uuid5

        query_hash = hashlib.sha256(query.encode()).hexdigest()
        ranked: list[tuple[float, ChunkRecord]] = []
        for chunk, candidate in self.chunks:
            if document_ids and chunk.document_id not in document_ids:
                continue
            if document_version_ids and chunk.document_version_id not in document_version_ids:
                continue
            score = sum(a * b for a, b in zip(vector, candidate, strict=True))
            denominator = math.sqrt(sum(a * a for a in vector)) * math.sqrt(
                sum(b * b for b in candidate)
            )
            ranked.append((score / denominator if denominator else 0.0, chunk))
        ranked.sort(key=lambda item: (-item[0], str(item[1].id)))
        results: list[RepositorySearchRow] = []
        for score, chunk in ranked[:top_k]:
            citation_id = uuid5(chunk.id, query_hash)
            locator = {
                "kind": "character_range",
                "start": chunk.start_offset,
                "end": chunk.end_offset,
            }
            citation = CitationResponse(
                citation_id=citation_id,
                document_id=chunk.document_id,
                document_version_id=chunk.document_version_id,
                chunk_id=chunk.id,
                score=score,
                snippet=chunk.content[:360],
                content=chunk.content,
                locator=locator,
            )
            self.citations[citation_id] = citation
            results.append(
                RepositorySearchRow(
                    document_id=chunk.document_id,
                    document_version_id=chunk.document_version_id,
                    chunk_id=chunk.id,
                    content=chunk.content,
                    start_offset=chunk.start_offset,
                    end_offset=chunk.end_offset,
                    score=score,
                    citation_id=citation_id,
                )
            )
        return self.embedding_version_id, results

    def get_citation(self, citation_id: UUID) -> CitationResponse | None:
        return self.citations.get(citation_id)
