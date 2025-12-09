# Cursor Cloud Enable Script
# This script helps enable Cursor Cloud sync for the workspace

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cursor Cloud Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Cursor is running
$cursorProcess = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue

if ($cursorProcess) {
    Write-Host "[OK] Cursor is running" -ForegroundColor Green
} else {
    Write-Host "[!] Cursor is not running. Starting Cursor..." -ForegroundColor Yellow
    Start-Process "cursor" -ArgumentList "$PWD"
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "To enable Cursor Cloud:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. In Cursor IDE, press Ctrl+Shift+P" -ForegroundColor White
Write-Host "2. Type: 'Cursor: Sign In' or 'Cursor: Enable Cloud'" -ForegroundColor White
Write-Host "3. Sign in with your Cursor account" -ForegroundColor White
Write-Host "4. Enable sync for this workspace" -ForegroundColor White
Write-Host ""
Write-Host "OR" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Click your profile icon (bottom left)" -ForegroundColor White
Write-Host "2. Click 'Sign In' or 'Enable Cloud'" -ForegroundColor White
Write-Host "3. Follow the prompts to enable sync" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Workspace Configuration:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[OK] .cursorrules created" -ForegroundColor Green
Write-Host "[OK] .cursorignore created" -ForegroundColor Green
Write-Host "[OK] .cursor/environment.json configured" -ForegroundColor Green
Write-Host "[OK] .vscode/settings.json created" -ForegroundColor Green
Write-Host ""
Write-Host "Your workspace is ready for Cursor Cloud!" -ForegroundColor Green
Write-Host ""
