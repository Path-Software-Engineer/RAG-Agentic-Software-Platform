# Local Runbook

## Start

```powershell
Set-Location "C:\JeanLoa\Path-Software-Engineer\RAG-Agentic-Software-Platform\05-rag-agent-workflow-platform"
Copy-Item .env.example .env -ErrorAction SilentlyContinue
.\scripts\setup.ps1
.\scripts\run-platform.ps1 -Build
```

Open the web application at <http://localhost:5173>, public Swagger at <http://localhost:5300/api/docs>, and API health at <http://localhost:5300/healthz>.

## Seed the complete demonstration

```powershell
.\scripts\seed-demo.ps1
.\scripts\seed-evaluation-demo.ps1
.\scripts\seed-agent-demo.ps1
```

## Diagnose

```powershell
docker compose ps
docker compose logs --tail 200 postgres redis rag-service api web
docker compose config --quiet
```

Healthy runtime means PostgreSQL and Redis health checks pass, migrations complete, FastAPI and NestJS report healthy, and the web health endpoint returns 200. A container merely being started is not acceptance.

## Validate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate rebuilds from an empty project-local database volume. Do not run it when local demo data must be preserved.

## Stop

```powershell
.\scripts\stop-platform.ps1
```

Use `docker compose down --volumes --remove-orphans` only when intentionally resetting all local project data.
