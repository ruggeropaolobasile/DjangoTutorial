param(
    [Parameter(Mandatory = $true)]
    [string]$Branch,
    [switch]$CreateFromMain
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Error $Message
    exit 1
}

git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    Fail "Current directory is not a git repository."
}

$status = git status --porcelain
if ($status) {
    Write-Host "Working tree is not clean. Commit or stash changes before switching branch:" -ForegroundColor Yellow
    git status --short
    exit 1
}

if ($CreateFromMain) {
    git checkout main
    if ($LASTEXITCODE -ne 0) { Fail "Unable to checkout main." }

    git pull --ff-only
    if ($LASTEXITCODE -ne 0) { Fail "Unable to pull main with --ff-only." }

    git checkout -b $Branch
    if ($LASTEXITCODE -ne 0) { Fail "Unable to create branch '$Branch' from main." }

    Write-Host "Created and switched to '$Branch' from up-to-date main." -ForegroundColor Green
    exit 0
}

git checkout $Branch
if ($LASTEXITCODE -ne 0) {
    Fail "Unable to checkout branch '$Branch'."
}

Write-Host "Switched to '$Branch' with a clean working tree." -ForegroundColor Green
