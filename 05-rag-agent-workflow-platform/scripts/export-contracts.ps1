$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$Python = "python"
if (Test-Path -LiteralPath $VenvPython) {
    $PreviousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $VenvPython -c "import fastapi" *> $null
    $VenvReady = $LASTEXITCODE -eq 0
    $ErrorActionPreference = $PreviousErrorAction
    if ($VenvReady) { $Python = $VenvPython }
}
Push-Location $Root
try {
    npm run build --workspace @rag-platform/api
    if ($LASTEXITCODE -ne 0) { throw "NestJS build failed before OpenAPI export." }
    node backend/nestjs-api/scripts/export-openapi.cjs
    if ($LASTEXITCODE -ne 0) { throw "Public OpenAPI export failed." }

    $env:PYTHONPATH = (Resolve-Path "ai-services\rag-agent-service").Path
    & $Python ai-services/rag-agent-service/scripts/export_openapi.py
    if ($LASTEXITCODE -ne 0) { throw "Internal OpenAPI export failed." }
} finally {
    Pop-Location
}
Write-Host "OK - public and internal OpenAPI contracts exported."
