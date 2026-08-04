# Sprint 1 — Semantic Search Module

## Goal

Allow a knowledge user to upload controlled text documents and retrieve traceable fragments with resolvable citations.

## Implementation delivered

- reproducible SvelteKit, NestJS, FastAPI, PostgreSQL/pgvector, and Redis workspace;
- controlled `.txt` and `.md` upload, SHA-256 deduplication, and durable status;
- normalized text, stable chunks, versioned deterministic embeddings;
- exact cosine reference search with bounded filters and top-k;
- public Documents, Search, and Citation APIs plus internal RAG APIs;
- responsive Documents, Search, and Citation screens;
- layer, contract, unit, migration, integration, E2E, and visual-validation gates ready in the root quality script.

## Out of scope

PDF, authentication, multi-tenancy, approximate vector indexes, retrieval evaluation, LLM answers, agents, tools, traces, SSE, and production deployment.

## Week evidence

- [Week 1 exploration](week-01/exploration.md) and [review](week-01/review.md)
- [Week 2 exploration](week-02/exploration.md) and [review](week-02/review.md)
- [Week 3 exploration](week-03/exploration.md) and [review](week-03/review.md)
- [Week 4 exploration](week-04/exploration.md) and [review](week-04/review.md)

## Closure state

The implementation is complete on the sprint branch. Static checks, unit tests, generated OpenAPI validation, and Compose configuration pass in the managed environment. Docker-backed migration/E2E execution, the Svelte production bundle, and browser captures still require the normal user terminal because this sandbox cannot access the Docker engine or spawn the esbuild binary. The release branch, merge, tag `v0.1.0-sprint-01-semantic-search`, and push remain pending explicit authorization.
