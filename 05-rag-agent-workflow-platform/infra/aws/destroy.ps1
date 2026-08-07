[CmdletBinding()]
param(
    [string]$Region = "us-east-1",
    [string]$Profile = "paths",
    [string]$StackName = "sf-05-rag-agent-workflow",
    [string]$RepositoryName = "sf-05-rag-agent-workflow-api",
    [string]$DatabaseUrlParameterName = "/sf/05/rag-agent-workflow/database-url",
    [switch]$DeleteSecret,
    [switch]$ConfirmDestroy
)

$ErrorActionPreference = "Stop"
$env:AWS_PAGER = ""
if (-not $ConfirmDestroy) {
    throw "Pass -ConfirmDestroy to delete only the Project 05 AWS stack and ECR repository."
}

$webBucket = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --profile $Profile `
    --query "Stacks[0].Outputs[?OutputKey=='WebBucketName'].OutputValue | [0]" `
    --output text `
    --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw "The Project 05 stack could not be inspected." }

if ($webBucket -and $webBucket -ne "None") {
    aws s3 rm "s3://$webBucket" --recursive --region $Region --profile $Profile
    if ($LASTEXITCODE -ne 0) { throw "The Project 05 web bucket could not be emptied." }
}

aws cloudformation delete-stack `
    --stack-name $StackName `
    --region $Region `
    --profile $Profile `
    --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw "The Project 05 stack deletion could not be started." }
aws cloudformation wait stack-delete-complete `
    --stack-name $StackName `
    --region $Region `
    --profile $Profile `
    --no-cli-pager
if ($LASTEXITCODE -ne 0) { throw "The Project 05 stack was not deleted cleanly." }

aws ecr delete-repository `
    --repository-name $RepositoryName `
    --force `
    --region $Region `
    --profile $Profile `
    --no-cli-pager | Out-Null
if ($LASTEXITCODE -ne 0) { throw "The Project 05 ECR repository could not be deleted." }

if ($DeleteSecret) {
    aws ssm delete-parameter `
        --name $DatabaseUrlParameterName `
        --region $Region `
        --profile $Profile `
        --no-cli-pager | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "The Project 05 SSM parameter could not be deleted." }
}

Write-Host "Project 05 AWS resources were deleted. Neon PostgreSQL was not modified."
