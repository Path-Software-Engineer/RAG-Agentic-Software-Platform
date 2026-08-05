# Sprint 2 — Retrieval Evaluation Dashboard

## Objective

Turn retrieval quality into inspectable software evidence. The increment adds ground-truth test cases, three versioned chunking strategies, reproducible comparisons, metric/error analysis, manual relevance review, and a real SvelteKit dashboard over public NestJS and internal FastAPI contracts.

## Completed scope

- canonical source persistence for controlled rechunking;
- compact 320/48, balanced 520/80, and broad 760/120 strategies;
- document-level retrieval test cases with rationale;
- versioned run snapshots with Precision@K, Recall@K, Hit Rate, MRR, chunk count, and errors;
- ranked per-query evidence and manual relevance audit;
- OpenAPI 0.2.0 public/internal routes;
- responsive Evaluation Lab with visual and tabular comparisons;
- migration `002`, fixtures, unit/contract/frontend/E2E checks, and demo seeding.

## Product boundary

Sprint 2 evaluates retrieval only. It does not generate answers, orchestrate agents, execute tools, stream traces, or claim production semantic quality. Sprint 3 remains unstarted.

## Validation status

Python lint, formatting, strict typing, unit tests, NestJS typecheck/tests/build, Svelte check/tests, generated OpenAPI, contract checks, Compose configuration, and Git whitespace are part of the gate. The managed sandbox cannot access Docker Desktop, so empty-database migration, container builds, live E2E, and browser capture must be executed from the normal terminal before an official release.

## Closure criteria

- all three strategies use identical selected experiment inputs;
- metrics and score semantics are visible;
- stored runs reopen without recomputation in the browser;
- manual labels are audited and preserve original expected-document IDs;
- incomplete recall remains inspectable;
- the full external Docker quality gate passes;
- no Sprint 3 runtime module exists.
