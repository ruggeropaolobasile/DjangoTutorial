#!/usr/bin/env bash
set -euo pipefail

SKIP_TESTS="${SKIP_TESTS:-0}"
SKIP_LINT="${SKIP_LINT:-0}"
DEPLOY_CHECKS="${DEPLOY_CHECKS:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="${REPO_ROOT}/mysite"
VENV_PYTHON="${PROJECT_DIR}/.venv/Scripts/python.exe"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Virtualenv Python not found at ${VENV_PYTHON}. Run scripts/dev.sh first."
  exit 1
fi

cd "${PROJECT_DIR}"

"${VENV_PYTHON}" manage.py check

if [[ "${SKIP_TESTS}" != "1" ]]; then
  "${VENV_PYTHON}" manage.py test
fi

if [[ "${SKIP_LINT}" != "1" ]]; then
  "${VENV_PYTHON}" -m ruff check .
fi

if [[ "${DEPLOY_CHECKS}" == "1" ]]; then
  DJANGO_ENV=production \
  DEBUG=False \
  SECRET_KEY=prod-check-secret-key-please-change-in-real-env-0123456789 \
  PUBLIC_DOMAIN=example.com \
  "${VENV_PYTHON}" manage.py check --deploy
fi

echo "Preflight checks completed."
