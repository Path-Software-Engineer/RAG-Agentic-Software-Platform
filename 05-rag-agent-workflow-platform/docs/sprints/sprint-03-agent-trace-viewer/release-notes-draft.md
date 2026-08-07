# v1.0.0 — RAG Agent Workflow Platform

## Overview

This final release integrates semantic search, retrieval evaluation and a governed agent workflow into one traceable applied-AI software platform.

## Sprint 3 highlights

- bounded LangGraph research workflow;
- explicit terminal outcomes and operational budgets;
- read-only allowlisted tools;
- durable PostgreSQL runs, steps, calls, events and checkpoints;
- ephemeral Redis Stream delivery;
- NestJS public API and reconnectable SSE;
- SvelteKit run workspace, graph and trace timeline;
- sanitized payloads with no private reasoning;
- controlled five-scenario security regression suite;
- OpenAPI 1.0.0, JSON Schemas and full cross-layer E2E.
- cost-bounded AWS delivery through CloudFront, private S3, one on-demand Lambda image and Neon PostgreSQL.

## Existing platform capabilities

Sprint 1 provides idempotent document ingestion, pgvector search and resolvable citations. Sprint 2 provides reproducible strategy comparison, Precision@K, Recall@K, Hit Rate, MRR and audited relevance review.

## Known limitations

The corpus and evaluation set are small and synthetic. The default embedding provider is deterministic. The agent uses one fixed workflow and read-only tools. Authentication, multi-tenancy, arbitrary actions and external LLM evaluation are not included. The AWS profile is a portfolio demo and does not claim production readiness or guaranteed zero cost.
