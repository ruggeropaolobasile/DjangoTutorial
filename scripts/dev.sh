#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
SKIP_INSTALL="${SKIP_INSTALL:-0}"
SKIP_MIGRATE="${SKIP_MIGRATE:-0}"
RESEED="${RESEED:-0}"
SEED_PROFILE="${SEED_PROFILE:-mvp}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="${REPO_ROOT}/mysite"
VENV_DIR="${PROJECT_DIR}/.venv"
VENV_PYTHON="${VENV_DIR}/Scripts/python.exe"
PREFLIGHT_SCRIPT="${SCRIPT_DIR}/workspace-preflight.sh"

if [[ -f "${PREFLIGHT_SCRIPT}" ]]; then
  echo "Workspace identity preflight"
  bash "${PREFLIGHT_SCRIPT}" --workspace-path "${REPO_ROOT}"
  echo
fi

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Creating virtualenv in ${VENV_DIR}"
  python -m venv "${VENV_DIR}"
fi

if [[ ! -f "${REPO_ROOT}/.env" && -f "${REPO_ROOT}/.env.example" ]]; then
  echo "Creating .env from .env.example"
  cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
fi

if [[ "${SKIP_INSTALL}" != "1" ]]; then
  echo "Installing development dependencies"
  "${VENV_PYTHON}" -m pip install -r "${PROJECT_DIR}/requirements/dev.txt"
fi

export DJANGO_ENV=local
export DEBUG="${DEBUG:-True}"
export PYTHONUNBUFFERED=1

cd "${PROJECT_DIR}"

if [[ "${SKIP_MIGRATE}" != "1" ]]; then
  echo "Running migrations"
  "${VENV_PYTHON}" manage.py migrate --noinput
fi

if [[ "${RESEED}" == "1" ]]; then
  echo "Reseeding demo data (profile: ${SEED_PROFILE})"
  "${VENV_PYTHON}" manage.py reseed_demo_data --profile "${SEED_PROFILE}"
fi

echo "Starting development server on http://${HOST}:${PORT}/"
"${VENV_PYTHON}" manage.py runserver "${HOST}:${PORT}"
