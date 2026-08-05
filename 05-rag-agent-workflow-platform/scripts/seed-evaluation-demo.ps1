[CmdletBinding()]
param([string]$ApiBaseUrl = "http://localhost:5300")

$ErrorActionPreference = "Stop"

$Documents = @(Invoke-RestMethod -Uri "$ApiBaseUrl/api/v1/documents" -Method Get)
$Completed = @($Documents | Where-Object { $_.status -eq "completed" })
if ($Completed.Count -lt 2) {
    throw "At least two completed documents are required. Run scripts/seed-demo.ps1 first."
}

$ByFilename = @{}
foreach ($Document in $Completed) { $ByFilename[$Document.filename] = $Document }
foreach ($Required in @("retrieval-safety.md", "chunking-guide.md", "citation-policy.txt")) {
    if (-not $ByFilename.ContainsKey($Required)) {
        throw "The controlled demo corpus is missing $Required."
    }
}

$Cases = @(
    @{
        query = "How should retrieved instructions be treated?"
        relevantDocumentIds = @($ByFilename["retrieval-safety.md"].documentId)
        rationale = "The safety document contains the explicit instruction boundary."
    },
    @{
        query = "What does chunk overlap preserve?"
        relevantDocumentIds = @($ByFilename["chunking-guide.md"].documentId)
        rationale = "The chunking guide defines overlap and context preservation."
    },
    @{
        query = "How must a citation preserve provenance?"
        relevantDocumentIds = @($ByFilename["citation-policy.txt"].documentId)
        rationale = "The citation policy defines the durable provenance contract."
    }
)

$Existing = @(Invoke-RestMethod -Uri "$ApiBaseUrl/api/v1/evaluations/test-cases" -Method Get)
$SelectedCases = @()
foreach ($Case in $Cases) {
    $Match = $Existing | Where-Object { $_.query -eq $Case.query } | Select-Object -First 1
    if (-not $Match) {
        $Match = Invoke-RestMethod `
            -Uri "$ApiBaseUrl/api/v1/evaluations/test-cases" `
            -Method Post `
            -ContentType "application/json" `
            -Body ($Case | ConvertTo-Json -Depth 5)
    }
    $SelectedCases += $Match
}

$Strategies = @(Invoke-RestMethod -Uri "$ApiBaseUrl/api/v1/evaluations/strategies" -Method Get)
$Payload = @{
    strategyIds = @($Strategies.strategyId)
    testCaseIds = @($SelectedCases.testCaseId)
    documentVersionIds = @($Completed.documentVersionId)
    topK = 3
}
$Run = Invoke-RestMethod `
    -Uri "$ApiBaseUrl/api/v1/evaluations/runs" `
    -Method Post `
    -ContentType "application/json" `
    -Body ($Payload | ConvertTo-Json -Depth 5)

Write-Host "OK - controlled Sprint 2 evaluation evidence created."
Write-Host "Run: $($Run.runId)"
foreach ($Strategy in $Run.strategies) {
    Write-Host ("{0}: Precision@3={1:P1} Recall@3={2:P1} HitRate={3:P1}" -f `
        $Strategy.metrics.strategyLabel, `
        $Strategy.metrics.precisionAtK, `
        $Strategy.metrics.recallAtK, `
        $Strategy.metrics.hitRate)
}
