[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Push-Location $Root
try {
    foreach ($Command in @("node", "npm", "python", "docker")) {
        if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
            throw "$Command is required but was not found on PATH."
        }
    }

    if (-not (Test-Path -LiteralPath $Python)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Python virtual environment creation failed." }
    }
    & $Python -m pip --version *> $null
    if ($LASTEXITCODE -ne 0) {
        & $Python -m ensurepip --upgrade
        if ($LASTEXITCODE -ne 0) { throw "pip could not be initialized inside .venv." }
    }
    & $Python -m pip install --disable-pip-version-check -r ai-services/rag-agent-service/requirements.lock
    if ($LASTEXITCODE -ne 0) { throw "Locked Python dependency installation failed." }

    npm ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw "Locked Node dependency installation failed." }

    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration is invalid." }
    Write-Host "OK - Sprint 1 development environment is ready."
} finally {
    Pop-Location
}
