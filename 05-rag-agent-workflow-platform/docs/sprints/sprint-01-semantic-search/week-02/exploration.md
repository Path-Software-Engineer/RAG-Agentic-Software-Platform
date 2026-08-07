# Week 2 Exploration — Ingestion design

Canonical UTF-8 text is preferable to raw byte chunking because it makes offsets, hashing behavior, and tests understandable. Paragraph-aware character windows were selected over token chunking for the controlled corpus: they require no model tokenizer, preserve readable source cards, and remain deterministic.

The initial boundary accepts text only. PDF is deferred because reliable extraction and page provenance need a larger security and test surface.

Embedding providers are adapters. The deterministic hashing provider enables repeatable CI; an OpenAI-compatible implementation is environment-gated and must match the configured dimension.
