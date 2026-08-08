[CmdletBinding()]
param(
    [string]$Region = "us-east-1",
    [string]$Profile = "paths",
    [string]$StackName = "sf-05-rag-agent-workflow",
    [string]$RepositoryName = "sf-05-rag-agent-workflow-api",
    [string]$ImageTag = "",
    [string]$DatabaseUrlParameterName = "/sf/05/rag-agent-workflow/database-url",
    [switch]$PreflightOnly,
    [switch]$SmokeOnly,
    [switch]$ReusePublishedImage,
    [switch]$RecoverFailedStack
)

$ErrorActionPreference = "Stop"
$env:AWS_PAGER = ""
$persistentPath = @(
    [Environment]::GetEnvironmentVariable("Path", "User")
    [Environment]::GetEnvironmentVariable("Path", "Machine")
) -join ";"
$requiredWindowsPaths = @(
    (Join-Path $env:SystemRoot "System32")
    $env:SystemRoot
    (Join-Path $env:SystemRoot "System32\Wbem")
    "C:\Program Files\Git\cmd"
) -join ";"
$env:Path = "$requiredWindowsPaths;$env:Path;$persistentPath"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Template = Join-Path $PSScriptRoot "template.yaml"
$Dockerfile = Join-Path $PSScriptRoot "platform-lambda.Dockerfile"
$WebRoot = Join-Path $ProjectRoot "frontend\sveltekit-app"
$WebBuild = Join-Path $WebRoot "build"
$env:BUILDX_CONFIG = Join-Path $ProjectRoot ".tmp\docker-buildx"
New-Item -ItemType Directory -Force -Path $env:BUILDX_CONFIG | Out-Null

function Invoke-Native {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Command,
        [Parameter(Mandatory)][string[]]$Arguments,
        [AllowEmptyString()][string]$StandardInput,
        [switch]$StreamOutput
    )
    $previousErrorActionPreference = $ErrorActionPreference
    $nativePreferenceExists = Test-Path Variable:\PSNativeCommandUseErrorActionPreference
    if ($nativePreferenceExists) { $previousNativePreference = $PSNativeCommandUseErrorActionPreference }
    try {
        $ErrorActionPreference = "Continue"
        if ($nativePreferenceExists) { $PSNativeCommandUseErrorActionPreference = $false }
        $hasInput = $PSBoundParameters.ContainsKey("StandardInput")
        if ($StreamOutput) {
            $lines = [System.Collections.Generic.List[string]]::new()
            if ($hasInput) {
                $StandardInput | & $Command @Arguments 2>&1 | ForEach-Object {
                    $line = $_.ToString(); $lines.Add($line); Write-Host $line
                }
            }
            else {
                & $Command @Arguments 2>&1 | ForEach-Object {
                    $line = $_.ToString(); $lines.Add($line); Write-Host $line
                }
            }
            $output = $lines
        }
        elseif ($hasInput) { $output = $StandardInput | & $Command @Arguments 2>&1 }
        else { $output = & $Command @Arguments 2>&1 }
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
        if ($nativePreferenceExists) { $PSNativeCommandUseErrorActionPreference = $previousNativePreference }
    }
    if ($exitCode -ne 0) {
        throw "$Command failed: $Command $($Arguments -join ' ')`n$($output -join [Environment]::NewLine)"
    }
    return ($output -join [Environment]::NewLine).Trim()
}

function Get-StackOutput {
    param([Parameter(Mandatory)][string]$Key)
    return Invoke-Native -Command "aws" -Arguments @(
        "cloudformation", "describe-stacks",
        "--stack-name", $StackName,
        "--region", $Region,
        "--profile", $Profile,
        "--query", "Stacks[0].Outputs[?OutputKey=='$Key'].OutputValue | [0]",
        "--output", "text",
        "--no-cli-pager"
    )
}

function Wait-JsonHealth {
    param([Parameter(Mandatory)][string]$Uri, [Parameter(Mandatory)][string]$Label)
    $lastError = ""
    for ($attempt = 1; $attempt -le 24; $attempt++) {
        try {
            $response = Invoke-RestMethod -Uri $Uri -Method Get -TimeoutSec 30
            if ($response.status -in @("ok", "ready")) { return }
            $lastError = "unexpected status '$($response.status)'"
        }
        catch { $lastError = $_.Exception.Message }
        if ($attempt -lt 24) {
            Write-Host "$Label is not ready ($attempt/24); retrying in 10 seconds."
            Start-Sleep -Seconds 10
        }
    }
    throw "$Label did not become ready. Last error: $lastError"
}

