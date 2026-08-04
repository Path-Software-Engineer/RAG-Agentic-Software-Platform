[CmdletBinding()]
param([switch]$Build)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    $Arguments = @("compose", "up", "-d")
    if ($Build) { $Arguments += "--build" }
    & docker @Arguments
    if ($LASTEXITCODE -ne 0) { throw "The local platform could not be started." }
    & docker compose ps
    Write-Host "Web:     http://localhost:5173"
    Write-Host "Swagger: http://localhost:5300/api/docs"
} finally {
    Pop-Location
}
