# PR and CI Process

Obiettivo: PR ripetibili, verificabili e con rischio controllato.

## Prima della PR

1. Esegui check locali (`preflight` consigliato).
2. Compila `PULL_REQUEST_TEMPLATE.md` in modo completo.
3. Esplicita rischi, rollback e verifiche endpoint.

## CI

Workflow: `.github/workflows/ci.yml`

- `test-and-lint`
  - `python manage.py check`
  - `python manage.py test`
  - `ruff check mysite`
- `deploy-check`
  - `python manage.py check --deploy`

Trigger push coperti: `main`, `feature/**`, `fix/**`, `chore/**`
