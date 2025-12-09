# Cloud Agents Quick Start Guide
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cloud Agents - Quick Start Guide" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. VERIFY SETUP" -ForegroundColor Yellow
Write-Host "   Run: .\verify-github-setup.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "2. RUN CLOUD AGENT" -ForegroundColor Yellow
Write-Host "   Basic:" -ForegroundColor Gray
Write-Host "   .\run-cloud-agent.ps1 -AgentType video" -ForegroundColor White
Write-Host ""
Write-Host "   With options:" -ForegroundColor Gray
Write-Host "   .\run-cloud-agent.ps1 -AgentType music -WorkflowMode parallel" -ForegroundColor White
Write-Host ""
Write-Host "   Available agents:" -ForegroundColor Gray
Write-Host "   video, music, image, voice, content, editing," -ForegroundColor Gray
Write-Host "   optimization, analytics, safety, social, all" -ForegroundColor Gray
Write-Host ""

Write-Host "3. LIST WORKFLOW RUNS" -ForegroundColor Yellow
Write-Host "   .\list-workflow-runs.ps1" -ForegroundColor White
Write-Host "   .\list-workflow-runs.ps1 -Limit 20" -ForegroundColor White
Write-Host ""

Write-Host "4. CHECK STATUS" -ForegroundColor Yellow
Write-Host "   .\get-workflow-status.ps1 -RunId [run_id]" -ForegroundColor White
Write-Host "   (Get run ID from list-workflow-runs.ps1)" -ForegroundColor Gray
Write-Host ""

Write-Host "5. MANUAL TRIGGER" -ForegroundColor Yellow
Write-Host "   GitHub -> Actions -> Cloud Agents -> Run workflow" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to Run Cloud Agents!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify setup first
Write-Host "Verifying setup..." -ForegroundColor Yellow
$token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if ($token) {
    Write-Host "[OK] GITHUB_TOKEN is set" -ForegroundColor Green
} else {
    Write-Host "[!] GITHUB_TOKEN not set - run setup-github-runtime.ps1" -ForegroundColor Yellow
}
