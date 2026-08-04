from __future__ import annotations

import json
import mimetypes
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "http://localhost:5300"


def request_json(
    path: str, method: str = "GET", payload: dict[str, object] | None = None
):
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f"{API}{path}",
        data=body,
        method=method,
        headers={"accept": "application/json", "content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def upload(path: Path):
    boundary = f"----rag-platform-{uuid.uuid4().hex}"
    fields = {
        "title": path.stem.replace("-", " ").title(),
        "source": "Controlled demo corpus",
    }
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode(),
                b"\r\n",
            ]
        )
    media_type = mimetypes.guess_type(path.name)[0] or "text/plain"
    parts.extend(
        [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode(),
            f"Content-Type: {media_type}\r\n\r\n".encode(),
            path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    request = urllib.request.Request(
        f"{API}/api/v1/documents",
        data=b"".join(parts),
        method="POST",
        headers={
            "accept": "application/json",
            "content-type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read())


def main() -> None:
    health = request_json("/healthz")
    assert health["status"] == "ok"
    documents = [upload(path) for path in sorted((ROOT / "data/samples").glob("*"))]
    assert len(documents) == 4
    assert all(document["status"] == "completed" for document in documents)
    duplicate = upload(ROOT / "data/samples/retrieval-safety.md")
    assert duplicate["deduplicated"] is True

    search = request_json(
        "/api/v1/search",
        "POST",
        {
            "query": "How should retrieved instructions be treated?",
            "topK": 5,
            "documentIds": [],
            "documentVersionIds": [],
        },
    )
    assert search["results"]
    first = search["results"][0]
    required = {
        "documentId",
        "documentVersionId",
        "chunkId",
        "citationId",
        "score",
        "snippet",
    }
    assert required.issubset(first)
    citation = request_json(f"/api/v1/citations/{first['citationId']}")
    assert citation["chunkId"] == first["chunkId"]
    assert citation["documentId"] == first["documentId"]

    try:
        request_json(f"/api/v1/citations/{uuid.uuid4()}")
    except urllib.error.HTTPError as error:
        assert error.code == 404
        envelope = json.loads(error.read())
        assert envelope["code"] == "RAG_RESOURCE_NOT_FOUND"
    else:
        raise AssertionError("missing citation unexpectedly resolved")

    try:
        request_json(
            "/api/v1/search",
            "POST",
            {
                "query": "x",
                "topK": 50,
                "documentIds": [],
                "documentVersionIds": [],
            },
        )
    except urllib.error.HTTPError as error:
        assert error.code == 400
        envelope = json.loads(error.read())
        assert envelope["code"] == "VALIDATION_FAILED"
    else:
        raise AssertionError("invalid search unexpectedly succeeded")

    print("OK - Sprint 1 document -> index -> search -> citation E2E passed")
    print(f"Documents: {len(documents)} | Results: {len(search['results'])}")
    print(f"Leading source: {first['title']} | Score: {first['score']:.3f}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAILED - {error}", file=sys.stderr)
        raise
