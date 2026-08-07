[CmdletBinding()]
param(
    [string]$Region = "us-east-1",
    [string]$Profile = "paths",
    [string]$DatabaseUrlParameterName = "/sf/05/rag-agent-workflow/database-url"
)

$ErrorActionPreference = "Stop"
$env:AWS_PAGER = ""

function Invoke-Aws {
    param([Parameter(Mandatory)][string[]]$Arguments)
    $output = & aws @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI failed: aws $($Arguments -join ' ')`n$($output -join [Environment]::NewLine)"
    }
    return ($output -join [Environment]::NewLine).Trim()
}

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    throw "AWS CLI v2 is required."
}

$databaseUrlSecure = Read-Host "Neon PostgreSQL DATABASE_URL (pooled TLS endpoint)" -AsSecureString
$databaseUrl = [System.Net.NetworkCredential]::new("", $databaseUrlSecure).Password

if ($databaseUrl -notmatch '^postgres(ql)?://') {
    throw "DATABASE_URL must use the postgres:// or postgresql:// scheme."
}
if ($databaseUrl -notmatch '(?i)[?&]sslmode=require(?:&|$)') {
    throw "DATABASE_URL must require TLS with sslmode=require."
}

$temporaryFile = Join-Path ([System.IO.Path]::GetTempPath()) ("sf05-ssm-" + [guid]::NewGuid() + ".json")
try {
    $payload = @{
        Name = $DatabaseUrlParameterName
        Value = $databaseUrl
        Type = "SecureString"
        Tier = "Standard"
        Overwrite = $true
        Description = "Neon PostgreSQL pooled TLS URL for Software Engineer Project 05"
    } | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText(
        $temporaryFile,
        $payload,
        [System.Text.UTF8Encoding]::new($false)
    )
    Invoke-Aws -Arguments @(
        "ssm", "put-parameter",
        "--region", $Region,
        "--profile", $Profile,
        "--cli-input-json", "file://$temporaryFile",
        "--no-cli-pager"
    ) | Out-Null
}
finally {
    $databaseUrl = $null
    Remove-Item -LiteralPath $temporaryFile -Force -ErrorAction SilentlyContinue
}

Write-Host "AWS SSM SecureString configured without writing the Neon URL to the repository."
