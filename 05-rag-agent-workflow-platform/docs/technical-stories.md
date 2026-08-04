# Technical Stories — Sprint 1

## TS-501 — Reproducible document-to-vector pipeline

**Need:** The platform needs deterministic ingestion, provenance-preserving chunks, versioned embeddings, and idempotent pgvector persistence.

**Acceptance criteria:** controlled validation; canonical UTF-8 normalization; stable chunks; exact 128-dimensional vectors; empty-database migration; repeated ingestion does not duplicate durable artifacts.

**Status:** Implemented in the Sprint 1 working tree.

**Evidence:** `database/migrations/001_sprint_01_initial.sql`, `ai-services/rag-agent-service/app`, `ai-services/rag-agent-service/tests`.

**Related user stories:** US-501, US-502.

## TS-502 — Versioned public and internal contracts

**Need:** Browser-facing behavior and RAG internals must remain independently replaceable and traceable.

**Acceptance criteria:** NestJS `/api/v1`; FastAPI `/internal/v1`; typed validation; correlation IDs; sanitized error mapping; OpenAPI documents; contract fixtures and tests.

**Status:** Implemented in the Sprint 1 working tree.

**Evidence:** `backend/nestjs-api/src`, `packages/contracts`, `tests/contracts`.

**Related user stories:** US-501, US-502.

## TS-503 — Accessible semantic-search experience

**Need:** A user must complete ingestion, search, and citation inspection without reading code.

**Acceptance criteria:** responsive Documents, Search, and Citation routes; loading, empty, success, error and unavailable states; keyboard-visible focus; no client-side retrieval recomputation; reduced-motion support.

**Status:** Implemented in the Sprint 1 working tree.

**Evidence:** `frontend/sveltekit-app/src`, `frontend/sveltekit-app/tests`.

**Related user stories:** US-501, US-502.

## Traceability

| Technical Story | User Stories | Primary evidence |
|---|---|---|
| TS-501 | US-501, US-502 | Python service, pgvector migration |
| TS-502 | US-501, US-502 | NestJS/FastAPI OpenAPI and contract tests |
| TS-503 | US-501, US-502 | SvelteKit routes and component tests |
