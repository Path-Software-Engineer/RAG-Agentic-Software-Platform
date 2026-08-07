[CmdletBinding()]
param(
    [string]$ApiBaseUrl = "http://localhost:5300"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "request-integrity.ps1")
$Files = Get-ChildItem -LiteralPath (Join-Path $Root "data\samples") -File | Sort-Object Name

foreach ($File in $Files) {
    $Title = [System.IO.Path]::GetFileNameWithoutExtension($File.Name).Replace("-", " ")
    Invoke-HashedMultipartRequest `
        -Uri "$ApiBaseUrl/api/v1/documents" `
        -Title $Title `
        -Source "Controlled demo corpus" `
        -File $File | Out-Null
}

Write-Host "OK - controlled Sprint 1 corpus loaded."