function Wait-Document {
    param(
        [Parameter(Mandatory)][string]$Uri,
        [Parameter(Mandatory)][string]$Label,
        [Parameter(Mandatory)][string]$ExpectedText
    )
    $lastError = ""
    for ($attempt = 1; $attempt -le 18; $attempt++) {
        try {
            $response = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 30
            if ($response.StatusCode -eq 200 -and $response.Content -like "*$ExpectedText*") { return }
            $lastError = "HTTP $($response.StatusCode) without '$ExpectedText'"
        }
        catch { $lastError = $_.Exception.Message }
        if ($attempt -lt 18) {
            Write-Host "$Label is not ready ($attempt/18); retrying in 10 seconds."
            Start-Sleep -Seconds 10
        }
    }
    throw "$Label did not become ready. Last error: $lastError"
}

function Assert-Preflight {
    foreach ($command in @("aws", "git")) {
        if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
            throw "$command is required for the AWS deployment workflow."
        }
    }
    if (-not $SmokeOnly) {
        foreach ($command in @("docker", "node", "npm")) {
            if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
                throw "$command is required to build the immutable release."
            }
        }
    }

    $version = Invoke-Native -Command "aws" -Arguments @("--version")
    if ($version -notmatch '^aws-cli/2\.') { throw "AWS CLI v2 is required; detected: $version" }

    $identity = Invoke-Native -Command "aws" -Arguments @(
        "sts", "get-caller-identity", "--profile", $Profile, "--output", "json", "--no-cli-pager"
    ) | ConvertFrom-Json
    if (-not $identity.Account) { throw "AWS caller identity did not include an account ID." }

    $budgetCount = Invoke-Native -Command "aws" -Arguments @(
        "budgets", "describe-budgets",
        "--account-id", $identity.Account,
        "--profile", $Profile,
        "--query", "length(Budgets)",
        "--output", "text",
        "--no-cli-pager"
    )
    if ([int]$budgetCount -lt 1) {
        throw "No AWS budget exists for this account. Create a low monthly alert budget first."
    }

    Invoke-Native -Command "aws" -Arguments @(
        "ssm", "get-parameter",
        "--name", $DatabaseUrlParameterName,
        "--region", $Region,
        "--profile", $Profile,
        "--query", "Parameter.Name",
        "--output", "text",
        "--no-cli-pager"
    ) | Out-Null

    Invoke-Native -Command "aws" -Arguments @(
        "cloudformation", "validate-template",
        "--template-body", "file://$Template",
        "--region", $Region,
        "--profile", $Profile,
        "--no-cli-pager"
    ) | Out-Null

    if (-not $SmokeOnly) {
        Invoke-Native -Command "docker" -Arguments @("info", "--format", "{{.ServerVersion}}") | Out-Null
        Invoke-Native -Command "node" -Arguments @("--version") | Out-Null
        Invoke-Native -Command "npm" -Arguments @("--version") | Out-Null
    }
    return $identity
}

Write-Host "[1/8] Verifying AWS identity, budget, secret, template and local tools"
$identity = Assert-Preflight
$unreservedConcurrency = [int](Invoke-Native -Command "aws" -Arguments @(
    "lambda", "get-account-settings",
    "--region", $Region,
    "--profile", $Profile,
    "--query", "AccountLimit.UnreservedConcurrentExecutions",
    "--output", "text",
    "--no-cli-pager"
))
$useReservedConcurrency = if ($unreservedConcurrency -gt 100) { "true" } else { "false" }
if ($useReservedConcurrency -eq "true") {
    Write-Host "Lambda quota supports a one-execution reservation while preserving 100 unreserved executions."
}
else {
    Write-Host "Lambda exposes only $unreservedConcurrency unreserved executions; the stack will not request an invalid function reservation."
}
if ($PreflightOnly) {
    Write-Host "OK - AWS deployment preflight passed for account $($identity.Account)."
    return
}

if ($SmokeOnly) {
    Write-Host "Verifying the existing serverless deployment without changing resources"
    $applicationUrl = Get-StackOutput -Key "ApplicationUrl"
    Wait-JsonHealth -Uri "$applicationUrl/health.json" -Label "SvelteKit web"
    Wait-JsonHealth -Uri "$applicationUrl/healthz" -Label "NestJS API"
    Wait-Document -Uri "$applicationUrl/api/docs" -Label "Swagger UI" -ExpectedText "swagger-ui"
    $tools = @(Invoke-RestMethod -Uri "$applicationUrl/api/v1/agents/tools" -Method Get -TimeoutSec 30)
    if ($tools.Count -ne 3) { throw "Expected exactly three allowlisted agent tools." }
    Write-Host "OK - remote AWS smoke checks passed: $applicationUrl"
    return
}

