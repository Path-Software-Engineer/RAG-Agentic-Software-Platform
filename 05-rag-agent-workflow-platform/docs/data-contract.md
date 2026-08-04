# Data Contract — Semantic Search 1.0

## Canonical document

- `document_id`: opaque UUID owned by `app.documents`.
- `document_version_id`: immutable UUID for one uploaded byte sequence.
- `content_sha256`: lowercase SHA-256 used for deduplication.
- `media_type`: allowlisted real type (`text/plain` or `text/markdown`).
- `byte_size`: positive and no greater than the configured boundary.
- original content is stored outside database metadata and never returned by list endpoints.

## Chunk

- `chunk_id`: UUIDv5 of document-version ID and chunk index.
- `chunk_index`: zero-based order within the version.
- `content`: canonical UTF-8 fragment.
- `start_offset`, `end_offset`: offsets in canonical text.
- `locator`: `{ "kind": "character_range", "start": n, "end": n }`.
- `chunking_version`: `char-window-v1`.

## Embedding version

- provider, model, dimension, preprocessing version, and UTC creation time are mandatory;
- an embedding is written idempotently for `(chunk_id, embedding_version_id)`;
- vectors from different versions are never compared in one logical query;
- Sprint 1 persists dimension 128 because the migration and provider are locked together.

## Search result and citation

Every result contains `document_id`, `document_version_id`, `chunk_id`, `citation_id`, rank, score, snippet, title, source, and locator. `score` is `1 - cosine_distance`, clamped to `[-1, 1]`; it is not a probability or correctness claim.

A citation resolves through `citation_id` to the same durable identifiers. If the referenced chunk cannot be resolved, the API must return a controlled not-found response rather than incomplete provenance.
