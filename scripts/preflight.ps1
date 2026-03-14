param(
    [switch]$SkipTests,
    [switch]$SkipLint,
    [switch]$DeployChecks
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$projectDir = Join-Path $repoRoot "mysite"
$venvPython = Join-Path $projectDir ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Virtualenv Python not found at $venvPython. Run .\scripts\dev.ps1 first."
    exit 1
}

Push-Location $projectDir
try {
    & $venvPython manage.py check

    if (-not $SkipTests) {
        & $venvPython manage.py test
    }

    if (-not $SkipLint) {
        & $venvPython -m ruff check .
    }

    if ($DeployChecks) {
        $env:DJANGO_ENV = "production"
        $env:DEBUG = "False"
        $env:SECRET_KEY = "prod-check-secret-key-please-change-in-real-env-0123456789"
        $env:PUBLIC_DOMAIN = "example.com"
        & $venvPython manage.py check --deploy
    }
}
finally {
    Pop-Location
}

Write-Host "Preflight checks completed." -ForegroundColor Green
