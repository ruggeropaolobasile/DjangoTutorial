param()

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Error $Message
    exit 1
}

git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    Fail "Current directory is not a git repository."
}

$repoRoot = (git rev-parse --show-toplevel).Trim()
$branch = (git branch --show-current).Trim()
$head = (git rev-parse --short HEAD).Trim()
$status = git status --short
$worktrees = git worktree list

Write-Host "Session context"
Write-Host "  repo root : $repoRoot"
Write-Host "  branch    : $branch"
Write-Host "  head      : $head"
Write-Host "  cwd       : $((Get-Location).Path)"
Write-Host ""
Write-Host "Working tree status"
if ($status) {
    $status | ForEach-Object { Write-Host "  $_" }
}
else {
    Write-Host "  clean"
}

Write-Host ""
Write-Host "Known worktrees"
$worktrees | ForEach-Object { Write-Host "  $_" }
