[CmdletBinding()]
param(
    [string]$ApiBaseUrl = "http://localhost:5300"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Files = Get-ChildItem -LiteralPath (Join-Path $Root "data\samples") -File | Sort-Object Name

foreach ($File in $Files) {
    $Title = [System.IO.Path]::GetFileNameWithoutExtension($File.Name).Replace("-", " ")
    $Arguments = @(
        "--silent", "--show-error", "--fail-with-body",
        "--request", "POST",
        "--form", "title=$Title",
        "--form", "source=Controlled demo corpus",
        "--form", "file=@$($File.FullName)",
        "$ApiBaseUrl/api/v1/documents"
    )
    & curl.exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Demo ingestion failed for $($File.Name)." }
    Write-Host ""
}

Write-Host "OK - controlled Sprint 1 corpus loaded."
