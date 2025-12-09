# Get Status of Specific Workflow Run
param(
    [Parameter(Mandatory=$true)]
    [string]$RunId
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Workflow Run Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if (-not $token) {
    Write-Host "[ERROR] GITHUB_TOKEN not found!" -ForegroundColor Red
    exit 1
}

$repo = "halvo78/ai-program-video-music-overlay"
$url = "https://api.github.com/repos/$repo/actions/runs/$RunId"

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

try {
    $run = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    
    Write-Host "Workflow: $($run.name)" -ForegroundColor Yellow
    Write-Host "   Run #$($run.run_number)" -ForegroundColor Gray
    Write-Host "   Status: $($run.status)" -ForegroundColor $(if ($run.status -eq "completed") { "Green" } else { "Yellow" })
    Write-Host "   Conclusion: $($run.conclusion)" -ForegroundColor $(if ($run.conclusion -eq "success") { "Green" } else { "Red" })
    Write-Host "   Created: $($run.created_at)" -ForegroundColor Gray
    Write-Host "   Updated: $($run.updated_at)" -ForegroundColor Gray
    Write-Host "   URL: $($run.html_url)" -ForegroundColor Cyan
    Write-Host ""
    
    # Get jobs
    $jobsUrl = "$url/jobs"
    $jobs = Invoke-RestMethod -Uri $jobsUrl -Headers $headers -Method Get
    
    Write-Host "Jobs:" -ForegroundColor Yellow
    foreach ($job in $jobs.jobs) {
        $statusColor = switch ($job.status) {
            "completed" { "Green" }
            "in_progress" { "Yellow" }
            "queued" { "Cyan" }
            default { "Gray" }
        }
        Write-Host "   $($job.name): $($job.status) - $($job.conclusion)" -ForegroundColor $statusColor
    }
    
} catch {
    Write-Host "[ERROR] Failed to get workflow run: $_" -ForegroundColor Red
    exit 1
}
