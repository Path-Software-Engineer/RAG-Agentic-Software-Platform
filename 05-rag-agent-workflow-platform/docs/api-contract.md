# HTTP Contract — Sprint 2

Public base path: `/api/v1`

Internal base path: `/internal/v1`

## Public NestJS resources

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/documents` | Upload and index one controlled UTF-8 document idempotently |
| `GET` | `/documents` | List document metadata and ingestion status |
| `GET` | `/documents/{documentId}` | Resolve one document resource |
| `POST` | `/documents/{documentId}/index` | Confirm a completed index state |
| `POST` | `/search` | Execute bounded exact vector search |
| `GET` | `/citations/{citationId}` | Resolve a result to durable evidence |
| `GET` | `/evaluations/strategies` | List versioned chunking strategies |
| `GET`, `POST` | `/evaluations/test-cases` | List or create document-level ground truth |
| `GET`, `POST` | `/evaluations/runs` | List summaries or execute a comparison |
| `GET` | `/evaluations/runs/{runId}` | Resolve one complete run snapshot |
| `PATCH` | `/evaluations/runs/{runId}/results/{resultId}/relevance` | Record a manual relevance review and recalculate metrics |

Swagger UI is served at `/api/docs`; machine-readable OpenAPI is served at `/api/openapi.json`.

## Internal FastAPI resources

FastAPI mirrors the retrieval-evaluation resources beneath `/internal/v1/evaluations` using snake_case fields. It additionally owns ingestion, exact retrieval, and citation resolution. These routes are private service contracts and are not called by the browser.

## Evaluation request rules

- a test case contains a 2–500 character query, one or more relevant document UUIDs, and a rationale;
- a run contains 1–5 unique strategy IDs, up to 100 test cases, up to 100 document versions, and `topK` from 1 through 10;
- omitting test-case or document-version filters selects all available evidence;
- every run returns complete strategy metrics and per-query ranked results;
- a relevance review contains a boolean judgment and optional notes of at most 500 characters;
- public JSON uses camelCase; internal JSON uses snake_case.

## Cross-cutting rules

- `x-correlation-id` is accepted or generated and propagated across service boundaries;
- timestamps are UTC ISO 8601;
- errors use `{ code, message, details, correlationId }` with sanitized details;
- HTTP clients have explicit timeouts;
- contract fixtures live in `packages/contracts/fixtures/`;
- OpenAPI 0.2.0 contracts are generated from running application metadata;
- the Svelte client consumes public resource types through one adapter module.
