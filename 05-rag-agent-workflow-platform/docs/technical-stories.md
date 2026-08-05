# Technical Stories — Sprints 1–2

## TS-501 — Reproducible document-to-vector pipeline

**Need:** The platform needs deterministic ingestion, provenance-preserving chunks, versioned embeddings, and idempotent pgvector persistence.

**Acceptance criteria:** controlled validation; canonical normalization; stable chunks; exact 128-dimensional vectors; empty-database migration; repeated ingestion does not duplicate durable artifacts.

**Status:** Implemented in Sprint 1.

**Evidence:** migration `001`, Python service and unit tests.

**Related user stories:** US-501, US-502.

## TS-502 — Versioned public and internal contracts

**Need:** Browser behavior and retrieval internals must remain independently replaceable and traceable.

**Acceptance criteria:** NestJS `/api/v1`; FastAPI `/internal/v1`; typed validation; correlation IDs; sanitized errors; generated OpenAPI; fixtures and contract checks.

**Status:** Implemented in Sprint 1 and extended in Sprint 2.

**Evidence:** `backend/nestjs-api/src`, `packages/contracts`, `tests/contracts`.

**Related user stories:** US-501, US-502, US-503, US-504, US-505.

## TS-503 — Accessible semantic-search experience

**Need:** A user must complete ingestion, search, and citation inspection without reading code.

**Acceptance criteria:** responsive routes; loading, empty, success, error, and unavailable states; visible focus; no client-side retrieval recomputation; reduced-motion support.

**Status:** Implemented in Sprint 1.

**Evidence:** SvelteKit routes and frontend contract tests.

**Related user stories:** US-501, US-502.

## TS-504 — Reproducible multi-strategy evaluation engine

**Need:** The retrieval boundary needs to rechunk the same source versions under named strategies and calculate comparable metrics without browser-side arithmetic.

**Acceptance criteria:** three bounded strategy versions; identical experiment inputs; deterministic ranking; macro Precision@K, Recall@K, Hit Rate and MRR; per-query evidence; explicit invalid-input failures.

**Status:** Implemented in Sprint 2.

**Evidence:** `ai-services/rag-agent-service/app/evaluation.py`, `ai-services/rag-agent-service/tests/test_retrieval_evaluation.py`.

**Related user stories:** US-503, US-504.

## TS-505 — Durable evaluation and relevance audit

**Need:** Evaluation evidence must survive restarts and manual review must be traceable.

**Acceptance criteria:** canonical sources; persisted test cases; complete run snapshots; selected identifiers and cutoff retained; audited relevance labels; original expected-document IDs preserved.

**Status:** Implemented in Sprint 2.

**Evidence:** migration `002`, Postgres evaluation repository.

**Related user stories:** US-504, US-505.

## TS-506 — Cross-layer retrieval-evaluation contract

**Need:** SvelteKit, NestJS, and FastAPI need typed evaluation boundaries without leaking storage or recomputing evidence.

**Acceptance criteria:** public camelCase and internal snake_case OpenAPI 0.2.0; fixtures; stable errors; metadata enrichment only in NestJS; PATCH CORS; contract and live E2E checks.

**Status:** Implemented in Sprint 2.

**Evidence:** `packages/contracts`, NestJS evaluation module, contract check, retrieval-evaluation E2E.

**Related user stories:** US-503, US-504, US-505.

## TS-507 — Accessible evaluation evidence dashboard

**Need:** A reviewer needs to configure, compare, inspect, and label retrieval evidence without reading code.

**Acceptance criteria:** real API data only; complete UI states; grouped controls; horizontal comparison and table; error details; accessible actions; responsive layout; reduced motion.

**Status:** Implemented in Sprint 2.

**Evidence:** Evaluation Lab route, shared stylesheet, frontend contract test.

**Related user stories:** US-504, US-505.

## Traceability

| Technical Story | User Stories | Primary evidence |
|---|---|---|
| TS-501 | US-501, US-502 | Python pipeline and migration `001` |
| TS-502 | US-501–US-505 | OpenAPI, fixtures, contract checks |
| TS-503 | US-501, US-502 | Semantic-search Svelte routes |
| TS-504 | US-503, US-504 | Evaluation engine and Python tests |
| TS-505 | US-504, US-505 | Migration `002` and audit repository |
| TS-506 | US-503–US-505 | NestJS/FastAPI contracts and E2E |
| TS-507 | US-504, US-505 | Evaluation Lab and frontend tests |
