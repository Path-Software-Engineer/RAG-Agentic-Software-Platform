# Week 3 Exploration — Retrieval and citations

Cosine similarity was selected because normalized deterministic vectors make the score interpretable as a relative ranking signal. Exact scan is the reference. An approximate index is rejected for Sprint 1 because the four-document corpus cannot demonstrate an honest latency/recall benefit.

Allowed filters are limited to document IDs and document-version IDs. Top-k is limited to 1–10. Every result creates or reuses a durable citation containing document/version/chunk identifiers, snippet, locator, and score.

Risk: users may read similarity as confidence. Both API descriptions and UI copy explicitly reject that interpretation.
