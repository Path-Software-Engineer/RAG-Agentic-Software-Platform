# Threat Model — Sprints 1–2

## Assets

Document bytes, canonical sources, chunks, metadata, embeddings, citation provenance, test cases, run snapshots, relevance labels, database/provider credentials, and operational identifiers.

## Trust boundaries

1. browser to public NestJS API;
2. NestJS to internal FastAPI;
3. services to PostgreSQL;
4. uploaded bytes and reviewer judgments to retrieval logic.

## Primary threats and controls

| Threat | Current control | Residual limitation |
|---|---|---|
| oversized or disguised upload | byte limit, extension/MIME allowlist, UTF-8 decode, sanitized name | no malware scanner in local portfolio release |
| duplicate ingestion | SHA-256 unique constraint and idempotency key | identical bytes intentionally resolve to the first resource |
| prompt injection in document text | content is displayed as untrusted evidence only | agents do not exist in Sprint 2 |
| provenance forgery | server-generated IDs and resolvable citation endpoint | external source authenticity is not verified |
| SQL injection | parameterized queries | application authentication is deferred |
| data leakage in logs | content-free structured logs and sanitized errors | local Docker operators can access volumes |
| provider key exposure | environment-only configuration and no key logging | secret-manager integration belongs to deployment work |
| denial through broad retrieval | query, filter, strategy, test-case, version and top-K bounds; HTTP timeout | no tenant quota or rate limiter yet |
| relevance-label tampering | server-owned result IDs, run-membership validation, correlation ID and audit row | authentication and reviewer identity are deferred |
| misleading metric comparison | visible corpus/test-set/cutoff semantics and persisted snapshots | the small synthetic test set has limited external validity |

## Explicit non-claims

This release is not multi-tenant, is not approved for private documents, has no authentication, does not perform malware scanning, and does not execute retrieved instructions. Relevance labels are local reviewer judgments, not authoritative universal ground truth.
