# Tool Policy Lab

Purpose: verify that the runtime exposes only named read-only tools and rejects unknown capabilities before implementation lookup.

The registry contains `semantic_search`, `document_lookup`, and `evaluation_lookup`. The released workflow permits and invokes semantic search only. No tool accepts shell commands, SQL, arbitrary URLs or write actions. Every result is size-bounded and sanitized before trace persistence.

Evidence lives in `app/agents.py`, its unit tests, the tool-definition JSON Schema, the public `/api/v1/agents/tools` resource and the Sprint 3 E2E.
