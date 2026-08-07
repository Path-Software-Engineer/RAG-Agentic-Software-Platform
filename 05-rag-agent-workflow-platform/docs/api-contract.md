# HTTP Contract — Platform 1.0

Public base path: `/api/v1`

Internal base path: `/internal/v1`

Swagger UI is served at `/api/docs`; machine-readable public OpenAPI is served at `/api/openapi.json`.

## Public NestJS resources

| Method | Route | Purpose |
|---|---|---|
| `POST`, `GET` | `/documents` | Upload or list controlled documents |
| `GET` | `/documents/{documentId}` | Resolve document metadata |
| `POST` | `/documents/{documentId}/index` | Confirm idempotent index state |
| `POST` | `/search` | Execute bounded semantic search |
| `GET` | `/citations/{citationId}` | Resolve durable source evidence |
| `GET` | `/evaluations/strategies` | List versioned retrieval strategies |
| `GET`, `POST` | `/evaluations/test-cases` | List or create ground-truth cases |
| `GET`, `POST` | `/evaluations/runs` | List or execute evaluation runs |
| `GET` | `/evaluations/runs/{runId}` | Resolve one evaluation snapshot |
| `PATCH` | `/evaluations/runs/{runId}/results/{resultId}/relevance` | Audit a relevance review |
| `GET` | `/agents/tools` | List allowlisted read-only tools |
| `GET`, `POST` | `/agents/runs` | List summaries or execute a bounded run |
| `GET` | `/agents/runs/{runId}` | Resolve terminal status and answer |
| `GET` | `/agents/runs/{runId}/trace` | Resolve graph, steps, calls and events |
| `GET` | `/agents/runs/{runId}/events` | Replay sanitized events over SSE |
| `POST` | `/agents/runs/{runId}/cancel` | Cancel only a non-terminal run |
| `POST` | `/security/evaluations` | Run the controlled local policy suite |

## Agent request rules

- `workflowId` is fixed to `bounded-research-v1`;
- the goal contains 3–500 visible characters;
- `documentVersionIds` contains at most 50 UUIDs;
- tools are unique members of `semantic_search`, `document_lookup`, and `evaluation_lookup`;
- `idempotencyKey` contains 8–120 safe characters;
- budgets are bounded to 4–16 steps, 1–6 tool calls, 500–20,000 ms overall and 250–8,000 ms per tool;
- public JSON uses camelCase and internal JSON uses snake_case.

## SSE contract

`Last-Event-ID` is interpreted as the last observed positive sequence number. The server replays events strictly after that cursor, emits IDs equal to `sequenceNumber`, and closes after `run_completed`, `run_failed`, or `run_cancelled`. A heartbeat contains operational cursor data only and is not persisted as a trace event.

## Cross-cutting rules

- `x-correlation-id` is accepted or generated and propagated;
- timestamps are UTC ISO 8601 and IDs are opaque UUIDs;
- errors use `{ code, message, details, correlationId }` with sanitized details;
- OpenAPI 1.0.0 is generated from NestJS and FastAPI metadata;
- JSON Schema validates run, event, tool and security artifacts;
- the browser consumes one typed public API adapter and never calls FastAPI directly.
