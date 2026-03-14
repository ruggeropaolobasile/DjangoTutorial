param(
    [string]$WorkspacePath = ".",
    [string]$Role,
    [switch]$AsJson
)

$ErrorActionPreference = "Stop"

function Get-CommandOutput {
    param(
        [string[]]$Command
    )

    $output = & $Command[0] $Command[1..($Command.Length - 1)] 2>$null
    if ($LASTEXITCODE -ne 0) {
        return $null
    }
    return ($output | Out-String).Trim()
}

function Get-GitOutput {
    param(
        [string]$GitPath,
        [string[]]$Arguments
    )

    $command = @("git", "-c", "safe.directory=$GitPath", "-C", $GitPath) + $Arguments
    return Get-CommandOutput -Command $command
}

$resolvedWorkspace = Resolve-Path $WorkspacePath
$workspaceFullPath = $resolvedWorkspace.Path
$sessionCwd = (Get-Location).Path

$repoRoot = Get-CommandOutput @("git", "-c", "safe.directory=$workspaceFullPath", "-C", $workspaceFullPath, "rev-parse", "--show-toplevel")
if (-not $repoRoot) {
    throw "No Git repository found from '$workspaceFullPath'."
}

$repoRoot = (Resolve-Path $repoRoot).Path
$repoName = Split-Path -Leaf $repoRoot
$branch = Get-GitOutput -GitPath $repoRoot -Arguments @("branch", "--show-current")
if (-not $branch) {
    $branch = "(detached HEAD)"
}

$statusShort = Get-GitOutput -GitPath $repoRoot -Arguments @("status", "--short")
$roleFile = Join-Path $repoRoot ".codex-role"

if (-not $Role -and $env:CODEX_REPO_ROLE) {
    $Role = $env:CODEX_REPO_ROLE.Trim()
}
if (-not $Role -and (Test-Path $roleFile)) {
    $Role = (Get-Content $roleFile -TotalCount 1).Trim()
}
if (-not $Role) {
    $Role = $repoName
}

$identity = [ordered]@{
    workspace_path = $workspaceFullPath
    session_cwd = $sessionCwd
    repo_root = $repoRoot
    repo_name = $repoName
    branch = $branch
    role = $Role
    clean_worktree = [string]::IsNullOrWhiteSpace($statusShort)
    status_summary = if ([string]::IsNullOrWhiteSpace($statusShort)) { "clean" } else { "dirty" }
}

if ($AsJson) {
    $identity | ConvertTo-Json -Depth 2
    exit 0
}

Write-Host "=== Codex Workspace Preflight ==="
Write-Host ("workspace_path : {0}" -f $identity.workspace_path)
Write-Host ("session_cwd    : {0}" -f $identity.session_cwd)
Write-Host ("repo_root      : {0}" -f $identity.repo_root)
Write-Host ("repo_name      : {0}" -f $identity.repo_name)
Write-Host ("branch         : {0}" -f $identity.branch)
Write-Host ("role           : {0}" -f $identity.role)
Write-Host ("worktree       : {0}" -f $identity.status_summary)

if ($identity.workspace_path -ne $identity.repo_root) {
    Write-Host "note           : the selected workspace path is inside the repo, not the repo root."
}
if ($identity.session_cwd -ne $identity.workspace_path) {
    Write-Host "note           : the current shell is running from a different folder than workspace_path."
}

if (-not [string]::IsNullOrWhiteSpace($statusShort)) {
    Write-Host ""
    Write-Host "Pending changes:"
    Write-Host $statusShort
}
