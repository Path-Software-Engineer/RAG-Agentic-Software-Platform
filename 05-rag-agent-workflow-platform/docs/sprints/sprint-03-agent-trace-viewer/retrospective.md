# Sprint 3 Retrospective

## What worked

- freezing the trace/event contracts before UI work prevented browser-side invention;
- keeping PostgreSQL authoritative made Redis failure semantics clear;
- one deterministic workflow allowed policy, budgets, citations and failure paths to be tested without paid services;
- the three-layer boundary remained intact through generated OpenAPI and E2E checks.

## What required care

- a visible trace can be mistaken for private reasoning, so the product now states the boundary explicitly;
- SSE needed terminal completion as well as cursor replay;
- timeout outcomes needed their own terminal semantics instead of becoming generic failures;
- generated frontend tooling can hit managed-Windows `spawn EPERM`, so Docker remains the release build boundary.

## Next boundary

Project 05 ends here. Multi-agent work belongs to the separate AI Project 30 and must not be backfilled as a hidden Sprint 4.
