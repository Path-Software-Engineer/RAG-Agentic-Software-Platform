# RAG & Agent Workflow Platform

Project 05 of the Software Engineer path is a modular platform for trustworthy retrieval-augmented software. The first release delivers a complete Semantic Search vertical: controlled document ingestion, reproducible chunking, versioned embeddings, PostgreSQL/pgvector retrieval, resolvable citations, a NestJS public API, and an accessible SvelteKit interface.

The original three-sprint roadmap remains preserved in [the project master plan](docs/project-master-plan.md). This working tree implements only Sprint 1.

## Current release boundary

| Module | Status | Release |
|---|---|---|
| Semantic Search | Implemented; Docker-backed runtime acceptance remains pending outside the managed sandbox | `v0.1.0-sprint-01-semantic-search` pending authorization |
| Retrieval Evaluation | Planned; not started | Sprint 2 |
| Agent Workflow Trace Viewer | Planned; not started | Sprint 3 |

No evaluation-run, agent, tool-call, or trace functionality is claimed by this release.

## Architecture

```text
Browser
  -> SvelteKit web application
  -> NestJS public API (/api/v1)
       -> app schema in PostgreSQL
       -> internal FastAPI RAG service (/internal/v1)
            -> rag schema + pgvector

Redis is available for future bounded temporary work, but Sprint 1 does not make
it a source of truth or introduce a cache without benchmark evidence.
```

Ownership remains explicit:

- SvelteKit presents typed API resources and never accesses infrastructure directly.
- NestJS owns the public contract and the `app` database schema.
- FastAPI owns ingestion, chunking, embeddings, retrieval, citations, and the `rag` schema.
- PostgreSQL is the durable source of truth; pgvector performs exact reference search.
- the deterministic embedding provider keeps local development and CI free from external model costs.

See [architecture](docs/architecture.md), [API contract](docs/api-contract.md), and [data contract](docs/data-contract.md).

## Product flow

```text
.txt or .md document
  -> filename, MIME, size and hash validation
  -> normalized canonical text
  -> provenance-preserving chunks
  -> versioned deterministic embeddings
  -> exact cosine search in pgvector
  -> ranked source cards
  -> resolvable citation detail
```

The deterministic provider is evidence infrastructure, not a claim of production semantic quality. An OpenAI-compatible adapter can be configured later without changing public contracts.

## Run locally

Prerequisites: Docker Desktop with Linux containers.

```powershell
Set-Location "C:\JeanLoa\Path-Software-Engineer\RAG-Agentic-Software-Platform\05-rag-agent-workflow-platform"
Copy-Item .env.example .env
.\scripts\setup.ps1
.\scripts\run-platform.ps1 -Build
```

Open:

- Web: <http://localhost:5173>
- NestJS Swagger: <http://localhost:5300/api/docs>
- NestJS OpenAPI JSON: <http://localhost:5300/api/openapi.json>
- API health: <http://localhost:5300/healthz>

Load the controlled demo corpus:

```powershell
.\scripts\seed-demo.ps1
```

Stop the platform:

```powershell
.\scripts\stop-platform.ps1
```

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate validates Compose configuration, builds all services, recreates PostgreSQL from an empty volume, checks pgvector and Redis health, runs Python/NestJS/Svelte tests, verifies public and internal OpenAPI contracts, and exercises the document-to-citation flow.

## Demonstration

1. Open **Documents** and add one of the legal fixtures in `data/samples/`.
2. Confirm the document reaches `completed` and exposes its chunk count.
3. Open **Search**, enter a meaning-based query, and choose `top_k`.
4. Inspect score semantics and provenance on each source card.
5. Open a citation to resolve the document, version, chunk, and locator.
6. Review the explicit evidence boundary in the interface.

## Sprint evidence

- [Sprint 1 overview](docs/sprints/sprint-01-semantic-search/README.md)
- [User stories](docs/user-stories.md)
- [Technical stories](docs/technical-stories.md)
- [Decisions](docs/decisions.md)
- [Threat model](docs/threat-model.md)

## Evidence boundary

- The included corpus is small, synthetic, and non-sensitive.
- Exact pgvector search is the reference implementation; no ANN index is claimed useful without a larger benchmark.
- Deterministic embeddings make behavior reproducible but do not match a production-grade language embedding model.
- Search scores express configured vector similarity, not truth, confidence, or answer correctness.
- Sprint 1 returns evidence fragments and citations; it does not generate answers.
- Authentication, tenant isolation, evaluation dashboards, agents, and deployment are outside this release.

## Author

Jean Franck Loa Rojas

Software Engineer Path — Applied AI Software Systems
