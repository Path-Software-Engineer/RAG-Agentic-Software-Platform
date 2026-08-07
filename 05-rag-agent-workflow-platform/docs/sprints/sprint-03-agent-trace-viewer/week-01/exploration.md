# Week 1 Exploration — Workflow and Threat Boundary

Days 785–791 examined a single defensible use case: retrieve evidence from an approved corpus and return a cited or explicit non-answer outcome. The chosen graph is fixed, tools begin read-only, PostgreSQL owns durable state, Redis owns temporary delivery, and no chain-of-thought enters the trace.

Alternatives rejected: open-ended chat, arbitrary tool routing, write tools, Redis-only traces and external-provider-dependent tests.
