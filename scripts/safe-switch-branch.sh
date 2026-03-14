#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/safe-switch-branch.sh <branch> [--create-from-main]"
  exit 1
fi

BRANCH="$1"
CREATE_FROM_MAIN="${2:-}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Current directory is not a git repository."
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit or stash changes before switching branch:"
  git status --short
  exit 1
fi

if [[ "$CREATE_FROM_MAIN" == "--create-from-main" ]]; then
  git checkout main
  git pull --ff-only
  git checkout -b "$BRANCH"
  echo "Created and switched to '$BRANCH' from up-to-date main."
  exit 0
fi

git checkout "$BRANCH"
echo "Switched to '$BRANCH' with a clean working tree."
