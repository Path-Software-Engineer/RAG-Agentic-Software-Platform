Add-Type -AssemblyName System.Net.Http

function Get-PayloadSha256 {
    param([Parameter(Mandatory)][byte[]]$Bytes)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [System.BitConverter]::ToString($sha256.ComputeHash($Bytes)).Replace("-", "").ToLowerInvariant()
    }
    finally { $sha256.Dispose() }
}

function Invoke-HashedJsonRequest {
    param(
        [Parameter(Mandatory)][string]$Uri,
        [ValidateSet("POST", "PATCH")][string]$Method = "POST",
        [Parameter(Mandatory)][string]$Body,
        [hashtable]$Headers = @{}
    )
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    $requestHeaders = @{} + $Headers
    $requestHeaders["x-amz-content-sha256"] = Get-PayloadSha256 -Bytes $bytes
    return Invoke-RestMethod `
        -Uri $Uri `
        -Method $Method `
        -Headers $requestHeaders `
        -ContentType "application/json" `
        -Body $bytes `
        -TimeoutSec 75
}

function Invoke-HashedMultipartRequest {
    param(
        [Parameter(Mandatory)][string]$Uri,
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][System.IO.FileInfo]$File
    )
    $boundary = "----sf05-$([guid]::NewGuid().ToString('N'))"
    $multipart = [System.Net.Http.MultipartFormDataContent]::new($boundary)
    $client = [System.Net.Http.HttpClient]::new()
    $request = [System.Net.Http.HttpRequestMessage]::new(
        [System.Net.Http.HttpMethod]::Post,
        $Uri
    )
    try {
        $multipart.Add([System.Net.Http.StringContent]::new($Title), "title")
        $multipart.Add([System.Net.Http.StringContent]::new($Source), "source")
        $fileContent = [System.Net.Http.ByteArrayContent]::new(
            [System.IO.File]::ReadAllBytes($File.FullName)
        )
        $mediaType = if ($File.Extension -eq ".md") { "text/markdown" } else { "text/plain" }
        $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse($mediaType)
        $multipart.Add($fileContent, "file", $File.Name)

        $body = $multipart.ReadAsByteArrayAsync().GetAwaiter().GetResult()
        $request.Content = [System.Net.Http.ByteArrayContent]::new($body)
        $request.Content.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse(
            "multipart/form-data; boundary=$boundary"
        )
        $request.Headers.Accept.Add(
            [System.Net.Http.Headers.MediaTypeWithQualityHeaderValue]::new("application/json")
        )
        $null = $request.Headers.TryAddWithoutValidation(
            "x-amz-content-sha256",
            (Get-PayloadSha256 -Bytes $body)
        )

        $response = $client.SendAsync($request).GetAwaiter().GetResult()
        $responseBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        if (-not $response.IsSuccessStatusCode) {
            throw "HTTP $([int]$response.StatusCode): $responseBody"
        }
        return $responseBody | ConvertFrom-Json
    }
    finally {
        $request.Dispose()
        $multipart.Dispose()
        $client.Dispose()
    }
}
