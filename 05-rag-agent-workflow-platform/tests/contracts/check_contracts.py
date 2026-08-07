from __future__ import annotations

import json
import re
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
    agent_run = json.loads(
        (ROOT / "packages/contracts/fixtures/agent-run-request.json").read_text(
            encoding="utf-8"
        )
    )
    security = json.loads(
        (ROOT / "packages/contracts/fixtures/security-scenarios.json").read_text(
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
    assert set(agent_run) == {
        "goal",
        "workflowId",
        "documentVersionIds",
        "allowedToolNames",
        "budget",
        "idempotencyKey",
    }
    assert agent_run["workflowId"] == "bounded-research-v1"
    assert agent_run["allowedToolNames"] == ["semantic_search"]
    assert agent_run["budget"]["maxSteps"] <= 16
    assert security["policyVersion"] == "agent-policy/1.0"
    assert {item["category"] for item in security["scenarios"]} == {
        "benign",
        "prompt_injection",
        "tool_abuse",
        "data_exfiltration",
        "denial_of_wallet",
    }
    schema = json.loads(
        (ROOT / "packages/contracts/schemas/evaluation-run.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["additionalProperties"] is False
    for name in (
        "agent-run.schema.json",
        "agent-trace-event.schema.json",
        "tool-definition.schema.json",
        "security-evaluation.schema.json",
    ):
        contract = json.loads(
            (ROOT / "packages/contracts/schemas" / name).read_text(encoding="utf-8")
        )
        assert contract["$schema"].endswith("2020-12/schema")
        assert contract["additionalProperties"] is False


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
        "api/v1/agents",
        "runs/:runId/trace",
        "runs/:runId/events",
        "runs/:runId/cancel",
        "api/v1/security",
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
        "/internal/v1/agents/tools",
        "/internal/v1/agents/runs",
        "/internal/v1/agents/runs/{run_id}/trace",
        "/internal/v1/agents/runs/{run_id}/events",
        "/internal/v1/agents/runs/{run_id}/cancel",
        "/internal/v1/security/evaluations",
    ):
        assert route in internal_source


def test_sprint_boundary_contains_agent_trace_runtime_but_no_sprint_four() -> None:
    project_paths = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*")}
    required = (
        "backend/nestjs-api/src/agents/agents.module.ts",
        "ai-services/rag-agent-service/app/agents.py",
        "frontend/sveltekit-app/src/routes/agents/+page.svelte",
        "database/migrations/003_sprint_03_agent_trace_viewer.sql",
    )
    assert set(required).issubset(project_paths)
    forbidden = (
        "sprint-04",
        "29-agentic-workflow-langgraph-lab",
        "llm-evaluation-suite",
    )
    assert not any(
        token in path.lower() for path in project_paths for token in forbidden
    )


def test_generated_openapi_contracts_are_structurally_valid() -> None:
    contracts = ROOT / "packages/contracts/openapi"
    public = json.loads((contracts / "public-v1.json").read_text(encoding="utf-8"))
    internal = json.loads((contracts / "internal-v1.json").read_text(encoding="utf-8"))
    assert public["info"]["version"] == "1.0.0"
    assert internal["info"]["version"] == "1.0.0"
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
        "/api/v1/agents/tools",
        "/api/v1/agents/runs",
        "/api/v1/agents/runs/{runId}",
        "/api/v1/agents/runs/{runId}/trace",
        "/api/v1/agents/runs/{runId}/events",
        "/api/v1/agents/runs/{runId}/cancel",
        "/api/v1/security/evaluations",
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
        "/internal/v1/agents/tools",
        "/internal/v1/agents/runs",
        "/internal/v1/agents/runs/{run_id}",
        "/internal/v1/agents/runs/{run_id}/trace",
        "/internal/v1/agents/runs/{run_id}/events",
        "/internal/v1/agents/runs/{run_id}/cancel",
        "/internal/v1/security/evaluations",
    }.issubset(internal["paths"])
    _resolve_local_refs(public)
    _resolve_local_refs(internal)


def test_local_and_container_build_bootstrap_is_reproducible() -> None:
    setup = (ROOT / "scripts/setup.ps1").read_text(encoding="utf-8")
    web_dockerfile = (ROOT / "frontend/sveltekit-app/Dockerfile").read_text(
        encoding="utf-8"
    )
    assert setup.index("ensurepip --upgrade") < setup.index("pip --version")
    assert "@rolldown/binding-linux-x64-musl@1.2.2" in web_dockerfile
    assert "--package-lock=false" in web_dockerfile


def test_sprint_three_documentation_is_traceable() -> None:
    required = (
        "docs/event-contract.md",
        "docs/trace-contract.md",
        "docs/runbook.md",
        "docs/deployment-notes.md",
        "docs/sprints/sprint-03-agent-trace-viewer/README.md",
        "docs/sprints/sprint-03-agent-trace-viewer/demo-script.md",
        "docs/sprints/sprint-03-agent-trace-viewer/release-notes-draft.md",
        "docs/sprints/sprint-03-agent-trace-viewer/retrospective.md",
        "reports/security/sprint-03-security-evaluation.md",
    )
    assert all((ROOT / path).is_file() for path in required)
    for week in range(1, 5):
        base = ROOT / f"docs/sprints/sprint-03-agent-trace-viewer/week-{week:02d}"
        assert (base / "exploration.md").is_file()
        assert (base / "review.md").is_file()

    user_stories = (ROOT / "docs/user-stories.md").read_text(encoding="utf-8")
    technical_stories = (ROOT / "docs/technical-stories.md").read_text(encoding="utf-8")
    declared = set(re.findall(r"^## (US-\d+)", user_stories, re.MULTILINE))
    related = set(re.findall(r"US-\d+", technical_stories))
    assert {"US-506", "US-507", "US-508"}.issubset(declared)
    assert related.issubset(declared)


if __name__ == "__main__":
    test_contract_fixtures_are_versioned_and_bounded()
    test_public_and_internal_routes_are_declared_in_source()
    test_sprint_boundary_contains_agent_trace_runtime_but_no_sprint_four()
    test_generated_openapi_contracts_are_structurally_valid()
    test_local_and_container_build_bootstrap_is_reproducible()
    test_sprint_three_documentation_is_traceable()
    print("OK - Sprint 3 contract, trace and boundary checks passed")
