#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Current directory is not a git repository."
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
BRANCH="$(git branch --show-current)"
HEAD_SHORT="$(git rev-parse --short HEAD)"
STATUS="$(git status --short)"
WORKTREES="$(git worktree list)"

echo "Session context"
echo "  repo root : ${REPO_ROOT}"
echo "  branch    : ${BRANCH}"
echo "  head      : ${HEAD_SHORT}"
echo "  cwd       : $(pwd)"
echo
echo "Working tree status"
if [[ -n "${STATUS}" ]]; then
  while IFS= read -r line; do
    echo "  ${line}"
  done <<< "${STATUS}"
else
  echo "  clean"
fi

echo
echo "Known worktrees"
while IFS= read -r line; do
  echo "  ${line}"
done <<< "${WORKTREES}"
