# GitHub Runtime Configuration Setup Script
# This script helps set up GitHub runtime access for cloud agents

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Runtime Configuration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GITHUB_TOKEN is already set
$existingToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")

if ($existingToken) {
    Write-Host "[OK] GITHUB_TOKEN is already set" -ForegroundColor Green
    Write-Host "Current token: $($existingToken.Substring(0, [Math]::Min(10, $existingToken.Length)))..." -ForegroundColor Gray
    $update = Read-Host "Update token? (y/n)"
    if ($update -ne "y") {
        Write-Host "Keeping existing token." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "To set up GitHub runtime access:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create GitHub Personal Access Token:" -ForegroundColor White
Write-Host "   https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Required Scopes:" -ForegroundColor White
Write-Host "   - repo (Full control)" -ForegroundColor Gray
Write-Host "   - workflow (Update workflows)" -ForegroundColor Gray
Write-Host "   - actions:read (Read Actions)" -ForegroundColor Gray
Write-Host "   - actions:write (Write Actions)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Enter your token below:" -ForegroundColor White
Write-Host ""

$token = Read-Host "GitHub Token" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)

if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
    Write-Host "[ERROR] Token cannot be empty" -ForegroundColor Red
    exit 1
}

# Set environment variable
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $tokenPlain, "User")

Write-Host ""
Write-Host "[OK] GITHUB_TOKEN set successfully!" -ForegroundColor Green
Write-Host ""

# Test token
Write-Host "Testing GitHub API access..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "token $tokenPlain"
        "Accept" = "application/vnd.github.v3+json"
    }
    $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get
    Write-Host "[OK] GitHub API access verified!" -ForegroundColor Green
    Write-Host "   User: $($response.login)" -ForegroundColor Gray
    Write-Host "   Name: $($response.name)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Failed to verify token: $_" -ForegroundColor Red
    Write-Host "Please check your token and try again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Add token to GitHub Secrets:" -ForegroundColor White
Write-Host "   https://github.com/halvo78/ai-program-video-music-overlay/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Create .env file (optional):" -ForegroundColor White
Write-Host "   GITHUB_TOKEN=$tokenPlain" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Reload Cursor to pick up environment variable" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
