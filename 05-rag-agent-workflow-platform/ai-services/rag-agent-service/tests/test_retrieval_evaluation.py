from __future__ import annotations

from uuid import UUID

import pytest

from app.embeddings import DeterministicHashEmbeddingProvider
from app.evaluation import EvaluationService, InMemoryEvaluationRepository
from app.models import (
    EvaluationRunRequest,
    EvaluationTestCaseCreate,
    RelevanceLabelRequest,
    SourceDocument,
)

SAFETY_DOCUMENT_ID = UUID("00000000-0000-0000-0000-000000000201")
SAFETY_VERSION_ID = UUID("00000000-0000-0000-0000-000000000202")
CHUNKING_DOCUMENT_ID = UUID("00000000-0000-0000-0000-000000000203")
CHUNKING_VERSION_ID = UUID("00000000-0000-0000-0000-000000000204")
CORRELATION_ID = UUID("00000000-0000-0000-0000-000000000205")


def build_service() -> tuple[EvaluationService, InMemoryEvaluationRepository]:
    repository = InMemoryEvaluationRepository(
        [
            SourceDocument(
                document_id=SAFETY_DOCUMENT_ID,
                document_version_id=SAFETY_VERSION_ID,
                content=(
                    "Retrieved instructions are untrusted evidence. Safety policy and "
                    "system guardrails must remain authoritative. Citations preserve provenance."
                ),
            ),
            SourceDocument(
                document_id=CHUNKING_DOCUMENT_ID,
                document_version_id=CHUNKING_VERSION_ID,
                content=(
                    "Chunking divides a document into overlapping context windows. "
                    "The overlap and boundary determine how fragments preserve local context."
                ),
            ),
        ]
    )
    return EvaluationService(repository, DeterministicHashEmbeddingProvider()), repository


def test_strategy_catalog_is_versioned_and_bounded() -> None:
    service, _ = build_service()
    strategies = service.list_strategies()
    assert [item.strategy_id for item in strategies] == [
        "compact-320",
        "balanced-520",
        "broad-760",
    ]
    assert all(item.overlap < item.chunk_size for item in strategies)


def test_evaluation_run_produces_reproducible_bounded_metrics() -> None:
    service, repository = build_service()
    case = service.create_test_case(
        EvaluationTestCaseCreate(
            query="How must retrieved instructions be treated under safety policy?",
            relevant_document_ids=[SAFETY_DOCUMENT_ID],
            rationale="The safety source contains the explicit evidence boundary.",
        )
    )
    run = service.run(
        EvaluationRunRequest(
            strategy_ids=["compact-320", "balanced-520", "broad-760"],
            test_case_ids=[case.test_case_id],
            document_version_ids=[SAFETY_VERSION_ID, CHUNKING_VERSION_ID],
            top_k=2,
            correlation_id=CORRELATION_ID,
        )
    )

    assert run.status == "completed"
    assert len(run.strategies) == 3
    assert run.correlation_id == CORRELATION_ID
    assert run.strategy_ids == ["compact-320", "balanced-520", "broad-760"]
    assert run.test_case_ids == [case.test_case_id]
    assert set(run.document_version_ids) == {SAFETY_VERSION_ID, CHUNKING_VERSION_ID}
    assert run.embedding_version == "local:deterministic-hash-v1:128:canonical-text-v1"
    assert "not confidence" in run.score_semantics
    for strategy in run.strategies:
        assert strategy.metrics.query_count == 1
        assert 0 <= strategy.metrics.precision_at_k <= 1
        assert 0 <= strategy.metrics.recall_at_k <= 1
        assert 0 <= strategy.metrics.hit_rate <= 1
        assert len(strategy.queries[0].results) == 2
        assert strategy.queries[0].expected_document_ids == [SAFETY_DOCUMENT_ID]

    summaries = repository.list_runs()
    assert summaries[0].run_id == run.run_id
    assert summaries[0].strategy_count == 3


def test_manual_relevance_label_is_auditable_and_recalculates_metrics() -> None:
    service, _ = build_service()
    case = service.create_test_case(
        EvaluationTestCaseCreate(
            query="What does chunk overlap preserve?",
            relevant_document_ids=[CHUNKING_DOCUMENT_ID],
            rationale="The chunking source defines overlap and context preservation.",
        )
    )
    run = service.run(
        EvaluationRunRequest(
            strategy_ids=["balanced-520"],
            test_case_ids=[case.test_case_id],
            document_version_ids=[SAFETY_VERSION_ID, CHUNKING_VERSION_ID],
            top_k=2,
            correlation_id=CORRELATION_ID,
        )
    )
    hit = run.strategies[0].queries[0].results[0]
    expected_before = run.strategies[0].queries[0].expected_document_ids

    updated = service.label(
        run.run_id,
        hit.result_id,
        RelevanceLabelRequest(
            relevant=False,
            notes="Reviewed against the controlled source.",
            correlation_id=CORRELATION_ID,
        ),
    )

    assert updated is not None
    labelled = updated.strategies[0].queries[0].results[0]
    assert labelled.relevant is False
    assert labelled.relevance_source == "manual"
    assert labelled.relevance_notes == "Reviewed against the controlled source."
    assert updated.strategies[0].queries[0].expected_document_ids == expected_before


def test_evaluation_rejects_unknown_strategy_and_missing_evidence() -> None:
    service, _ = build_service()
    with pytest.raises(ValueError, match="unknown chunking strategy"):
        service.run(
            EvaluationRunRequest(
                strategy_ids=["unknown"],
                top_k=3,
                correlation_id=CORRELATION_ID,
            )
        )

    with pytest.raises(ValueError, match="test case"):
        service.run(
            EvaluationRunRequest(
                strategy_ids=["balanced-520"],
                top_k=3,
                correlation_id=CORRELATION_ID,
            )
        )

    case = service.create_test_case(
        EvaluationTestCaseCreate(
            query="What does chunk overlap preserve?",
            relevant_document_ids=[CHUNKING_DOCUMENT_ID],
            rationale="The chunking source defines the expected evidence.",
        )
    )
    with pytest.raises(ValueError, match="outside the selected corpus"):
        service.run(
            EvaluationRunRequest(
                strategy_ids=["balanced-520"],
                test_case_ids=[case.test_case_id],
                document_version_ids=[SAFETY_VERSION_ID],
                top_k=3,
                correlation_id=CORRELATION_ID,
            )
        )
