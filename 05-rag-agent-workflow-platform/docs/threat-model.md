# Threat Model — Platform 1.0

## Assets

Document bytes, canonical sources, chunks, embeddings, citations, evaluation evidence, agent goals, run state, tool calls, trace events, checkpoints, provider/database credentials and operational identifiers.

## Trust boundaries

1. browser to public NestJS API;
2. NestJS to internal FastAPI;
3. FastAPI to PostgreSQL and Redis;
4. uploaded or retrieved text to workflow policy and tools;
5. ephemeral SSE delivery to the durable trace.

## Threats and controls

| Threat | Current control | Residual limitation |
|---|---|---|
| oversized or disguised upload | byte, extension, MIME and UTF-8 validation | no malware scanner in the local portfolio release |
| prompt injection in the request | bounded input and explicit policy patterns before tools | pattern policy is not a complete semantic defense |
| indirect injection in retrieved text | retrieved content is typed as untrusted evidence and never executed | human reviewers must still inspect cited text |
| arbitrary tool use | registry allowlist, strict names, read-only definitions and workflow scope | no write-action approval implementation exists |
| SQL, shell or network abuse | no such tool contracts; bounded semantic-search arguments | host operators still control the local runtime |
| data exfiltration | credential-key, token, canary and email redaction before persistence/streaming | redaction is defense in depth, not a DLP product |
| denial of wallet or unbounded loops | fixed graph, step/tool limits and overall/per-tool timeouts | no tenant quota or rate limiter yet |
| duplicate side effects | idempotency key and durable checkpoint after each event | the released tools are read-only by design |
| trace manipulation or loss | PostgreSQL ordering constraint and durable events; Redis is non-authoritative | no signed external audit ledger |
| private reasoning exposure | structured observable fields only and explicit `privateReasoningExposed: false` | operator diagnostics must keep the same policy |
| misleading evidence | citations are resolvable; similarity and security metrics state their scope | synthetic fixtures do not establish production safety |
| credential leakage in logs | sanitized errors and no full query/document payload logging | deployment secret-manager integration is environment-specific |

## Controlled security suite

The deterministic suite contains one benign case plus prompt-injection, tool-abuse, data-exfiltration and denial-of-wallet cases. It runs locally, calls no external target and stores only scenario IDs, categories, expected/observed dispositions and policy codes. Five passing fixtures demonstrate regression behavior of this policy version; they do not prove general agent security.

## Human approval boundary

Version 1.0.0 has no mutating tool. Any future file, database, messaging, purchasing or deployment action must introduce an explicit approval contract, authorization, audit identity, idempotent execution and compensation behavior before the tool can enter the registry.

## Explicit non-claims

The release is not multi-tenant, not approved for sensitive documents, has no authentication, does not execute arbitrary code, does not rely on an external LLM, and is not a production security certification. No chain-of-thought is collected or displayed.
