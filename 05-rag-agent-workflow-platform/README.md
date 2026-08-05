# RAG & Agent Workflow Platform

Project 05 of the Software Engineer path is a modular platform for trustworthy retrieval-augmented software. Sprint 1 turns controlled text documents into traceable semantic-search evidence. Sprint 2 adds a reproducible Retrieval Evaluation Dashboard that compares versioned chunking strategies against explicit document-level relevance judgments.

The original three-sprint roadmap remains preserved in [the project master plan](docs/project-master-plan.md). This working tree implements Sprints 1 and 2 only.

## Current release boundary

| Module | Status | Release |
|---|---|---|
| Semantic Search | Implemented in Sprint 1 | `v0.1.0-sprint-01-semantic-search` pending release workflow |
| Retrieval Evaluation | Implemented; Docker-backed runtime acceptance remains pending outside the managed sandbox | `v0.2.0-sprint-02-retrieval-evaluation` pending authorization |
| Agent Workflow Trace Viewer | Planned; not started | Sprint 3 |

No agent, tool-call, streaming trace, or workflow-execution functionality is claimed by this release.

## Architecture

```text
Browser
  -> SvelteKit web application
  -> NestJS public API (/api/v1)
       -> app schema in PostgreSQL
       -> internal FastAPI RAG service (/internal/v1)
            -> rag schema + pgvector
            -> versioned retrieval evaluation engine
```

Ownership remains explicit:

- SvelteKit presents typed API resources and never calculates retrieval metrics.
- NestJS owns the public contract, application metadata, orchestration, and error mapping.
- FastAPI owns normalization, chunking, embeddings, retrieval, citations, evaluation runs, and relevance-label recalculation.
- PostgreSQL is the durable source of truth; `app` and `rag` remain separately owned schemas.
- the deterministic embedding provider keeps local development and CI free from external model costs.

See [architecture](docs/architecture.md), [API contract](docs/api-contract.md), and [data contract](docs/data-contract.md).

## Product flows

```text
Semantic Search
.txt or .md -> validate -> normalize -> chunk -> embed -> rank -> resolve citation

Retrieval Evaluation
indexed sources + ground-truth queries
  -> choose versioned chunking strategies
  -> rebuild comparable evaluation chunks
  -> rank every query at the same K
  -> calculate macro Precision@K, Recall@K, Hit Rate and MRR
  -> inspect errors and record manual relevance labels
```

Evaluation runs are immutable evidence snapshots apart from explicitly audited relevance reviews. Similarity is a ranking signal, not confidence or correctness.

## Run locally

Prerequisite: Docker Desktop with Linux containers.

```powershell
Set-Location "C:\JeanLoa\Path-Software-Engineer\RAG-Agentic-Software-Platform\05-rag-agent-workflow-platform"
Copy-Item .env.example .env
.\scripts\setup.ps1
.\scripts\run-platform.ps1 -Build
```

Open:

- Web: <http://localhost:5173>
- Retrieval Evaluation: <http://localhost:5173/evaluation>
- NestJS Swagger: <http://localhost:5300/api/docs>
- NestJS OpenAPI JSON: <http://localhost:5300/api/openapi.json>
- API health: <http://localhost:5300/healthz>

Load the controlled corpus and evaluation evidence:

```powershell
.\scripts\seed-demo.ps1
.\scripts\seed-evaluation-demo.ps1
```

Stop the platform:

```powershell
.\scripts\stop-platform.ps1
```

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate validates contract fixtures and OpenAPI, Python typing/lint/tests, Compose configuration, an empty PostgreSQL migration through `002`, service builds, NestJS/Svelte tests, the semantic-search E2E, and the retrieval-evaluation E2E including a relevance-label audit.

## Sprint 2 demonstration

1. Load the controlled corpus and open **Retrieval Evaluation**.
2. Review or create test cases with explicit relevant documents and rationale.
3. Select the compact, balanced, and broad chunking strategies under one shared cutoff.
4. Run the controlled evaluation and compare Precision@K, Recall@K, Hit Rate, MRR, chunk counts, and errors.
5. Expand an incomplete-recall query and inspect every retrieved fragment.
6. Apply a manual relevance label and confirm that the run snapshot and metrics are recalculated while the original expected-document set remains visible.
7. Read the evidence boundary before interpreting any observed leader.

## Sprint evidence

- [Sprint 1 overview](docs/sprints/sprint-01-semantic-search/README.md)
- [Sprint 2 overview](docs/sprints/sprint-02-retrieval-evaluation/README.md)
- [User stories](docs/user-stories.md)
- [Technical stories](docs/technical-stories.md)
- [Decisions](docs/decisions.md)
- [Threat model](docs/threat-model.md)

## Evidence boundary

- The included corpus and test set are small, synthetic, and non-sensitive.
- The reference implementation uses exact comparison and deterministic local embeddings.
- Precision@K, Recall@K, Hit Rate, and MRR apply only to the selected test cases, corpus versions, strategy versions, and cutoff.
- Manual labels are reviewer judgments, not universal relevance truth.
- No statistical significance, external benchmark, production semantic quality, or model-generalization claim is made.
- Authentication, tenant isolation, agents, tool execution, streaming traces, and deployment are outside this release.

## Author

Jean Franck Loa Rojas

Software Engineer Path — Applied AI Software Systems
