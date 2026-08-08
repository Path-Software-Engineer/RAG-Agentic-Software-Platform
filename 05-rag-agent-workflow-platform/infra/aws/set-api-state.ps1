[CmdletBinding()]
param(
    [ValidateSet("Running", "Paused")][string]$State,
    [string]$Region = "us-east-1",
    [string]$Profile = "paths",
    [string]$FunctionName = "sf-05-rag-agent-workflow-api"
)

$ErrorActionPreference = "Stop"
$env:AWS_PAGER = ""

if ($State -eq "Paused") {
    aws lambda put-function-concurrency `
        --function-name $FunctionName `
        --reserved-concurrent-executions 0 `
        --region $Region `
        --profile $Profile `
        --no-cli-pager | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "AWS Lambda could not be paused." }
    Write-Host "$FunctionName is paused at reserved concurrency 0."
    return
}

$unreservedConcurrency = aws lambda get-account-settings `
    --region $Region `
    --profile $Profile `
    --query "AccountLimit.UnreservedConcurrentExecutions" `
    --output text `
    --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw "AWS Lambda account concurrency could not be inspected." }

if ([int]$unreservedConcurrency -gt 100) {
    aws lambda put-function-concurrency `
        --function-name $FunctionName `
        --reserved-concurrent-executions 1 `
        --region $Region `
        --profile $Profile `
        --no-cli-pager | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "AWS Lambda could not be resumed." }
    Write-Host "$FunctionName is running with reserved concurrency 1."
    return
}

aws lambda delete-function-concurrency `
    --function-name $FunctionName `
    --region $Region `
    --profile $Profile `
    --no-cli-pager | Out-Null
if ($LASTEXITCODE -ne 0) { throw "AWS Lambda could not remove its paused concurrency setting." }
Write-Host "$FunctionName is running under the regional concurrency quota ($unreservedConcurrency); no invalid reservation was requested."
