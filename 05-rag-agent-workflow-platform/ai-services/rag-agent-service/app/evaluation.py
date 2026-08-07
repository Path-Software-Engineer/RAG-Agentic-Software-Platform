from __future__ import annotations

import json
import math
import time
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4, uuid5

try:
    import psycopg  # type: ignore[import-not-found]
    from psycopg.rows import dict_row  # type: ignore[import-not-found]
except ImportError:  # Allows isolated unit tests before runtime dependencies are installed.
    psycopg = None
    dict_row = None

from app.chunking import CharacterWindowChunker
from app.embeddings import EmbeddingProvider
from app.models import (
    ChunkingStrategyResource,
    EvaluationHit,
    EvaluationQueryResult,
    EvaluationRunRequest,
    EvaluationRunResource,
    EvaluationRunSummary,
    EvaluationStrategyResult,
    EvaluationTestCaseCreate,
    EvaluationTestCaseResource,
    RelevanceLabelRequest,
    SourceDocument,
    StrategyMetrics,
)

STRATEGIES = (
    ChunkingStrategyResource(
        strategy_id="compact-320",
        label="Compact context",
        description="Short windows favor precise matches while producing more chunks.",
        chunk_size=320,
        overlap=48,
        boundary="natural-character-window",
    ),
    ChunkingStrategyResource(
        strategy_id="balanced-520",
        label="Balanced context",
        description="Medium windows balance local precision with enough surrounding evidence.",
        chunk_size=520,
        overlap=80,
        boundary="natural-character-window",
    ),
    ChunkingStrategyResource(
        strategy_id="broad-760",
        label="Broad context",
        description="Long windows preserve more context while reducing the number of chunks.",
        chunk_size=760,
        overlap=120,
        boundary="natural-character-window",
    ),
)


class EvaluationRepository(Protocol):
    def create_test_case(self, payload: EvaluationTestCaseCreate) -> EvaluationTestCaseResource: ...

    def list_test_cases(self, ids: list[UUID]) -> list[EvaluationTestCaseResource]: ...

    def list_sources(self, version_ids: list[UUID]) -> list[SourceDocument]: ...

    def save_run(self, run: EvaluationRunResource) -> None: ...

    def list_runs(self) -> list[EvaluationRunSummary]: ...

    def get_run(self, run_id: UUID) -> EvaluationRunResource | None: ...

    def replace_run_after_label(
        self,
        run: EvaluationRunResource,
        result_id: UUID,
        label: RelevanceLabelRequest,
    ) -> None: ...


def _summary(run: EvaluationRunResource) -> EvaluationRunSummary:
    metrics = sorted(
        (item.metrics for item in run.strategies),
        key=lambda item: (
            -item.recall_at_k,
            -item.precision_at_k,
            -item.mean_reciprocal_rank,
            item.chunk_count,
            item.strategy_id,
        ),
    )[0]
    return EvaluationRunSummary(
        run_id=run.run_id,
        top_k=run.top_k,
        strategy_count=len(run.strategies),
        query_count=metrics.query_count,
        best_strategy_id=metrics.strategy_id,
        best_recall_at_k=metrics.recall_at_k,
        created_at=run.created_at,
    )


