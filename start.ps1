# Start Script - AI Program Video and Music Overlay
# Starts both FastAPI backend and Next.js frontend

param(
    [Parameter(Mandatory=$false)]
    [switch]$BackendOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$FrontendOnly,
    
    [Parameter(Mandatory=$false)]
    [int]$BackendPort = 8000,
    
    [Parameter(Mandatory=$false)]
    [int]$FrontendPort = 3000
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AI Program Video and Music Overlay" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: .\install.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

# Function to start backend
function Start-Backend {
    Write-Host ""
    Write-Host "Starting FastAPI Backend..." -ForegroundColor Yellow
    Write-Host "   Port: $BackendPort" -ForegroundColor Gray
    Write-Host "   URL: http://localhost:$BackendPort" -ForegroundColor Cyan
    Write-Host "   API Docs: http://localhost:$BackendPort/docs" -ForegroundColor Cyan
    Write-Host ""
    
    $backendJob = Start-Job -ScriptBlock {
        param($port)
        Set-Location $using:PWD
        & "venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port $port --reload
    } -ArgumentList $BackendPort
    
    return $backendJob
}

# Function to start frontend
function Start-Frontend {
    Write-Host ""
    Write-Host "Starting Next.js Frontend..." -ForegroundColor Yellow
    Write-Host "   Port: $FrontendPort" -ForegroundColor Gray
    Write-Host "   URL: http://localhost:$FrontendPort" -ForegroundColor Cyan
    Write-Host ""
    
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location "$using:PWD\dashboard"
        npm run dev
    }
    
    return $frontendJob
}

# Start services
$jobs = @()

if (-not $FrontendOnly) {
    $backendJob = Start-Backend
    $jobs += $backendJob
    Start-Sleep -Seconds 3
}

if (-not $BackendOnly) {
    if (Test-Path "dashboard\package.json") {
        $frontendJob = Start-Frontend
        $jobs += $frontendJob
    } else {
        Write-Host "[WARNING] Dashboard not found, skipping frontend" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend: http://localhost:$BackendPort" -ForegroundColor Cyan
if (-not $BackendOnly) {
    Write-Host "Frontend: http://localhost:$FrontendPort" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host ""

# Monitor jobs
try {
    while ($true) {
        $running = $jobs | Where-Object { $_.State -eq "Running" }
        if ($running.Count -eq 0) {
            Write-Host "[WARNING] All services stopped" -ForegroundColor Yellow
            break
        }
        Start-Sleep -Seconds 5
    }
} finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    $jobs | Stop-Job
    $jobs | Remove-Job
    Write-Host "[OK] All services stopped" -ForegroundColor Green
}
