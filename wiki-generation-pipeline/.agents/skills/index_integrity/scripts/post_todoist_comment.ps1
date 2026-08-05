<#
.SYNOPSIS
    Posts a comment to a Todoist task in the Index Integrity Patches section.

.DESCRIPTION
    Used by the index_integrity skill to auto-comment on patch tasks when implementing,
    testing, or blocking a patch. Reads the Todoist API key from the project .env file.

.PARAMETER TaskId
    The Todoist task ID to post the comment to.

.PARAMETER Comment
    The comment content to post.

.EXAMPLE
    . .agents/skills/index_integrity/scripts/post_todoist_comment.ps1 -TaskId "6h4rj3Xjr6v83PM4" -Comment "IMPLEMENTED (TESTED) — description here"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$TaskId,
    [Parameter(Mandatory=$true)]
    [string]$Comment
)

$envFile = Join-Path $PSScriptRoot "..\..\..\..\.env"
if (-not (Test-Path -LiteralPath $envFile)) {
    # Try from wiki-generation-pipeline root
    $envFile = "C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\.env"
}

$tokenLine = Get-Content -LiteralPath $envFile -ErrorAction SilentlyContinue | Where-Object { $_ -match "TODOIST_API_KEY" }
if ($tokenLine -match 'TODOIST_API_KEY=(.+)') {
    $token = $Matches[1].Trim()
} else {
    Write-Error "No TODOIST_API_KEY found in .env file"
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    task_id = $TaskId
    content = $Comment
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "https://api.todoist.com/api/v1/comments" -Headers $headers -Method Post -Body $body
    Write-Output "Comment posted successfully to task $TaskId"
    Write-Output "Comment ID: $($result.id)"
} catch {
    Write-Error "Failed to post comment: $_"
    exit 1
}
