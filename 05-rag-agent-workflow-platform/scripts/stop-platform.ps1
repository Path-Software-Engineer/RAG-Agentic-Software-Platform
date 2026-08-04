$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    & docker compose down
    if ($LASTEXITCODE -ne 0) { throw "The local platform could not be stopped cleanly." }
} finally {
    Pop-Location
}
