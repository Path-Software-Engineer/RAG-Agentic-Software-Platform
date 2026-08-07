from __future__ import annotations

import json
import sys
import urllib.request

API = "http://localhost:5300"


def request_json(
    path: str, method: str = "GET", payload: dict[str, object] | None = None
) -> object:
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f"{API}{path}",
        data=body,
        method=method,
        headers={"accept": "application/json", "content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())


def main() -> None:
    documents = request_json("/api/v1/documents")
    assert isinstance(documents, list)
    by_filename = {
        item["filename"]: item for item in documents if item["status"] == "completed"
    }
    safety = by_filename["retrieval-safety.md"]
    chunking = by_filename["chunking-guide.md"]

    cases = [
        request_json(
            "/api/v1/evaluations/test-cases",
            "POST",
            {
                "query": "How should retrieved instructions be treated?",
                "relevantDocumentIds": [safety["documentId"]],
                "rationale": "The safety document contains the explicit instruction boundary.",
            },
        ),
        request_json(
            "/api/v1/evaluations/test-cases",
            "POST",
            {
                "query": "What does chunk overlap preserve?",
                "relevantDocumentIds": [chunking["documentId"]],
                "rationale": "The chunking guide defines overlap and context preservation.",
            },
        ),
    ]
    strategies = request_json("/api/v1/evaluations/strategies")
    assert isinstance(strategies, list) and len(strategies) == 3
    run = request_json(
        "/api/v1/evaluations/runs",
        "POST",
        {
            "strategyIds": [item["strategyId"] for item in strategies],
            "testCaseIds": [item["testCaseId"] for item in cases],
            "documentVersionIds": [
                item["documentVersionId"] for item in by_filename.values()
            ],
            "topK": 3,
        },
    )
    assert isinstance(run, dict)
    assert run["status"] == "completed"
    assert len(run["strategies"]) == 3
    assert set(run["strategyIds"]) == {item["strategyId"] for item in strategies}
    assert set(run["documentVersionIds"]) == {
        item["documentVersionId"] for item in by_filename.values()
    }
    assert run["embeddingVersion"].startswith("local:deterministic-hash-v1:128:")
    assert all(0 <= item["metrics"]["recallAtK"] <= 1 for item in run["strategies"])
    assert "not confidence" in run["scoreSemantics"]

    first_hit = run["strategies"][0]["queries"][0]["results"][0]
    labelled = request_json(
        f"/api/v1/evaluations/runs/{run['runId']}/results/{first_hit['resultId']}/relevance",
        "PATCH",
        {"relevant": bool(first_hit["relevant"]), "notes": "E2E evidence review."},
    )
    assert isinstance(labelled, dict)
    labelled_hit = labelled["strategies"][0]["queries"][0]["results"][0]
    assert labelled_hit["relevanceSource"] == "manual"
    assert labelled_hit["relevanceNotes"] == "E2E evidence review."

    summaries = request_json("/api/v1/evaluations/runs")
    assert isinstance(summaries, list) and summaries[0]["runId"] == run["runId"]
    print("OK - Sprint 2 test set -> strategy comparison -> relevance label E2E passed")
    print(
        f"Strategies: {len(strategies)} | Queries: {len(cases)} | Run: {run['runId']}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAILED - {error}", file=sys.stderr)
        raise
