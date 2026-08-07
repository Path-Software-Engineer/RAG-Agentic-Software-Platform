# Week 4 Review — Sprint 1 closure

Implemented: Documents, Search, and Citation UI; public and internal integration; frontend contract tests; NestJS and Python tests; generated OpenAPI validation; empty-database migration gate; document-to-citation E2E gate; runbook; review evidence; and release draft.

Verified in the managed environment: Python lint, typecheck and six tests; NestJS typecheck, build and five tests; two frontend contract tests; Svelte diagnostics; OpenAPI exports and structural references; and Docker Compose configuration.

Pending runtime acceptance: the managed shell cannot access the Docker Desktop engine and blocks Vite's esbuild subprocess. The normal user terminal must execute `scripts/run-quality-gate.ps1` to prove the image builds, empty-database migration, pgvector query, live E2E, production Svelte bundle, and visual captures. Until that evidence passes, Sprint 1 is a release candidate rather than an official release.

Retrospective:

- **Keep:** exact-reference-first decisions, deterministic providers, explicit schema ownership, source-first UX.
- **Improve:** use a larger legal corpus before choosing ANN, caching, or a production embedding provider.
- **Stop:** treating build success as runtime acceptance or similarity as confidence.

The next planned product increment is Sprint 2, but it is not opened by this review.
