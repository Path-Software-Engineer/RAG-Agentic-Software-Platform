# v0.2.0 — Sprint 2: Retrieval Evaluation

## Overview

Sprint 2 adds a reproducible Retrieval Evaluation Dashboard to the existing semantic-search platform. It compares versioned chunking strategies against explicit document-level judgments and keeps every metric linked to ranked source evidence.

## Included

- three versioned chunking strategies;
- controlled retrieval test set and rationale;
- Precision@K, Recall@K, Hit Rate, MRR, chunk count, and error analysis;
- durable evaluation snapshots and relevance-label audit;
- public NestJS and internal FastAPI OpenAPI 0.2.0 resources;
- responsive SvelteKit Evaluation Lab;
- migration, fixtures, unit/contract/frontend tests, live E2E, and demo seed script.

## Evidence boundary

The included corpus and test set are small and synthetic. Deterministic embeddings support reproducibility but are not production language embeddings. Results do not establish statistical significance, external validity, or a universally best chunking strategy. Sprint 3 agents and workflow traces are not included.

## Release workflow

Commit, Gitflow integration, tag `v0.2.0-sprint-02-retrieval-evaluation`, and push remain pending explicit authorization and a successful external Docker quality gate.
