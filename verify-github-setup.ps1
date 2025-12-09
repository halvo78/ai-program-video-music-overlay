# Verify GitHub Runtime Setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Runtime Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check environment variable
$token = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if ($token) {
    Write-Host "[OK] GITHUB_TOKEN environment variable is set" -ForegroundColor Green
    Write-Host "   Token: $($token.Substring(0, [Math]::Min(10, $token.Length)))..." -ForegroundColor Gray
} else {
    Write-Host "[!] GITHUB_TOKEN not set in environment" -ForegroundColor Yellow
    Write-Host "   Run: .\setup-github-runtime.ps1" -ForegroundColor Gray
}

# Check git remote
Write-Host ""
Write-Host "Git Remote Configuration:" -ForegroundColor Yellow
git remote -v

# Check git config
Write-Host ""
Write-Host "Git Configuration:" -ForegroundColor Yellow
$gitUser = git config user.name
$gitEmail = git config user.email
Write-Host "   User: $gitUser" -ForegroundColor Gray
Write-Host "   Email: $gitEmail" -ForegroundColor Gray

# Test GitHub API (if token available)
if ($token) {
    Write-Host ""
    Write-Host "Testing GitHub API Access..." -ForegroundColor Yellow
    try {
        $headers = @{
            "Authorization" = "token $token"
            "Accept" = "application/vnd.github.v3+json"
        }
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get -ErrorAction Stop
        Write-Host "[OK] GitHub API access verified!" -ForegroundColor Green
        Write-Host "   User: $($response.login)" -ForegroundColor Gray
        Write-Host "   Name: $($response.name)" -ForegroundColor Gray
        Write-Host "   Type: $($response.type)" -ForegroundColor Gray
    } catch {
        Write-Host "[ERROR] GitHub API test failed: $_" -ForegroundColor Red
    }
    
    # Test repository access
    Write-Host ""
    Write-Host "Testing Repository Access..." -ForegroundColor Yellow
    try {
        $repoUrl = "https://api.github.com/repos/halvo78/ai-program-video-music-overlay"
        $repoResponse = Invoke-RestMethod -Uri $repoUrl -Headers $headers -Method Get -ErrorAction Stop
        Write-Host "[OK] Repository access verified!" -ForegroundColor Green
        Write-Host "   Repository: $($repoResponse.full_name)" -ForegroundColor Gray
        Write-Host "   Private: $($repoResponse.private)" -ForegroundColor Gray
        Write-Host "   Default Branch: $($repoResponse.default_branch)" -ForegroundColor Gray
    } catch {
        Write-Host "[ERROR] Repository access failed: $_" -ForegroundColor Red
    }
    
    # Test Actions API
    Write-Host ""
    Write-Host "Testing GitHub Actions API..." -ForegroundColor Yellow
    try {
        $workflowsUrl = "https://api.github.com/repos/halvo78/ai-program-video-music-overlay/actions/workflows"
        $workflowsResponse = Invoke-RestMethod -Uri $workflowsUrl -Headers $headers -Method Get -ErrorAction Stop
        Write-Host "[OK] GitHub Actions API access verified!" -ForegroundColor Green
        Write-Host "   Workflows: $($workflowsResponse.total_count)" -ForegroundColor Gray
    } catch {
        Write-Host "[WARNING] GitHub Actions API test failed: $_" -ForegroundColor Yellow
        Write-Host "   This may require 'actions:read' scope" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "[!] Cannot test API without GITHUB_TOKEN" -ForegroundColor Yellow
}

# Check configuration files
Write-Host ""
Write-Host "Configuration Files:" -ForegroundColor Yellow
$configFiles = @(
    ".cursor/github-runtime-config.json",
    ".cursor/git-config.json",
    ".cursor/github-auth-config.json",
    ".github/runtime-config.md"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "   [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "   [!] $file - Missing" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