class PostgresEvaluationRepository:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def connect(self) -> psycopg.Connection[dict[str, object]]:
        if psycopg is None or dict_row is None:
            raise RuntimeError("psycopg is required for the PostgreSQL runtime")
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def create_test_case(self, payload: EvaluationTestCaseCreate) -> EvaluationTestCaseResource:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO rag.retrieval_test_cases(query, relevant_document_ids, rationale)
                VALUES (%s, %s::uuid[], %s)
                RETURNING id AS test_case_id, query, relevant_document_ids, rationale, created_at
                """,
                (
                    payload.query,
                    [str(value) for value in payload.relevant_document_ids],
                    payload.rationale,
                ),
            )
            row = cursor.fetchone()
            assert row is not None
            return EvaluationTestCaseResource.model_validate(row)

    def list_test_cases(self, ids: list[UUID]) -> list[EvaluationTestCaseResource]:
        with self.connect() as connection, connection.cursor() as cursor:
            if ids:
                cursor.execute(
                    """
                    SELECT id AS test_case_id, query, relevant_document_ids, rationale, created_at
                    FROM rag.retrieval_test_cases WHERE id=ANY(%s::uuid[]) ORDER BY created_at, id
                    """,
                    ([str(value) for value in ids],),
                )
            else:
                cursor.execute(
                    """
                    SELECT id AS test_case_id, query, relevant_document_ids, rationale, created_at
                    FROM rag.retrieval_test_cases ORDER BY created_at, id
                    """
                )
            return [EvaluationTestCaseResource.model_validate(row) for row in cursor.fetchall()]

    def list_sources(self, version_ids: list[UUID]) -> list[SourceDocument]:
        with self.connect() as connection, connection.cursor() as cursor:
            if version_ids:
                cursor.execute(
                    """
                    SELECT document_id, document_version_id, content FROM rag.document_sources
                    WHERE document_version_id=ANY(%s::uuid[])
                    ORDER BY document_id, document_version_id
                    """,
                    ([str(value) for value in version_ids],),
                )
            else:
                cursor.execute(
                    """
                    SELECT document_id, document_version_id, content FROM rag.document_sources
                    ORDER BY document_id, document_version_id
                    """
                )
            return [SourceDocument.model_validate(row) for row in cursor.fetchall()]

    def save_run(self, run: EvaluationRunResource) -> None:
        snapshot = run.model_dump(mode="json")
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO rag.evaluation_runs(
                    id, top_k, strategy_ids, test_case_ids, document_version_ids,
                    status, snapshot, correlation_id, created_at, completed_at
                ) VALUES (%s, %s, %s, %s::uuid[], %s::uuid[], 'completed', %s::jsonb, %s, %s, %s)
                """,
                (
                    run.run_id,
                    run.top_k,
                    run.strategy_ids,
                    [str(value) for value in run.test_case_ids],
                    [str(value) for value in run.document_version_ids],
                    json.dumps(snapshot),
                    run.correlation_id,
                    run.created_at,
                    run.completed_at,
                ),
            )

    def list_runs(self) -> list[EvaluationRunSummary]:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT snapshot FROM rag.evaluation_runs ORDER BY created_at DESC LIMIT 50"
            )
            return [
                _summary(EvaluationRunResource.model_validate(row["snapshot"]))
                for row in cursor.fetchall()
            ]

    def get_run(self, run_id: UUID) -> EvaluationRunResource | None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT snapshot FROM rag.evaluation_runs WHERE id=%s", (run_id,))
            row = cursor.fetchone()
            return EvaluationRunResource.model_validate(row["snapshot"]) if row else None

    def replace_run_after_label(
        self,
        run: EvaluationRunResource,
        result_id: UUID,
        label: RelevanceLabelRequest,
    ) -> None:
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                "UPDATE rag.evaluation_runs SET snapshot=%s::jsonb WHERE id=%s",
                (run.model_dump_json(), run.run_id),
            )
            cursor.execute(
                """
                INSERT INTO rag.relevance_labels(result_id, run_id, relevant, notes, correlation_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (result_id) DO UPDATE SET
                    relevant=EXCLUDED.relevant, notes=EXCLUDED.notes,
                    correlation_id=EXCLUDED.correlation_id, labeled_at=now()
                """,
                (result_id, run.run_id, label.relevant, label.notes, label.correlation_id),
            )


class InMemoryEvaluationRepository:
    def __init__(self, sources: Sequence[SourceDocument] = ()) -> None:
        self.sources = list(sources)
        self.test_cases: dict[UUID, EvaluationTestCaseResource] = {}
        self.runs: dict[UUID, EvaluationRunResource] = {}

    def create_test_case(self, payload: EvaluationTestCaseCreate) -> EvaluationTestCaseResource:
        resource = EvaluationTestCaseResource(
            test_case_id=uuid4(), created_at=datetime.now(UTC), **payload.model_dump()
        )
        self.test_cases[resource.test_case_id] = resource
        return resource

    def list_test_cases(self, ids: list[UUID]) -> list[EvaluationTestCaseResource]:
        selected = (
            self.test_cases.values() if not ids else (self.test_cases.get(value) for value in ids)
        )
        return sorted(
            (item for item in selected if item is not None), key=lambda item: str(item.test_case_id)
        )

    def list_sources(self, version_ids: list[UUID]) -> list[SourceDocument]:
        return [
            item
            for item in self.sources
            if not version_ids or item.document_version_id in version_ids
        ]

    def save_run(self, run: EvaluationRunResource) -> None:
        self.runs[run.run_id] = run

    def list_runs(self) -> list[EvaluationRunSummary]:
        return [
            _summary(item)
            for item in sorted(self.runs.values(), key=lambda item: item.created_at, reverse=True)
        ]

    def get_run(self, run_id: UUID) -> EvaluationRunResource | None:
        return self.runs.get(run_id)

    def replace_run_after_label(
        self,
        run: EvaluationRunResource,
        result_id: UUID,
        label: RelevanceLabelRequest,
    ) -> None:
        self.runs[run.run_id] = run


