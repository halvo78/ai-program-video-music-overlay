# Secrets Management Script
# Manage environment variables and API keys

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("list", "set", "get", "remove", "verify", "template")]
    [string]$Action = "list",
    
    [Parameter(Mandatory=$false)]
    [string]$Key = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Value = ""
)

$envFile = ".env"
$envExample = ".env.example"

function Show-Header {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Secrets Management" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-List {
    Show-Header
    
    if (Test-Path $envFile) {
        Write-Host "Current environment variables:" -ForegroundColor Yellow
        Write-Host ""
        $content = Get-Content $envFile
        foreach ($line in $content) {
            if ($line -match "^([^#][^=]+)=(.*)$") {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                if ($value.Length -gt 0) {
                    $displayValue = if ($value.Length -gt 20) { $value.Substring(0, 20) + "..." } else { $value }
                    Write-Host "  $key = $displayValue" -ForegroundColor Gray
                } else {
                    Write-Host "  $key = (not set)" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "[INFO] .env file not found" -ForegroundColor Yellow
        Write-Host "Run: .\secrets.ps1 -Action template" -ForegroundColor Gray
    }
}

function Set-Secret {
    param([string]$Key, [string]$Value)
    
    Show-Header
    
    if ([string]::IsNullOrWhiteSpace($Key)) {
        Write-Host "[ERROR] Key is required" -ForegroundColor Red
        return
    }
    
    if ([string]::IsNullOrWhiteSpace($Value)) {
        $Value = Read-Host "Enter value for $Key" -AsSecureString
        $Value = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
        )
    }
    
    # Read existing .env or create new
    $envContent = @()
    if (Test-Path $envFile) {
        $envContent = Get-Content $envFile
        $found = $false
        for ($i = 0; $i -lt $envContent.Length; $i++) {
            if ($envContent[$i] -match "^$Key\s*=") {
                $envContent[$i] = "$Key=$Value"
                $found = $true
                break
            }
        }
        if (-not $found) {
            $envContent += "$Key=$Value"
        }
    } else {
        $envContent = @("$Key=$Value")
    }
    
    $envContent | Set-Content $envFile
    Write-Host "[OK] Set $Key" -ForegroundColor Green
}

function Get-Secret {
    param([string]$Key)
    
    Show-Header
    
    if ([string]::IsNullOrWhiteSpace($Key)) {
        Write-Host "[ERROR] Key is required" -ForegroundColor Red
        return
    }
    
    if (Test-Path $envFile) {
        $content = Get-Content $envFile
        foreach ($line in $content) {
            if ($line -match "^$Key\s*=(.*)$") {
                $value = $matches[1].Trim()
                Write-Host "$Key = $value" -ForegroundColor Green
                return
            }
        }
    }
    
    Write-Host "[INFO] $Key not found" -ForegroundColor Yellow
}

function Remove-Secret {
    param([string]$Key)
    
    Show-Header
    
    if ([string]::IsNullOrWhiteSpace($Key)) {
        Write-Host "[ERROR] Key is required" -ForegroundColor Red
        return
    }
    
    if (Test-Path $envFile) {
        $content = Get-Content $envFile
        $newContent = $content | Where-Object { $_ -notmatch "^$Key\s*=" }
        $newContent | Set-Content $envFile
        Write-Host "[OK] Removed $Key" -ForegroundColor Green
    } else {
        Write-Host "[INFO] .env file not found" -ForegroundColor Yellow
    }
}

function Verify-Secrets {
    Show-Header
    
    Write-Host "Verifying required secrets..." -ForegroundColor Yellow
    Write-Host ""
    
    $required = @(
        "GITHUB_TOKEN",
        "TOGETHER_AI_API_KEY",
        "HUGGINGFACE_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
    )
    
    $optional = @(
        "FLUX_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "STRIPE_SECRET_KEY",
        "SUPABASE_URL",
        "SUPABASE_KEY"
    )
    
    $allSet = $true
    
    Write-Host "Required:" -ForegroundColor Yellow
    foreach ($key in $required) {
        $value = [System.Environment]::GetEnvironmentVariable($key, "User")
        if ([string]::IsNullOrWhiteSpace($value)) {
            # Try .env file
            if (Test-Path $envFile) {
                $content = Get-Content $envFile
                foreach ($line in $content) {
                    if ($line -match "^$key\s*=(.*)$") {
                        $value = $matches[1].Trim()
                        break
                    }
                }
            }
        }
        
        if ([string]::IsNullOrWhiteSpace($value)) {
            Write-Host "  [ ] $key - MISSING" -ForegroundColor Red
            $allSet = $false
        } else {
            Write-Host "  [OK] $key" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    Write-Host "Optional:" -ForegroundColor Yellow
    foreach ($key in $optional) {
        $value = [System.Environment]::GetEnvironmentVariable($key, "User")
        if ([string]::IsNullOrWhiteSpace($value) -and (Test-Path $envFile)) {
            $content = Get-Content $envFile
            foreach ($line in $content) {
                if ($line -match "^$key\s*=(.*)$") {
                    $value = $matches[1].Trim()
                    break
                }
            }
        }
        
        if ([string]::IsNullOrWhiteSpace($value)) {
            Write-Host "  [ ] $key - Not set" -ForegroundColor Gray
        } else {
            Write-Host "  [OK] $key" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    if ($allSet) {
        Write-Host "[OK] All required secrets are set!" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Some required secrets are missing" -ForegroundColor Yellow
        Write-Host "Run: .\secrets.ps1 -Action set -Key [KEY_NAME]" -ForegroundColor Gray
    }
}

function Create-Template {
    Show-Header
    
    $template = @"
# AI Program Video and Music Overlay - Environment Variables
# Copy this file to .env and fill in your API keys

# GitHub
GITHUB_TOKEN=your_github_token_here

# AI Providers
TOGETHER_AI_API_KEY=your_together_ai_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional AI Providers
FLUX_API_KEY=your_flux_key_here

# AWS (for cloud agents)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# Database
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# Payments
STRIPE_SECRET_KEY=your_stripe_secret_key_here

# Application
FASTAPI_PORT=8000
NEXTJS_PORT=3000
WORKFLOW_MODE=hybrid
GENERATED_DIR=generated
OUTPUT_DIR=output
"@
    
    $template | Set-Content $envExample
    Write-Host "[OK] Created .env.example template" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Copy .env.example to .env" -ForegroundColor Gray
    Write-Host "2. Fill in your API keys" -ForegroundColor Gray
    Write-Host "3. Run: .\secrets.ps1 -Action verify" -ForegroundColor Gray
}

# Main logic
switch ($Action) {
    "list" { Show-List }
    "set" { Set-Secret -Key $Key -Value $Value }
    "get" { Get-Secret -Key $Key }
    "remove" { Remove-Secret -Key $Key }
    "verify" { Verify-Secrets }
    "template" { Create-Template }
    default {
        Write-Host "Usage: .\secrets.ps1 -Action [list|set|get|remove|verify|template]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Yellow
        Write-Host "  .\secrets.ps1 -Action list" -ForegroundColor Gray
        Write-Host "  .\secrets.ps1 -Action set -Key GITHUB_TOKEN -Value 'token'" -ForegroundColor Gray
        Write-Host "  .\secrets.ps1 -Action get -Key GITHUB_TOKEN" -ForegroundColor Gray
        Write-Host "  .\secrets.ps1 -Action verify" -ForegroundColor Gray
        Write-Host "  .\secrets.ps1 -Action template" -ForegroundColor Gray
    }
}
