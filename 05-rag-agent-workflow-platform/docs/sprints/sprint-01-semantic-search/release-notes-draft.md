# v0.1.0 — Sprint 1: Semantic Search

## Overview

Sprint 1 introduces the first complete vertical of the RAG & Agent Workflow Platform: controlled text documents become normalized, provenance-preserving chunks, versioned vectors, ranked search evidence, and resolvable citations.

## Included

- UTF-8 `.txt` and `.md` ingestion with size, MIME, filename, encoding, and SHA-256 validation;
- replaceable storage, extraction, chunking, and embedding adapters;
- PostgreSQL schemas owned independently by NestJS and FastAPI;
- versioned 128-dimensional deterministic embeddings for local reproducibility;
- exact pgvector cosine retrieval with document and document-version filters;
- public Documents, Search, and Citation resources with Swagger/OpenAPI;
- responsive SvelteKit Documents, Search, and Citation flows;
- unit, contract, migration, integration, E2E, and quality gates.

## Evidence boundary

- The four-document corpus is synthetic, legal, and intentionally small.
- Similarity is a relative ranking signal, not probability, truth, or confidence.
- No approximate index is enabled because the corpus cannot support an honest ANN benchmark.
- The deterministic provider validates software behavior; it is not production semantic quality.
- Sprint 1 retrieves evidence and does not generate answers.
- Authentication, tenant isolation, retrieval evaluation, agents, tools, traces, and deployment are outside this release.

## Release state

Draft only. Create the release, merge, tag, and push only after the Docker-backed quality gate and visual review pass in the normal user environment and the repository owner explicitly authorizes Git publication.
