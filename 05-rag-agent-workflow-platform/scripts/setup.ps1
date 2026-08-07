[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$SetupTemp = Join-Path $Root ".tmp\setup"
$PreviousTemp = $env:TEMP
$PreviousTmp = $env:TMP

Push-Location $Root
try {
    New-Item -ItemType Directory -Path $SetupTemp -Force | Out-Null
    $env:TEMP = $SetupTemp
    $env:TMP = $SetupTemp

    foreach ($Command in @("node", "npm", "python", "docker")) {
        if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
            throw "$Command is required but was not found on PATH."
        }
    }

    if (-not (Test-Path -LiteralPath $Python)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Python virtual environment creation failed." }
    }
    # A partially-created virtual environment may contain python.exe without pip.
    # Bootstrap pip first so PowerShell's native error handling cannot abort the
    # setup before the recovery path is reached.
    $PreviousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Python -m ensurepip --upgrade
        $EnsurePipExitCode = $LASTEXITCODE
        & $Python -m pip --version *> $null
        $PipVersionExitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $PreviousErrorActionPreference
    }
    if ($EnsurePipExitCode -ne 0) { throw "pip could not be initialized inside .venv." }
    if ($PipVersionExitCode -ne 0) { throw "pip is unavailable inside .venv after bootstrap." }
    & $Python -m pip install --disable-pip-version-check -r ai-services/rag-agent-service/requirements.lock
    if ($LASTEXITCODE -ne 0) { throw "Locked Python dependency installation failed." }

    npm ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw "Locked Node dependency installation failed." }

    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration is invalid." }
    Write-Host "OK - Sprint 3 development environment is ready."
} finally {
    $env:TEMP = $PreviousTemp
    $env:TMP = $PreviousTmp
    Pop-Location
}
