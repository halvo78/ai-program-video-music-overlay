# Run Cloud Agent via GitHub Actions API
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("video", "music", "image", "voice", "content", "editing", "optimization", "analytics", "safety", "social", "all")]
    [string]$AgentType = "video",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("sequential", "parallel", "hybrid")]
    [string]$WorkflowMode = "hybrid",
    
    [Parameter(Mandatory=$false)]
    [string]$InputData = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Triggering Cloud Agent via GitHub API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get GitHub token
$token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if (-not $token) {
    Write-Host "[ERROR] GITHUB_TOKEN not found!" -ForegroundColor Red
    Write-Host "Run: .\setup-github-runtime.ps1" -ForegroundColor Yellow
    exit 1
}

$repo = "halvo78/ai-program-video-music-overlay"
$workflowFile = "cloud-agents.yml"
$url = "https://api.github.com/repos/$repo/actions/workflows/$workflowFile/dispatches"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "   Agent Type: $AgentType" -ForegroundColor Gray
Write-Host "   Workflow Mode: $WorkflowMode" -ForegroundColor Gray
Write-Host "   Repository: $repo" -ForegroundColor Gray
Write-Host ""

# Prepare inputs
$inputs = @{
    agent_type = $AgentType
    workflow_mode = $WorkflowMode
    platform = "github-actions"
}

if ($InputData) {
    $inputs["input_data"] = $InputData
}

$body = @{
    ref = "main"
    inputs = $inputs
} | ConvertTo-Json

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

Write-Host "Triggering workflow..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ErrorAction Stop
    Write-Host "[OK] Workflow triggered successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Get workflow run
    Start-Sleep -Seconds 2
    $runsUrl = "https://api.github.com/repos/$repo/actions/workflows/$workflowFile/runs?per_page=1"
    $runs = Invoke-RestMethod -Uri $runsUrl -Headers $headers -Method Get
    $run = $runs.workflow_runs[0]
    
    Write-Host "Workflow Run Details:" -ForegroundColor Yellow
    Write-Host "   Run ID: $($run.id)" -ForegroundColor Gray
    Write-Host "   Status: $($run.status)" -ForegroundColor Gray
    Write-Host "   URL: $($run.html_url)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "View run: $($run.html_url)" -ForegroundColor Cyan
    
} catch {
    Write-Host "[ERROR] Failed to trigger workflow: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cloud Agent Triggered Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
