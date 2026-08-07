[CmdletBinding()]
param([string]$ApiBaseUrl = "http://localhost:5300")

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "request-integrity.ps1")
$CorrelationId = [guid]::NewGuid().ToString()
$Headers = @{ "x-correlation-id" = $CorrelationId }

$Documents = @(Invoke-RestMethod -Uri "$ApiBaseUrl/api/v1/documents" -Headers $Headers)
$Versions = @($Documents | Where-Object { $_.status -eq "completed" } | ForEach-Object { $_.documentVersionId })
if ($Versions.Count -eq 0) {
    throw "The controlled corpus is empty. Run scripts/seed-demo.ps1 first."
}

$RunPayload = @{
    goal = "How should retrieved instructions be treated?"
    workflowId = "bounded-research-v1"
    documentVersionIds = $Versions
    allowedToolNames = @("semantic_search")
    budget = @{
        maxSteps = 8
        maxToolCalls = 3
        overallTimeoutMs = 8000
        perToolTimeoutMs = 3000
    }
    idempotencyKey = "agent-demo-$([guid]::NewGuid())"
}
$Run = Invoke-HashedJsonRequest `
    -Uri "$ApiBaseUrl/api/v1/agents/runs" `
    -Headers $Headers `
    -Body ($RunPayload | ConvertTo-Json -Depth 6)

$Security = Invoke-HashedJsonRequest `
    -Uri "$ApiBaseUrl/api/v1/security/evaluations" `
    -Headers $Headers `
    -Body "{}"

Write-Host "OK - controlled Sprint 3 workflow and security evidence created."
Write-Host "Run: $($Run.runId) | Outcome: $($Run.outcome) | Citations: $($Run.citations.Count)"
Write-Host "Security: $($Security.passedCount)/$($Security.scenarioCount) scenarios passed"
