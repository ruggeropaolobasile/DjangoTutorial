param(
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 8000,
    [ValidateSet("core", "mvp", "full")]
    [string]$SeedProfile = "mvp",
    [string]$Username = "demo-user",
    [string]$Password = "safe-password-123"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$projectDir = Join-Path $repoRoot "mysite"
$venvPython = Join-Path $projectDir ".venv\\Scripts\\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Virtualenv Python not found at $venvPython. Run .\\scripts\\dev.ps1 first."
    exit 1
}

$env:DJANGO_ENV = "local"
if (-not $env:DEBUG) {
    $env:DEBUG = "True"
}

Push-Location $projectDir
try {
    & $venvPython manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & $venvPython manage.py reseed_demo_data --profile $SeedProfile
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & $venvPython manage.py ensure_smoke_user --username $Username --password $Password
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Playwright smoke setup ready." -ForegroundColor Green
Write-Host "Base URL : http://$BindHost`:$Port/"
Write-Host "Login URL: http://$BindHost`:$Port/accounts/login/"
Write-Host "Username : $Username"
Write-Host "Password : $Password"
