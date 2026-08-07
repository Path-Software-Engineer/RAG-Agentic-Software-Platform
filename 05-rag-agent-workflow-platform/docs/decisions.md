# Architecture Decision Record

## ADR-001 — One sprint branch

**Status:** Accepted.

**Decision:** Use `sprint/p5-s1-semantic-search` for the complete increment, following the repository convention most recently defined by the owner. Release, merge, tag, and push require separate authorization.

## ADR-002 — PostgreSQL schema ownership

**Status:** Accepted.

**Decision:** NestJS owns `app`; FastAPI owns `rag`. Cross-schema opportunistic queries are forbidden. The migration creates both schemas so an empty database is reproducible.

## ADR-003 — Exact vector search first

**Status:** Accepted.

**Decision:** Use exact cosine distance as Sprint 1's reference. Do not create HNSW or IVFFlat until a representative dataset demonstrates a useful latency/recall trade-off.

## ADR-004 — Deterministic embeddings by default

**Status:** Accepted with limitation.

**Decision:** A 128-dimensional deterministic hashing provider is the default for local development and CI. It is free, reproducible, and sufficient to validate contracts, provenance, persistence, and ranking. An OpenAI-compatible adapter is configuration-only and disabled without credentials. The deterministic provider is not marketed as production language understanding.

## ADR-005 — Controlled text formats

**Status:** Accepted.

**Decision:** Sprint 1 accepts UTF-8 `.txt` and `.md` files up to 1 MiB. PDF is deferred because robust parsing, page provenance, malformed-file isolation, and licensing evidence would widen this sprint.

## ADR-006 — Character-window chunking

**Status:** Accepted.

**Decision:** Canonical text is chunked at 520 characters with 80 characters of overlap, preferring paragraph or sentence boundaries. Every chunk stores stable UUIDv5 identity, ordered index, offsets, locator, and `char-window-v1`.

## ADR-007 — No cache without a benchmark

**Status:** Accepted.

**Decision:** Redis is available and health-checked but unused by product logic in Sprint 1. A query cache would otherwise add invalidation and ownership complexity without measured value.

## ADR-008 — Product visual language

**Status:** Accepted.

**Decision:** Use a dark developer-workbench aesthetic with slate surfaces, green operational status, cyan provenance accents, IBM Plex Sans-compatible body typography, and monospace evidence labels. Interaction states must remain keyboard-visible and respect reduced motion.

## ADR-009 — One branch per sprint

**Status:** Accepted.

**Decision:** Sprint 2 is isolated in `sprint/p5-s2-retrieval-evaluation`. Day-level branches are not created. Merge, release tag, and push remain separate actions requiring authorization.

## ADR-010 — Document-level ground truth first

**Status:** Accepted with limitation.

**Decision:** Retrieval test cases identify one or more relevant documents and include a human rationale. Passage-level graded judgments are deferred until a larger corpus justifies the annotation cost.

## ADR-011 — Versioned chunking comparison

**Status:** Accepted.

**Decision:** Compare three named natural-character-window strategies: compact 320/48, balanced 520/80, and broad 760/120. Every run freezes strategy IDs, test cases, document versions, cutoff, ranked evidence, and metric semantics. No observed leader is promoted as universally best.

## ADR-012 — Macro retrieval metrics with explicit semantics

**Status:** Accepted.

**Decision:** Report macro Precision@K, Recall@K, Hit Rate, MRR, and incomplete-recall count. Similarity remains a ranking score rather than probability. Metrics cannot be compared across undisclosed corpus, judgment, embedding, or cutoff changes.

## ADR-013 — Audited relevance review

**Status:** Accepted.

**Decision:** Manual result labels revise the stored run snapshot and recalculate affected metrics while preserving the original expected-document IDs. The label, notes, correlation ID, and timestamp remain in a dedicated audit table.

## ADR-014 — One bounded workflow, not autonomous chat

**Status:** Accepted.

**Decision:** Version 1.0.0 exposes only `bounded-research-v1`. Policy checking, retrieval, evidence assessment and finalization are explicit graph nodes. There is no open-ended planner loop, arbitrary tool selection or hidden background execution.

## ADR-015 — LangGraph behind an application service

**Status:** Accepted.

**Decision:** FastAPI owns a typed LangGraph `StateGraph`, while the application service owns budgets, tools, sanitization, persistence and outcomes. An equivalent deterministic fallback exists only so isolated unit tests can run when LangGraph is not installed; the locked Docker runtime installs LangGraph.

## ADR-016 — Read-only allowlisted tools

**Status:** Accepted.

**Decision:** `semantic_search`, `document_lookup`, and `evaluation_lookup` are the only registered tool contracts. The released workflow invokes semantic search only. Tools accept strict bounded arguments, return sanitized bounded resources and perform no shell, SQL, network, file-write or business action.

## ADR-017 — Durable trace, ephemeral delivery

**Status:** Accepted.

**Decision:** PostgreSQL `agent` tables own run, step, tool-call, event and checkpoint truth. Redis Streams provides namespaced, length-bounded, TTL-based delivery. A Redis failure may reduce live fan-out but cannot invalidate or erase the durable trace.

## ADR-018 — Observable execution without private reasoning

**Status:** Accepted.

**Decision:** The UI shows graph nodes, state transitions, sanitized tool inputs/results, durations, error codes, citations and terminal outcomes. It never stores or presents chain-of-thought, system prompts or private reasoning. The trace is operational evidence, not a causal explanation of a model.

## ADR-019 — One branch for Sprint 3

**Status:** Accepted.

**Decision:** The complete increment lives in `sprint/p5-s3-agent-trace-viewer`. Commit, merge, tag `v1.0.0-rag-agent-workflow-platform`, push and release publication require separate authorization.

## ADR-020 — One on-demand AWS runtime for the portfolio profile

**Status:** Accepted for the public demo.

**Decision:** Compile SvelteKit into a private S3 origin behind CloudFront and package NestJS plus the private FastAPI engine in one Lambda container. NestJS remains the only public application boundary and reaches FastAPI through localhost. Neon PostgreSQL remains durable. Do not create RDS, ElastiCache, App Runner, VPC, NAT Gateway, load balancers or provisioned concurrency. Redis remains part of the complete Docker architecture but is replaced by the explicit null publisher in this low-traffic profile because PostgreSQL owns replayable trace truth.
