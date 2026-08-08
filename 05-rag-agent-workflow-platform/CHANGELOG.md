# Changelog

## 1.0.1 — AWS deployment fix

- replaced the unsupported CloudFormation `ssm-secure` Lambda environment reference;
- added least-privilege runtime access to the Project 05 SSM parameter;
- added validated, decrypted startup loading without logging or persisting the Neon URL;
- preserved the existing immutable ECR, CloudFront, S3 and Lambda topology.

## 1.0.0 — Unreleased

- added the bounded Agent Workflow Trace Viewer;
- added LangGraph orchestration, read-only tool registry and explicit budgets;
- added durable agent runs, steps, calls, events and checkpoints;
- added Redis Stream event delivery and reconnectable terminal SSE;
- added public/internal agent APIs and OpenAPI 1.0.0;
- added SvelteKit workflow workspace, graph and timeline;
- added controlled agent security regression evidence;
- added a cost-bounded AWS profile using CloudFront, private S3, one on-demand Lambda image and Neon PostgreSQL;
- added payload-integrity hashing for protected CloudFront POST/PATCH requests;
- completed project documentation, runbook and release draft.

## 0.2.0 — Release candidate

- added reproducible retrieval strategy comparison and audited relevance review.

## 0.1.0 — Implemented

- added controlled document ingestion, semantic search and resolvable citations.
