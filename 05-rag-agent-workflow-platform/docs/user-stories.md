# User Stories — Sprints 1–2

## US-501 — Register and index controlled documents

**Story:** As a knowledge user, I want to upload an allowed document so that its content becomes searchable without exposing infrastructure details.

**Acceptance criteria:**

- a valid UTF-8 `.txt` or `.md` upload returns stable document, version, job, status, and correlation identifiers;
- identical bytes resolve to the existing resource without duplicating durable artifacts;
- unsupported, empty, oversized, or non-UTF-8 files are rejected before persistence;
- completed chunks retain version, order, offsets, locator, and chunking version.

**Status:** Implemented in Sprint 1.

**Evidence:** `backend/nestjs-api/src/documents`, `ai-services/rag-agent-service/app/services.py`, `database/migrations/001_sprint_01_initial.sql`, `/documents`.

## US-502 — Search with resolvable sources

**Story:** As a knowledge user, I want ranked fragments with visible sources so that I can inspect where every result came from.

**Acceptance criteria:**

- valid search returns ordered results with score, document, version, chunk, citation, snippet, and locator;
- optional document/version filters are enforced;
- a citation resolves to durable source evidence;
- empty results are explicit and never generate an answer;
- similarity is described as a ranking signal rather than confidence or truth.

**Status:** Implemented in Sprint 1.

**Evidence:** `ai-services/rag-agent-service/app/services.py`, `backend/nestjs-api/src/search`, `frontend/sveltekit-app/src/routes/search`, `frontend/sveltekit-app/src/routes/citations`.

## US-503 — Define a retrieval test set

**Story:** As an ML engineer, I want queries linked to explicitly relevant documents so that retrieval quality is evaluated against reviewable ground truth.

**Acceptance criteria:**

- a test case stores a bounded query, one or more relevant document IDs, a rationale, and a stable ID;
- invalid or incomplete cases are rejected without persistence;
- stored cases and expected-document counts are visible and selectable in the Evaluation Lab.

**Status:** Implemented in Sprint 2.

**Evidence:** `ai-services/rag-agent-service/app/evaluation.py`, migration `002`, `backend/nestjs-api/src/evaluations`, `frontend/sveltekit-app/src/routes/evaluation`.

## US-504 — Compare retrieval strategies under one experiment

**Story:** As an ML engineer, I want to run the same corpus and test set through multiple chunking strategies so that I can compare their observed retrieval behavior fairly.

**Acceptance criteria:**

- every selected strategy receives the same corpus versions, test cases, embedding adapter, and K;
- each strategy returns chunk count, Precision@K, Recall@K, Hit Rate, MRR, error count, and ranked query evidence;
- a completed run persists a versioned snapshot and can be reopened;
- the dashboard provides both a visual comparison and an exact accessible table;
- the browser does not recalculate retrieval scores or metrics.

**Status:** Implemented in Sprint 2.

**Evidence:** evaluation engine, OpenAPI 0.2.0, NestJS evaluation service, and Svelte Evaluation Lab.

## US-505 — Inspect misses and review relevance

**Story:** As a retrieval reviewer, I want to inspect incomplete-recall queries and label individual results so that evaluation errors remain explainable and auditable.

**Acceptance criteria:**

- incomplete-recall queries expose strategy, rank, score, source, and snippet;
- a reviewer can mark a result relevant or not relevant;
- label, notes, correlation ID, and review time are stored without changing original expected-document IDs;
- affected metrics are recalculated in the revised snapshot;
- the interface states that reviewer labels are judgments rather than universal truth.

**Status:** Implemented in Sprint 2.

**Evidence:** `rag.relevance_labels`, evaluation label endpoint/service, Evaluation Lab error analysis, and Sprint 2 E2E test.
