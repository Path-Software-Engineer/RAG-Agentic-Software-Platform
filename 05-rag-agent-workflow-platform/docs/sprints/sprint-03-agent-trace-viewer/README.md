# Sprint 3 — Agent Workflow Trace Viewer

Global days 785–812 close Project 05 with one bounded, observable and secure evidence workflow.

## Delivered scope

- typed AgentRun, graph, tool, event, trace and security contracts;
- four-node LangGraph workflow with deterministic local execution;
- allowlisted read-only retrieval tools;
- explicit step, tool, time and result-size budgets;
- idempotency, cancellation boundary and durable checkpoints;
- PostgreSQL `agent` schema plus ephemeral Redis Streams;
- internal FastAPI and public NestJS agent APIs;
- terminal SSE replay using `Last-Event-ID`;
- SvelteKit run workspace and trace viewer;
- five-scenario local security regression suite;
- OpenAPI 1.0.0, JSON Schemas, E2E and complete documentation.

## Official flow

```text
goal -> validate -> policy check -> semantic_search -> assess evidence
     -> terminal outcome -> durable trace -> SSE replay -> trace viewer
```

## Closure evidence

The release gate covers Python typing/lint/tests, NestJS and Svelte tests, contract validation, empty-database migrations, PostgreSQL/pgvector/Redis health, service images, three cross-layer E2Es, OpenAPI export and Git whitespace. Final counts belong to the executed gate output and must not be invented in this document.

The repository-level static verification passed with 21 Python tests at 80.29% coverage, 9 NestJS tests, 5 frontend contract tests, Python and TypeScript type checks, contract validation, Docker Compose configuration validation and production builds for NestJS and SvelteKit. The containerized migration and cross-layer E2E stages still require execution from a host session with access to the Docker engine; the managed implementation session was denied access to the Docker named pipe.

## Limitations

The workflow is synchronous, deterministic and restricted to a controlled corpus. Security cases are fixtures. Authentication, tenancy, arbitrary tools, write actions, human approval execution, external LLM quality and cloud deployment are outside this release.

## Release boundary

The implementation branch is `sprint/p5-s3-agent-trace-viewer`. Commit, merge, tag, push and release publication remain separate authorized operations. The planned final tag is `v1.0.0-rag-agent-workflow-platform`.
