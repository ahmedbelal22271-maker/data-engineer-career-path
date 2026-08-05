# Measure the always-injected instruction load (bytes, lines, words, token estimate).
# Usage:  . .agents/skills/context_bloat_audit/scripts/measure_context_load.ps1
# Output: per-file table + totals + delta vs the baseline recorded in
#         references/context_bloat_evidence.md section 4.

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $scriptDir)))
$configPath = Join-Path $repoRoot 'opencode.json'

if (-not (Test-Path -LiteralPath $configPath)) {
    Write-Error "opencode.json not found at $configPath"
    exit 1
}

$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
if (-not $config.instructions -or $config.instructions.Count -eq 0) {
    Write-Output "No instructions array found in opencode.json."
    exit 0
}

$rows = foreach ($rel in $config.instructions) {
    $path = Join-Path $repoRoot ($rel -replace '/', '\')
    if (Test-Path -LiteralPath $path) {
        $content = Get-Content -LiteralPath $path -Raw
        $bytes   = (Get-Item -LiteralPath $path).Length
        $lines   = ($content -split "`n").Count
        $words   = ($content -split '\s+' | Where-Object { $_ }).Count
        $tokens  = [math]::Round($bytes / 4.0)
        [pscustomobject]@{ File = $rel; Bytes = $bytes; Lines = $lines; Words = $words; Tokens = $tokens }
    } else {
        [pscustomobject]@{ File = $rel; Bytes = 0; Lines = 0; Words = 0; Tokens = 0 }
        Write-Warning "MISSING: $rel"
    }
}

$rows | Format-Table -AutoSize
$totalTokens = ($rows | Measure-Object -Property Tokens -Sum).Sum
$totalBytes  = ($rows | Measure-Object -Property Bytes -Sum).Sum

Write-Output ("TOTAL injected load: {0:N0} bytes / {1:N0} tokens (approx, bytes/4)" -f $totalBytes, $totalTokens)
Write-Output "Baseline (evidence file section 4, re-measured 2026-08-05): ~39,461 tokens across 6 files."
$delta = $totalTokens - 39461
if ($delta -gt 0) { Write-Output "DELTA vs baseline: +$delta tokens (LOAD GREW — audit bloat)" }
else { Write-Output "DELTA vs baseline: $delta tokens" }
