# Week 1 Exploration — Scope and boundaries

**Problem:** Small knowledge corpora need searchable evidence without hiding provenance behind generated prose.

**User:** A technical knowledge user evaluating a RAG foundation.

**Corpus:** Four original, non-sensitive UTF-8 fixtures about retrieval engineering.

**Initial formats:** `.txt` and `.md`, maximum 1 MiB.

**Success:** An accepted document receives durable IDs and status through the complete SvelteKit -> NestJS -> FastAPI -> PostgreSQL path.

Primary architecture: one public NestJS boundary and one internal Python RAG boundary. Alternative rejected: browser-to-FastAPI access, because it duplicates public policy and couples the UI to retrieval internals.

Risks: premature module scaffolding, inconsistent resource types, leaked content, and false production claims. Controls are explicit ownership, generated/central public types, content-free logs, and an evidence boundary.