class EvaluationService:
    def __init__(self, repository: EvaluationRepository, embeddings: EmbeddingProvider) -> None:
        self.repository = repository
        self.embeddings = embeddings
        self.strategies = {item.strategy_id: item for item in STRATEGIES}

    def list_strategies(self) -> list[ChunkingStrategyResource]:
        return list(STRATEGIES)

    def create_test_case(self, payload: EvaluationTestCaseCreate) -> EvaluationTestCaseResource:
        return self.repository.create_test_case(payload)

    def list_test_cases(self) -> list[EvaluationTestCaseResource]:
        return self.repository.list_test_cases([])

    def run(self, request: EvaluationRunRequest) -> EvaluationRunResource:
        started = time.perf_counter()
        strategies = []
        for strategy_id in request.strategy_ids:
            if strategy_id not in self.strategies:
                raise ValueError(f"unknown chunking strategy: {strategy_id}")
            strategies.append(self.strategies[strategy_id])
        cases = self.repository.list_test_cases(request.test_case_ids)
        if not cases:
            raise ValueError("at least one retrieval test case is required")
        if request.test_case_ids and len(cases) != len(request.test_case_ids):
            raise ValueError("one or more retrieval test cases do not exist")
        sources = self.repository.list_sources(request.document_version_ids)
        if not sources:
            raise ValueError("at least one indexed document source is required")
        if request.document_version_ids and len(sources) != len(request.document_version_ids):
            raise ValueError("one or more document versions do not exist")
        source_document_ids = {item.document_id for item in sources}
        if any(not set(case.relevant_document_ids).issubset(source_document_ids) for case in cases):
            raise ValueError("one or more relevant documents are outside the selected corpus")

        run_id = uuid4()
        created_at = datetime.now(UTC)
        strategy_results = [
            self._evaluate_strategy(run_id, strategy, cases, sources, request.top_k)
            for strategy in strategies
        ]
        completed_at = datetime.now(UTC)
        run = EvaluationRunResource(
            run_id=run_id,
            status="completed",
            top_k=request.top_k,
            strategy_ids=request.strategy_ids,
            test_case_ids=[item.test_case_id for item in cases],
            document_version_ids=[item.document_version_id for item in sources],
            embedding_version=(
                f"{self.embeddings.provider}:{self.embeddings.model}:"
                f"{self.embeddings.dimension}:{self.embeddings.preprocessing_version}"
            ),
            score_semantics=(
                "cosine similarity from the configured embedding version; not confidence"
            ),
            metric_semantics=(
                "macro average across the selected test cases; expected document IDs "
                "are the relevance ground truth"
            ),
            strategies=strategy_results,
            created_at=created_at,
            completed_at=completed_at,
            elapsed_ms=round((time.perf_counter() - started) * 1000, 3),
            correlation_id=request.correlation_id,
        )
        self.repository.save_run(run)
        return run

    def list_runs(self) -> list[EvaluationRunSummary]:
        return self.repository.list_runs()

    def get_run(self, run_id: UUID) -> EvaluationRunResource | None:
        return self.repository.get_run(run_id)

    def label(
        self, run_id: UUID, result_id: UUID, payload: RelevanceLabelRequest
    ) -> EvaluationRunResource | None:
        run = self.repository.get_run(run_id)
        if run is None:
            return None
        found = False
        for strategy in run.strategies:
            for query in strategy.queries:
                for index, hit in enumerate(query.results):
                    if hit.result_id != result_id:
                        continue
                    found = True
                    query.results[index] = hit.model_copy(
                        update={
                            "relevant": payload.relevant,
                            "relevance_source": "manual",
                            "relevance_notes": payload.notes,
                        }
                    )
                    self._refresh_query_metrics(query, run.top_k)
            self._refresh_strategy_metrics(strategy)
        if not found:
            raise ValueError("evaluation result does not belong to this run")
        self.repository.replace_run_after_label(run, result_id, payload)
        return run

    def _evaluate_strategy(
        self,
        run_id: UUID,
        strategy: ChunkingStrategyResource,
        cases: list[EvaluationTestCaseResource],
        sources: list[SourceDocument],
        top_k: int,
    ) -> EvaluationStrategyResult:
        chunker = CharacterWindowChunker(
            strategy.chunk_size, strategy.overlap, f"evaluation-{strategy.strategy_id}-v1"
        )
        chunks = [
            chunk
            for source in sources
            for chunk in chunker.chunk(
                source.document_id, source.document_version_id, source.content
            )
        ]
        vectors = self.embeddings.embed([chunk.content for chunk in chunks])
        query_vectors = self.embeddings.embed([case.query for case in cases])
        queries: list[EvaluationQueryResult] = []
        for case, query_vector in zip(cases, query_vectors, strict=True):
            ranked = sorted(
                (
                    (self._cosine(query_vector, vector), chunk)
                    for chunk, vector in zip(chunks, vectors, strict=True)
                ),
                key=lambda item: (-item[0], str(item[1].id)),
            )[:top_k]
            expected = set(case.relevant_document_ids)
            hits = [
                EvaluationHit(
                    result_id=uuid5(
                        run_id,
                        f"{strategy.strategy_id}:{case.test_case_id}:{rank}:{chunk.id}",
                    ),
                    rank=rank,
                    score=max(-1.0, min(1.0, score)),
                    document_id=chunk.document_id,
                    document_version_id=chunk.document_version_id,
                    chunk_id=chunk.id,
                    snippet=chunk.content[:360],
                    locator=chunk.locator,
                    relevant=chunk.document_id in expected,
                )
                for rank, (score, chunk) in enumerate(ranked, start=1)
            ]
            query = EvaluationQueryResult(
                test_case_id=case.test_case_id,
                query=case.query,
                expected_document_ids=case.relevant_document_ids,
                precision_at_k=0,
                recall_at_k=0,
                hit=False,
                reciprocal_rank=0,
                results=hits,
            )
            self._refresh_query_metrics(query, top_k)
            queries.append(query)
        result = EvaluationStrategyResult(
            metrics=StrategyMetrics(
                strategy_id=strategy.strategy_id,
                strategy_label=strategy.label,
                query_count=len(queries),
                chunk_count=len(chunks),
                precision_at_k=0,
                recall_at_k=0,
                hit_rate=0,
                mean_reciprocal_rank=0,
                error_count=0,
            ),
            queries=queries,
        )
        self._refresh_strategy_metrics(result)
        return result

    @staticmethod
    def _cosine(first: list[float], second: list[float]) -> float:
        denominator = math.sqrt(sum(value * value for value in first)) * math.sqrt(
            sum(value * value for value in second)
        )
        return (
            sum(a * b for a, b in zip(first, second, strict=True)) / denominator
            if denominator
            else 0
        )

    @staticmethod
    def _refresh_query_metrics(query: EvaluationQueryResult, top_k: int) -> None:
        relevant_hits = [hit for hit in query.results if hit.relevant]
        expected_count = len(query.expected_document_ids)
        query.precision_at_k = round(len(relevant_hits) / top_k, 6)
        query.recall_at_k = (
            round(min(1.0, len({hit.document_id for hit in relevant_hits}) / expected_count), 6)
            if expected_count
            else 0
        )
        query.hit = bool(relevant_hits)
        query.reciprocal_rank = round(1 / relevant_hits[0].rank, 6) if relevant_hits else 0

    @staticmethod
    def _refresh_strategy_metrics(strategy: EvaluationStrategyResult) -> None:
        query_count = len(strategy.queries)
        strategy.metrics.precision_at_k = round(
            sum(item.precision_at_k for item in strategy.queries) / query_count, 6
        )
        strategy.metrics.recall_at_k = round(
            sum(item.recall_at_k for item in strategy.queries) / query_count, 6
        )
        strategy.metrics.hit_rate = round(
            sum(1 for item in strategy.queries if item.hit) / query_count, 6
        )
        strategy.metrics.mean_reciprocal_rank = round(
            sum(item.reciprocal_rank for item in strategy.queries) / query_count, 6
        )
        strategy.metrics.error_count = sum(1 for item in strategy.queries if item.recall_at_k < 1)
