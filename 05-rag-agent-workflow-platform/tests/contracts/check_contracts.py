from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _resolve_local_refs(document: dict[str, object]) -> None:
    def walk(value: object) -> None:
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str):
                assert reference.startswith("#/"), (
                    f"external reference is not allowed: {reference}"
                )
                target: object = document
                for segment in reference.removeprefix("#/").split("/"):
                    assert isinstance(target, dict) and segment in target, (
                        f"unresolved OpenAPI reference: {reference}"
                    )
                    target = target[segment]
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)


def test_contract_fixtures_are_versioned_and_bounded() -> None:
    ingestion = json.loads(
        (ROOT / "packages/contracts/fixtures/ingestion-request.json").read_text(
            encoding="utf-8"
        )
    )
    search = json.loads(
        (ROOT / "packages/contracts/fixtures/search-request.json").read_text(
            encoding="utf-8"
        )
    )
    evaluation_case = json.loads(
        (
            ROOT / "packages/contracts/fixtures/evaluation-test-case-request.json"
        ).read_text(encoding="utf-8")
    )
    evaluation_run = json.loads(
        (ROOT / "packages/contracts/fixtures/evaluation-run-request.json").read_text(
            encoding="utf-8"
        )
    )
    relevance_label = json.loads(
        (ROOT / "packages/contracts/fixtures/relevance-label-request.json").read_text(
            encoding="utf-8"
        )
    )
    assert set(ingestion) == {
        "job_id",
        "document_id",
        "document_version_id",
        "filename",
        "media_type",
        "content",
        "content_sha256",
        "correlation_id",
    }
    assert ingestion["media_type"] in {"text/plain", "text/markdown"}
    assert len(ingestion["content_sha256"]) == 64
    assert 1 <= search["top_k"] <= 10
    assert len(search["query"]) <= 500
    assert set(search) == {
        "query",
        "top_k",
        "document_ids",
        "document_version_ids",
        "correlation_id",
    }
    assert set(evaluation_case) == {"query", "relevantDocumentIds", "rationale"}
    assert evaluation_case["relevantDocumentIds"]
    assert set(evaluation_run) == {
        "strategyIds",
        "testCaseIds",
        "documentVersionIds",
        "topK",
    }
    assert len(evaluation_run["strategyIds"]) == len(set(evaluation_run["strategyIds"]))
    assert 1 <= evaluation_run["topK"] <= 10
    assert set(relevance_label) == {"relevant", "notes"}
    assert isinstance(relevance_label["relevant"], bool)
    schema = json.loads(
        (ROOT / "packages/contracts/schemas/evaluation-run.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["additionalProperties"] is False


def test_public_and_internal_routes_are_declared_in_source() -> None:
    public_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "backend/nestjs-api/src").rglob("*.controller.ts")
    )
    internal_source = (ROOT / "ai-services/rag-agent-service/app/main.py").read_text(
        encoding="utf-8"
    )
    for route in (
        "api/v1/documents",
        "api/v1",
        "search",
        "citations/:citationId",
        "api/v1/evaluations",
        "runs/:runId",
        "results/:resultId/relevance",
    ):
        assert route in public_source
    for route in (
        "/internal/v1/ingestions",
        "/internal/v1/retrieval/search",
        "/internal/v1/citations/{citation_id}",
        "/internal/v1/evaluations/strategies",
        "/internal/v1/evaluations/test-cases",
        "/internal/v1/evaluations/runs",
        "/internal/v1/evaluations/runs/{run_id}",
        "/internal/v1/evaluations/runs/{run_id}/results/{result_id}/relevance",
    ):
        assert route in internal_source


def test_sprint_boundary_contains_no_agent_runtime_modules() -> None:
    project_paths = {path.as_posix() for path in ROOT.rglob("*")}
    forbidden_runtime_segments = (
        "/src/agents/",
        "/src/traces/",
        "/app/agents/",
        "/app/tools/",
        "/app/tracing/",
    )
    assert not any(
        segment in path
        for path in project_paths
        for segment in forbidden_runtime_segments
    )


def test_generated_openapi_contracts_are_structurally_valid() -> None:
    contracts = ROOT / "packages/contracts/openapi"
    public = json.loads((contracts / "public-v1.json").read_text(encoding="utf-8"))
    internal = json.loads((contracts / "internal-v1.json").read_text(encoding="utf-8"))
    assert public["info"]["version"] == "0.2.0"
    assert internal["info"]["version"] == "0.2.0"
    assert {
        "/api/v1/documents",
        "/api/v1/documents/{documentId}",
        "/api/v1/documents/{documentId}/index",
        "/api/v1/search",
        "/api/v1/citations/{citationId}",
        "/api/v1/evaluations/strategies",
        "/api/v1/evaluations/test-cases",
        "/api/v1/evaluations/runs",
        "/api/v1/evaluations/runs/{runId}",
        "/api/v1/evaluations/runs/{runId}/results/{resultId}/relevance",
    }.issubset(public["paths"])
    assert {
        "/internal/v1/ingestions",
        "/internal/v1/retrieval/search",
        "/internal/v1/citations/{citation_id}",
        "/internal/v1/evaluations/strategies",
        "/internal/v1/evaluations/test-cases",
        "/internal/v1/evaluations/runs",
        "/internal/v1/evaluations/runs/{run_id}",
        "/internal/v1/evaluations/runs/{run_id}/results/{result_id}/relevance",
    }.issubset(internal["paths"])
    _resolve_local_refs(public)
    _resolve_local_refs(internal)


def test_local_and_container_build_bootstrap_is_reproducible() -> None:
    setup = (ROOT / "scripts/setup.ps1").read_text(encoding="utf-8")
    web_dockerfile = (ROOT / "frontend/sveltekit-app/Dockerfile").read_text(
        encoding="utf-8"
    )
    assert setup.index("ensurepip --upgrade") < setup.index("pip --version")
    assert '@rolldown/binding-linux-x64-musl@1.2.2' in web_dockerfile
    assert "--package-lock=false" in web_dockerfile


if __name__ == "__main__":
    test_contract_fixtures_are_versioned_and_bounded()
    test_public_and_internal_routes_are_declared_in_source()
    test_sprint_boundary_contains_no_agent_runtime_modules()
    test_generated_openapi_contracts_are_structurally_valid()
    test_local_and_container_build_bootstrap_is_reproducible()
    print("OK - Sprint 2 contract and boundary checks passed")
