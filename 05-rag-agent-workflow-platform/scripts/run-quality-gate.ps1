[CmdletBinding()]
param([switch]$SkipBuild)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$Python = "python"
if (Test-Path -LiteralPath $VenvPython) {
    $PreviousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $VenvPython -c "import mypy, pytest, ruff" *> $null
    $VenvReady = $LASTEXITCODE -eq 0
    $ErrorActionPreference = $PreviousErrorAction
    if ($VenvReady) { $Python = $VenvPython }
}
Push-Location $Root
try {
    $env:BUILDX_CONFIG = Join-Path $Root ".tmp\docker-buildx"
    New-Item -ItemType Directory -Force -Path $env:BUILDX_CONFIG | Out-Null

    Write-Host "[1/9] Repository and contract checks"
    & $Python tests/contracts/check_contracts.py
    if ($LASTEXITCODE -ne 0) { throw "Contract boundary check failed." }
    & $Python tests/contracts/check_aws_deployment.py
    if ($LASTEXITCODE -ne 0) { throw "AWS deployment boundary check failed." }

    Write-Host "[2/9] Python static checks and unit tests"
    $env:PYTHONPATH = (Resolve-Path "ai-services\rag-agent-service").Path
    & $Python -m ruff check ai-services/rag-agent-service/app ai-services/rag-agent-service/tests tests
    if ($LASTEXITCODE -ne 0) { throw "Ruff check failed." }
    & $Python -m mypy ai-services/rag-agent-service/app
    if ($LASTEXITCODE -ne 0) { throw "Mypy check failed." }
    & $Python -m pytest ai-services/rag-agent-service/tests -q -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { throw "Python unit or contract tests failed." }

    Write-Host "[3/9] Docker Compose configuration"
    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration failed." }

    if (-not $SkipBuild) {
        Write-Host "[4/9] Immutable service builds"
        docker compose build
        if ($LASTEXITCODE -ne 0) { throw "Docker service build failed." }
    } else {
        Write-Host "[4/9] Builds reused by explicit request"
    }

    Write-Host "[5/9] Empty-database migration"
    docker compose down --volumes --remove-orphans
    if ($LASTEXITCODE -ne 0) { throw "Previous project-local runtime could not be cleared." }
    docker compose up -d postgres redis migrate
    if ($LASTEXITCODE -ne 0) { throw "Infrastructure could not start." }
    docker compose wait migrate
    if ($LASTEXITCODE -ne 0) { docker compose logs migrate; throw "Database migrations failed." }
    $Healthy = $false
    for ($Attempt = 1; $Attempt -le 24; $Attempt++) {
        $States = docker compose ps --format json | ConvertFrom-Json
        $Unhealthy = @($States | Where-Object { $_.Health -and $_.Health -ne "healthy" })
        if ($States.Count -ge 2 -and $Unhealthy.Count -eq 0) { $Healthy = $true; break }
        Start-Sleep -Seconds 3
    }
    if (-not $Healthy) { docker compose logs postgres redis; throw "Infrastructure did not become healthy." }
    $Vector = docker compose exec -T postgres psql -U rag_platform -d rag_platform -tAc "SELECT extversion FROM pg_extension WHERE extname='vector'"
    if (-not $Vector.Trim()) { throw "pgvector migration evidence is missing." }
    $EvaluationTables = docker compose exec -T postgres psql -U rag_platform -d rag_platform -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='rag' AND table_name IN ('document_sources','retrieval_test_cases','evaluation_runs','relevance_labels')"
    if ($EvaluationTables.Trim() -ne "4") { throw "Sprint 2 evaluation migration evidence is incomplete." }
    $AgentTables = docker compose exec -T postgres psql -U rag_platform -d rag_platform -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='agent' AND table_name IN ('agent_runs','agent_steps','tool_calls','trace_events','agent_checkpoints','security_evaluations')"
    if ($AgentTables.Trim() -ne "6") { throw "Sprint 3 agent migration evidence is incomplete." }

    Write-Host "[6/9] Containerized service tests"
    docker compose run --rm rag-service python -m pytest -q --cov=app --cov-report=term-missing
    if ($LASTEXITCODE -ne 0) { throw "Python container tests failed." }
    docker build --target build -f backend/nestjs-api/Dockerfile -t sf-05-api-check .
    if ($LASTEXITCODE -ne 0) { throw "NestJS check image build failed." }
    docker run --rm sf-05-api-check npm test --workspace @rag-platform/api -- --runInBand
    if ($LASTEXITCODE -ne 0) { throw "NestJS tests failed." }

    Write-Host "[7/9] Frontend tests and compilation"
    docker build --target build -f frontend/sveltekit-app/Dockerfile -t sf-05-web-check .
    if ($LASTEXITCODE -ne 0) { throw "SvelteKit build failed." }
    docker run --rm sf-05-web-check npm test --workspace @rag-platform/web
    if ($LASTEXITCODE -ne 0) { throw "SvelteKit component tests failed." }

    Write-Host "[8/9] Integrated runtime and E2E"
    docker compose up -d
    if ($LASTEXITCODE -ne 0) { throw "Integrated platform could not start." }
    $Ready = $false
    for ($Attempt = 1; $Attempt -le 30; $Attempt++) {
        try {
            $Health = Invoke-RestMethod -Uri "http://localhost:5300/healthz" -TimeoutSec 3
            $Web = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:5173/healthz" -TimeoutSec 3
            if ($Health.status -eq "ok" -and $Web.StatusCode -eq 200) { $Ready = $true; break }
        } catch { Start-Sleep -Seconds 3 }
    }
    if (-not $Ready) { docker compose logs; throw "Integrated platform did not become healthy." }
    & $Python tests/integration/test_semantic_search_e2e.py
    if ($LASTEXITCODE -ne 0) { throw "Semantic-search E2E failed." }
    & $Python tests/integration/test_retrieval_evaluation_e2e.py
    if ($LASTEXITCODE -ne 0) { throw "Retrieval-evaluation E2E failed." }
    & $Python tests/integration/test_agent_trace_viewer_e2e.py
    if ($LASTEXITCODE -ne 0) { throw "Agent trace viewer E2E failed." }
    .\scripts\export-contracts.ps1

    Write-Host "[9/9] Git whitespace and boundary"
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw "Git whitespace validation failed." }
    Write-Host "OK - complete Sprint 3 Agent Workflow Trace Viewer quality gate passed"
} finally {
    Pop-Location
}
