param(
    [switch]$SkipTests,
    [switch]$SkipLint,
    [switch]$DeployChecks
)

$ErrorActionPreference = "Stop"

function Invoke-NativeCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Description,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    Write-Host "Running: $Description"
    & $Command
    if ($LASTEXITCODE -ne 0) {
        Write-Error "'$Description' failed with exit code $LASTEXITCODE."
        exit $LASTEXITCODE
    }
}

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
    Invoke-NativeCommand -Description "python manage.py check" -Command {
        & $venvPython manage.py check
    }

    if (-not $SkipTests) {
        Invoke-NativeCommand -Description "python manage.py test" -Command {
            & $venvPython manage.py test
        }
    }

    if (-not $SkipLint) {
        Invoke-NativeCommand -Description "python -m ruff check ." -Command {
            & $venvPython -m ruff check .
        }
    }

    if ($DeployChecks) {
        $names = @("DJANGO_ENV", "DEBUG", "SECRET_KEY", "PUBLIC_DOMAIN")
        $originals = @{}
        foreach ($name in $names) {
            $originals[$name] = [Environment]::GetEnvironmentVariable($name, "Process")
        }

        try {
            [Environment]::SetEnvironmentVariable("DJANGO_ENV", "production", "Process")
            [Environment]::SetEnvironmentVariable("DEBUG", "False", "Process")
            [Environment]::SetEnvironmentVariable("SECRET_KEY", "prod-check-secret-key-please-change-in-real-env-0123456789", "Process")
            [Environment]::SetEnvironmentVariable("PUBLIC_DOMAIN", "example.com", "Process")

            Invoke-NativeCommand -Description "python manage.py check --deploy" -Command {
                & $venvPython manage.py check --deploy
            }
        }
        finally {
            foreach ($name in $names) {
                [Environment]::SetEnvironmentVariable($name, $originals[$name], "Process")
            }
        }
    }
}
finally {
    Pop-Location
}

Write-Host "Preflight checks completed." -ForegroundColor Green
