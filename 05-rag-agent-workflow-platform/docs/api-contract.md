# HTTP Contract — Sprint 1

Public base path: `/api/v1`

Internal base path: `/internal/v1`

## Public NestJS resources

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/documents` | Upload one controlled UTF-8 text document and index it idempotently |
| `GET` | `/documents` | List document metadata and ingestion status |
| `GET` | `/documents/{documentId}` | Resolve one document resource |
| `POST` | `/documents/{documentId}/index` | Confirm the completed index state idempotently; failed uploads require a controlled re-upload |
| `POST` | `/search` | Execute bounded exact vector search |
| `GET` | `/citations/{citationId}` | Resolve a source card to durable evidence |

Swagger UI is served at `/api/docs`; machine-readable OpenAPI is served at `/api/openapi.json`.

## Internal FastAPI resources

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/internal/v1/ingestions` | Normalize, chunk, embed, and persist one version |
| `GET` | `/internal/v1/ingestions/{jobId}` | Inspect an ingestion owned by the caller |
| `POST` | `/internal/v1/retrieval/search` | Execute bounded exact retrieval |
| `GET` | `/internal/v1/citations/{citationId}` | Resolve one citation |

## Cross-cutting rules

- `x-correlation-id` is accepted or generated and returned across boundaries;
- timestamps are UTC ISO 8601;
- `topK` is an integer from 1 through 10;
- search filters accept at most 50 document IDs and 50 document-version IDs;
- public JSON uses camelCase; internal JSON uses snake_case;
- errors use `{ code, message, details, correlationId }` and sanitized details;
- HTTP clients have explicit timeouts;
- internal ingestion and search responses expose processing time in milliseconds without logging document content;
- contract fixtures live in `packages/contracts/fixtures/`;
- the Svelte client consumes public resource types from one adapter module.
