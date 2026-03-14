#!/usr/bin/env bash
set -euo pipefail

workspace_path="."
role="${CODEX_REPO_ROLE:-}"
as_json=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace-path)
      workspace_path="$2"
      shift 2
      ;;
    --role)
      role="$2"
      shift 2
      ;;
    --json)
      as_json=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

workspace_path="$(cd "$workspace_path" && pwd)"
session_cwd="$(pwd)"
repo_root="$(git -c safe.directory="$workspace_path" -C "$workspace_path" rev-parse --show-toplevel)"
repo_name="$(basename "$repo_root")"
branch="$(git -c safe.directory="$repo_root" -C "$repo_root" branch --show-current)"
status_short="$(git -c safe.directory="$repo_root" -C "$repo_root" status --short)"

if [[ -z "$branch" ]]; then
  branch="(detached HEAD)"
fi

if [[ -z "$role" && -f "$repo_root/.codex-role" ]]; then
  role="$(head -n 1 "$repo_root/.codex-role" | tr -d '\r')"
fi
if [[ -z "$role" ]]; then
  role="$repo_name"
fi

if [[ -z "$status_short" ]]; then
  clean_worktree=true
  status_summary="clean"
else
  clean_worktree=false
  status_summary="dirty"
fi

if [[ "$as_json" -eq 1 ]]; then
  printf '{\n'
  printf '  "workspace_path": "%s",\n' "$workspace_path"
  printf '  "session_cwd": "%s",\n' "$session_cwd"
  printf '  "repo_root": "%s",\n' "$repo_root"
  printf '  "repo_name": "%s",\n' "$repo_name"
  printf '  "branch": "%s",\n' "$branch"
  printf '  "role": "%s",\n' "$role"
  printf '  "clean_worktree": %s,\n' "$clean_worktree"
  printf '  "status_summary": "%s"\n' "$status_summary"
  printf '}\n'
  exit 0
fi

echo "=== Codex Workspace Preflight ==="
echo "workspace_path : $workspace_path"
echo "session_cwd    : $session_cwd"
echo "repo_root      : $repo_root"
echo "repo_name      : $repo_name"
echo "branch         : $branch"
echo "role           : $role"
echo "worktree       : $status_summary"

if [[ "$workspace_path" != "$repo_root" ]]; then
  echo "note           : the selected workspace path is inside the repo, not the repo root."
fi
if [[ "$session_cwd" != "$workspace_path" ]]; then
  echo "note           : the current shell is running from a different folder than workspace_path."
fi

if [[ -n "$status_short" ]]; then
  echo
  echo "Pending changes:"
  printf '%s\n' "$status_short"
fi
