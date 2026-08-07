# RAG & Agent Workflow Platform

Project 05 of the Software Engineer path is a modular platform for trustworthy retrieval and observable agent workflows. It turns controlled documents into resolvable search evidence, measures retrieval behavior under comparable experiments, and executes one bounded read-only workflow whose complete sanitized trace can be inspected without exposing private reasoning.

The original 84-day roadmap is preserved in [the project master plan](docs/project-master-plan.md). All three planned sprints and the cost-bounded AWS delivery profile are implemented in the current working tree; final Git release operations remain separately authorized.

## Product modules

| Module | Capability | Release boundary |
|---|---|---|
| Semantic Search | idempotent text ingestion, versioned chunks/embeddings, exact pgvector ranking and resolvable citations | Sprint 1 |
| Retrieval Evaluation | three versioned chunking strategies, test cases, Precision@K, Recall@K, Hit Rate, MRR and audited labels | Sprint 2 |
| Agent Trace Viewer | bounded LangGraph workflow, read-only tools, budgets, durable traces, SSE and controlled security evidence | Sprint 3 / 1.0.0 |

## Architecture

```text
Browser
  -> SvelteKit
  -> NestJS public API (/api/v1) and SSE
       -> PostgreSQL app schema
       -> FastAPI private API (/internal/v1)
            -> PostgreSQL rag schema + pgvector
            -> PostgreSQL agent schema
            -> LangGraph + allowlisted tools
            -> Redis Streams for ephemeral events
```

- SvelteKit presents typed server resources and never calculates retrieval metrics or traces.
- NestJS owns the public contract, validation, correlation, error mapping and SSE replay.
- FastAPI owns ingestion, embeddings, retrieval, evaluation, policy, graph execution, tools and sanitization.
- PostgreSQL is durable truth; Redis is temporary delivery only.
- the deterministic embedding provider and fixed workflow keep local development and CI independent of paid model APIs.

The AWS portfolio profile compiles SvelteKit into a private S3 origin behind CloudFront and runs NestJS plus the private FastAPI engine inside one on-demand Lambda container. Neon PostgreSQL remains the durable store. This profile preserves the public/private API boundary without App Runner, RDS, ElastiCache, NAT Gateway or provisioned concurrency. See [AWS deployment](infra/aws/README.md).

See [architecture](docs/architecture.md), [HTTP contract](docs/api-contract.md), [event contract](docs/event-contract.md), [trace contract](docs/trace-contract.md), and [threat model](docs/threat-model.md).

## Agent workflow

```text
goal
  -> policy_check
      -> blocked -> finalize
      -> allowed -> semantic_search -> assess_evidence -> finalize
  -> explicit terminal outcome
  -> durable ordered trace
  -> reconnectable SSE
  -> graph and timeline viewer
```

The released tools are `semantic_search`, `document_lookup`, and `evaluation_lookup`; only semantic search is invoked by `bounded-research-v1`. All are read-only. Step, tool, overall-time and per-tool-time budgets are explicit. Trace data is sanitized and contains no system prompt or chain-of-thought.

## Run locally

Prerequisite: Docker Desktop using Linux containers.

```powershell
Set-Location "C:\JeanLoa\Path-Software-Engineer\RAG-Agentic-Software-Platform\05-rag-agent-workflow-platform"
Copy-Item .env.example .env -ErrorAction SilentlyContinue
.\scripts\setup.ps1
.\scripts\run-platform.ps1 -Build
```

Open:

- Web: <http://localhost:5173>
- Agent workspace: <http://localhost:5173/agents>
- NestJS Swagger: <http://localhost:5300/api/docs>
- Public OpenAPI JSON: <http://localhost:5300/api/openapi.json>
- API health: <http://localhost:5300/healthz>

Load the complete controlled demonstration:

```powershell
.\scripts\seed-demo.ps1
.\scripts\seed-evaluation-demo.ps1
.\scripts\seed-agent-demo.ps1
```

Stop with `./scripts/stop-platform.ps1`. Operational details live in [the runbook](docs/runbook.md).

## Deploy to AWS

The public demo uses one CloudFront URL and scales API compute to zero between requests:

```powershell
.\infra\aws\configure-secrets.ps1 -Profile "paths" -Region "us-east-1"
.\infra\aws\deploy.ps1 -Profile "paths" -Region "us-east-1" -PreflightOnly
.\infra\aws\deploy.ps1 -Profile "paths" -Region "us-east-1"
```

The secret helper accepts a Neon pooled TLS URL. AWS Budgets are alerts rather than a hard cap; Lambda, S3, CloudFront, ECR, logs and transfer must still be monitored.

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate validates JSON Schemas and generated OpenAPI 1.0.0, Python lint/type/tests, Compose configuration, an empty PostgreSQL migration through `003`, pgvector and Redis health, container builds, NestJS/Svelte tests, three live cross-layer E2Es, SSE replay, security policy behavior and Git whitespace.

## Demonstration path

1. Use **Documents** and **Semantic Search** to inspect ranked, resolvable evidence.
2. Use **Evaluation Lab** to compare retrieval strategies under one versioned experiment.
3. Use **Workflow runs** to submit a bounded goal with corpus, tool and budget controls.
4. Open the run trace to compare the declared graph with the executed path, tool call, durations and citations.
5. Run **Security evidence** and inspect the benign and adversarial fixture dispositions.

## Sprint evidence

- [Sprint 1 — Semantic Search](docs/sprints/sprint-01-semantic-search/README.md)
- [Sprint 2 — Retrieval Evaluation](docs/sprints/sprint-02-retrieval-evaluation/README.md)
- [Sprint 3 — Agent Workflow Trace Viewer](docs/sprints/sprint-03-agent-trace-viewer/README.md)
- [User stories](docs/user-stories.md)
- [Technical stories](docs/technical-stories.md)
- [Architecture decisions](docs/decisions.md)
- [Security evaluation](reports/security/sprint-03-security-evaluation.md)

## Evidence boundary

- the corpus, judgments and security scenarios are small, synthetic and non-sensitive;
- deterministic local embeddings validate software contracts, not production semantic quality;
- retrieval scores are ranking signals, not confidence or truth;
- security-fixture success is regression evidence, not certification;
- the workflow is fixed, synchronous and read-only;
- authentication, tenant isolation, arbitrary tools, write actions and external LLM quality remain outside version 1.0.0;
- the AWS profile is a low-traffic portfolio topology, not production readiness or a zero-cost guarantee.

## Author

Jean Franck Loa Rojas

Software Engineer Path — Applied AI Software Systems