if (-not $ImageTag) {
    $ImageTag = (git -C $ProjectRoot rev-parse --short=12 HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Unable to derive the image tag from Git." }
}
if ($ImageTag -notmatch '^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$') {
    throw "ImageTag is not a valid ECR tag."
}

$stackStatus = Invoke-Native -Command "aws" -Arguments @(
    "cloudformation", "list-stacks",
    "--stack-status-filter", "CREATE_COMPLETE", "UPDATE_COMPLETE", "ROLLBACK_COMPLETE", "UPDATE_ROLLBACK_COMPLETE",
    "--region", $Region,
    "--profile", $Profile,
    "--query", "StackSummaries[?StackName=='$StackName'].StackStatus | [0]",
    "--output", "text",
    "--no-cli-pager"
)
if ($stackStatus -eq "ROLLBACK_COMPLETE") {
    if (-not $RecoverFailedStack) {
        throw "Stack $StackName is in ROLLBACK_COMPLETE. Rerun with -RecoverFailedStack."
    }
    Write-Host "Recovering only the failed Project 05 stack"
    Invoke-Native -Command "aws" -Arguments @(
        "cloudformation", "delete-stack", "--stack-name", $StackName,
        "--region", $Region, "--profile", $Profile, "--no-cli-pager"
    ) | Out-Null
    Invoke-Native -Command "aws" -Arguments @(
        "cloudformation", "wait", "stack-delete-complete", "--stack-name", $StackName,
        "--region", $Region, "--profile", $Profile, "--no-cli-pager"
    ) -StreamOutput | Out-Null
}

Write-Host "[2/8] Ensuring the private immutable ECR repository"
$repositoryUri = Invoke-Native -Command "aws" -Arguments @(
    "ecr", "describe-repositories",
    "--region", $Region,
    "--profile", $Profile,
    "--query", "repositories[?repositoryName=='$RepositoryName'].repositoryUri | [0]",
    "--output", "text",
    "--no-cli-pager"
)
if (-not $repositoryUri -or $repositoryUri -eq "None") {
    $repositoryUri = Invoke-Native -Command "aws" -Arguments @(
        "ecr", "create-repository",
        "--repository-name", $RepositoryName,
        "--image-scanning-configuration", "scanOnPush=true",
        "--image-tag-mutability", "IMMUTABLE",
        "--region", $Region,
        "--profile", $Profile,
        "--query", "repository.repositoryUri",
        "--output", "text",
        "--no-cli-pager"
    )
}

$lifecycleFile = Join-Path ([System.IO.Path]::GetTempPath()) ("sf05-ecr-" + [guid]::NewGuid() + ".json")
try {
    $policy = @{
        rules = @(
            @{ rulePriority = 1; description = "Remove untagged images after one day"; selection = @{ tagStatus = "untagged"; countType = "sinceImagePushed"; countUnit = "days"; countNumber = 1 }; action = @{ type = "expire" } },
            @{ rulePriority = 2; description = "Keep only two immutable release images"; selection = @{ tagStatus = "any"; countType = "imageCountMoreThan"; countNumber = 2 }; action = @{ type = "expire" } }
        )
    } | ConvertTo-Json -Depth 8 -Compress
    [System.IO.File]::WriteAllText($lifecycleFile, $policy, [System.Text.UTF8Encoding]::new($false))
    Invoke-Native -Command "aws" -Arguments @(
        "ecr", "put-lifecycle-policy", "--repository-name", $RepositoryName,
        "--lifecycle-policy-text", "file://$lifecycleFile",
        "--region", $Region, "--profile", $Profile, "--no-cli-pager"
    ) | Out-Null
}
finally { Remove-Item -LiteralPath $lifecycleFile -Force -ErrorAction SilentlyContinue }

$imageUri = "$repositoryUri`:$ImageTag"
if ($ReusePublishedImage) {
    Write-Host "[3/8] Verifying the existing immutable platform image"
    Invoke-Native -Command "aws" -Arguments @(
        "ecr", "describe-images", "--repository-name", $RepositoryName,
        "--image-ids", "imageTag=$ImageTag", "--region", $Region,
        "--profile", $Profile, "--no-cli-pager"
    ) | Out-Null
}
else {
    Write-Host "[3/8] Building and publishing the immutable serverless platform image"
    $registry = $repositoryUri.Split('/')[0]
    $password = Invoke-Native -Command "aws" -Arguments @(
        "ecr", "get-login-password", "--region", $Region, "--profile", $Profile
    )
    Invoke-Native -Command "docker" -Arguments @(
        "login", "--username", "AWS", "--password-stdin", $registry
    ) -StandardInput $password | Out-Null
    Invoke-Native -Command "docker" -Arguments @(
        "buildx", "build", "--platform", "linux/amd64", "--provenance=false",
        "--progress", "plain", "--file", $Dockerfile, "--tag", $imageUri,
        "--load", $ProjectRoot
    ) -StreamOutput | Out-Null
    Invoke-Native -Command "docker" -Arguments @("push", $imageUri) -StreamOutput | Out-Null
}

Write-Host "[4/8] Deploying the cost-bounded CloudFormation stack"
try {
    Invoke-Native -Command "aws" -Arguments @(
        "cloudformation", "deploy", "--template-file", $Template,
        "--stack-name", $StackName, "--region", $Region, "--profile", $Profile,
        "--capabilities", "CAPABILITY_NAMED_IAM", "--no-fail-on-empty-changeset",
        "--parameter-overrides", "PlatformImageUri=$imageUri",
        "DatabaseUrlParameterName=$DatabaseUrlParameterName",
        "UseReservedConcurrency=$useReservedConcurrency",
        "--no-cli-pager"
    ) -StreamOutput | Out-Null
}
catch {
    Write-Host "CloudFormation failed. Fetching failed Project 05 resource events."
    try {
        Invoke-Native -Command "aws" -Arguments @(
            "cloudformation", "describe-stack-events",
            "--stack-name", $StackName,
            "--region", $Region,
            "--profile", $Profile,
            "--query", "StackEvents[?contains(ResourceStatus, 'FAILED')].[Timestamp,LogicalResourceId,ResourceType,ResourceStatus,ResourceStatusReason]",
            "--output", "table",
            "--no-cli-pager"
        ) -StreamOutput | Out-Null
    }
    catch { Write-Host "CloudFormation events are not available for this failed operation." }
    throw
}

$applicationUrl = Get-StackOutput -Key "ApplicationUrl"
$webBucket = Get-StackOutput -Key "WebBucketName"
$distributionId = Get-StackOutput -Key "DistributionId"

Write-Host "[5/8] Building the real SvelteKit release against the same CloudFront origin"
$previousApiUrl = $env:PUBLIC_API_BASE_URL
try {
    $env:PUBLIC_API_BASE_URL = $applicationUrl
    Push-Location $ProjectRoot
    try {
        Invoke-Native -Command "npm" -Arguments @("ci", "--no-audit", "--no-fund") -StreamOutput | Out-Null
        Invoke-Native -Command "npm" -Arguments @("run", "build", "--workspace", "@rag-platform/web") -StreamOutput | Out-Null
    }
    finally { Pop-Location }
}
finally { $env:PUBLIC_API_BASE_URL = $previousApiUrl }

[System.IO.File]::WriteAllText(
    (Join-Path $WebBuild "health.json"),
    '{"status":"ready","service":"sf-05-rag-agent-workflow-web"}',
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "[6/8] Publishing the private SvelteKit origin"
Invoke-Native -Command "aws" -Arguments @(
    "s3", "sync", $WebBuild, "s3://$webBucket", "--delete",
    "--cache-control", "public,max-age=3600", "--exclude", "index.html",
    "--exclude", "health.json", "--region", $Region, "--profile", $Profile
) | Out-Null
foreach ($file in @("index.html", "health.json")) {
    $contentType = if ($file.EndsWith(".json")) { "application/json" } else { "text/html" }
    Invoke-Native -Command "aws" -Arguments @(
        "s3", "cp", (Join-Path $WebBuild $file), "s3://$webBucket/$file",
        "--cache-control", "no-store", "--content-type", $contentType,
        "--region", $Region, "--profile", $Profile
    ) | Out-Null
}

Write-Host "[7/8] Invalidating the CloudFront release boundary"
Invoke-Native -Command "aws" -Arguments @(
    "cloudfront", "create-invalidation", "--distribution-id", $distributionId,
    "--paths", "/*", "--profile", $Profile, "--no-cli-pager"
) | Out-Null

Write-Host "[8/8] Running remote health, demo and governed-agent smoke checks"
Wait-JsonHealth -Uri "$applicationUrl/health.json" -Label "SvelteKit web"
Wait-JsonHealth -Uri "$applicationUrl/healthz" -Label "NestJS API"
Wait-Document -Uri "$applicationUrl/api/docs" -Label "Swagger UI" -ExpectedText "swagger-ui"
& (Join-Path $ProjectRoot "scripts\seed-demo.ps1") -ApiBaseUrl $applicationUrl
if ($LASTEXITCODE -ne 0) { throw "Remote Sprint 1 demo seeding failed." }
& (Join-Path $ProjectRoot "scripts\seed-evaluation-demo.ps1") -ApiBaseUrl $applicationUrl
if ($LASTEXITCODE -ne 0) { throw "Remote Sprint 2 demo seeding failed." }
& (Join-Path $ProjectRoot "scripts\seed-agent-demo.ps1") -ApiBaseUrl $applicationUrl
if ($LASTEXITCODE -ne 0) { throw "Remote Sprint 3 demo seeding failed." }

Write-Host "OK - AWS deployment is ready: $applicationUrl"
Write-Host "Swagger: $applicationUrl/api/docs"
