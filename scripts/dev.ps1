param(
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$SkipInstall,
    [switch]$SkipMigrate
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$projectDir = Join-Path $repoRoot "mysite"
$venvDir = Join-Path $projectDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$envFile = Join-Path $repoRoot ".env"
$envExampleFile = Join-Path $repoRoot ".env.example"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtualenv in $venvDir"
    python -m venv $venvDir
}

if (-not (Test-Path $envFile) -and (Test-Path $envExampleFile)) {
    Write-Host "Creating .env from .env.example"
    Copy-Item $envExampleFile $envFile
}

if (-not $SkipInstall) {
    Write-Host "Installing development dependencies"
    & $venvPython -m pip install -r (Join-Path $projectDir "requirements\dev.txt")
}

$env:DJANGO_ENV = "local"
if (-not $env:DEBUG) {
    $env:DEBUG = "True"
}
$env:PYTHONUNBUFFERED = "1"

Push-Location $projectDir
try {
    if (-not $SkipMigrate) {
        Write-Host "Running migrations"
        & $venvPython manage.py migrate --noinput
    }

    Write-Host "Starting development server on http://$BindHost`:$Port/"
    & $venvPython manage.py runserver "$BindHost`:$Port"
}
finally {
    Pop-Location
}
