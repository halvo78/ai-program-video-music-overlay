# List GitHub Actions Workflow Runs
param(
    [Parameter(Mandatory=$false)]
    [int]$Limit = 10
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Actions Workflow Runs" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if (-not $token) {
    Write-Host "[ERROR] GITHUB_TOKEN not found!" -ForegroundColor Red
    exit 1
}

$repo = "halvo78/ai-program-video-music-overlay"
$url = "https://api.github.com/repos/$repo/actions/runs?per_page=$Limit"

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

try {
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    $runs = $response.workflow_runs
    
    Write-Host "Total Runs: $($response.total_count)" -ForegroundColor Yellow
    Write-Host ""
    
    if ($runs.Count -eq 0) {
        Write-Host "No workflow runs found." -ForegroundColor Yellow
        exit 0
    }
    
    foreach ($run in $runs) {
        $statusColor = switch ($run.status) {
            "completed" { "Green" }
            "in_progress" { "Yellow" }
            "queued" { "Cyan" }
            default { "Gray" }
        }
        
        $conclusionColor = switch ($run.conclusion) {
            "success" { "Green" }
            "failure" { "Red" }
            "cancelled" { "Yellow" }
            default { "Gray" }
        }
        
        Write-Host "Run #$($run.run_number) - $($run.name)" -ForegroundColor White
        Write-Host "   ID: $($run.id)" -ForegroundColor Gray
        Write-Host "   Status: $($run.status)" -ForegroundColor $statusColor
        Write-Host "   Conclusion: $($run.conclusion)" -ForegroundColor $conclusionColor
        Write-Host "   Created: $($run.created_at)" -ForegroundColor Gray
        Write-Host "   URL: $($run.html_url)" -ForegroundColor Cyan
        Write-Host ""
    }
    
} catch {
    Write-Host "[ERROR] Failed to get workflow runs: $_" -ForegroundColor Red
    exit 1
}
