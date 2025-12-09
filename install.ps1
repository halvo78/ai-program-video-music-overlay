# Installation Script - AI Program Video and Music Overlay
# Installs all dependencies for the unified platform

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Program Video and Music Overlay" -ForegroundColor Cyan
Write-Host "Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Python not found! Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Node.js
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check FFmpeg
$ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] FFmpeg found" -ForegroundColor Green
} else {
    Write-Host "[WARNING] FFmpeg not found. Video processing may not work." -ForegroundColor Yellow
    Write-Host "   Install from: https://ffmpeg.org/download.html" -ForegroundColor Gray
}

Write-Host ""

# Create virtual environment
Write-Host "Setting up Python environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install Python dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[WARNING] requirements.txt not found" -ForegroundColor Yellow
}

Write-Host ""

# Install Node.js dependencies
Write-Host "Setting up Node.js environment..." -ForegroundColor Yellow
if (Test-Path "dashboard\package.json") {
    Set-Location dashboard
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Node.js dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install Node.js dependencies" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
    Set-Location ..
} else {
    Write-Host "[WARNING] dashboard/package.json not found" -ForegroundColor Yellow
}

Write-Host ""

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @(
    "output",
    "generated",
    "temp",
    "logs",
    "assets\videos",
    "assets\music",
    "assets\images"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   Created: $dir" -ForegroundColor Gray
    }
}
Write-Host "[OK] Directories created" -ForegroundColor Green

Write-Host ""

# Check for .env file
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "[INFO] .env file not found. Creating template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
    if (-not (Test-Path ".env")) {
        Write-Host "[INFO] Create .env file manually with your API keys" -ForegroundColor Gray
    }
} else {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure .env file with your API keys" -ForegroundColor Gray
Write-Host "2. Run: .\start.ps1 to start the application" -ForegroundColor Gray
Write-Host "3. Or run: .\secrets.ps1 to manage secrets" -ForegroundColor Gray
Write-Host ""
