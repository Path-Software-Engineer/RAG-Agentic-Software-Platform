# Threat Model — Sprint 1

## Assets

Document bytes, normalized chunks, source metadata, embeddings, citation provenance, database credentials, provider credentials, and operational identifiers.

## Trust boundaries

1. browser to public NestJS API;
2. NestJS to internal FastAPI;
3. services to PostgreSQL;
4. uploaded bytes to extraction and retrieval logic.

## Primary threats and controls

| Threat | Sprint 1 control | Residual limitation |
|---|---|---|
| oversized or disguised upload | byte limit, extension/MIME allowlist, UTF-8 decode, sanitized name | no malware scanner in local portfolio release |
| duplicate ingestion | SHA-256 unique constraint and idempotency key | identical bytes intentionally resolve to the first resource |
| prompt injection in document text | retrieved content is displayed as untrusted evidence only | agents do not exist in Sprint 1 |
| provenance forgery | server-generated IDs and resolvable citation endpoint | external source authenticity is not verified |
| SQL injection | parameterized queries | application auth is deferred |
| data leakage in logs | content-free structured logs and sanitized error envelope | local Docker operators can access volumes |
| provider key exposure | environment-only configuration, no key logging | secret manager belongs to deployment work |
| denial through broad retrieval | query length and top-k bounds, HTTP timeout | no tenant quota or rate limiter yet |

## Explicit non-claims

This release is not multi-tenant, is not approved for private documents, has no authentication, does not perform malware scanning, and does not execute retrieved instructions.
