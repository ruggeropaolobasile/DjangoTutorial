## Summary
- 

## Agent Context
- AGENTS scope used:
  - [ ] Root `AGENTS.md`
  - [ ] `mysite/polls/AGENTS.md`
  - [ ] `mysite/mysite/settings/AGENTS.md`
- Notes:

## Technical Checklist
- [ ] Local tests pass (`python manage.py test`)
- [ ] Django checks pass (`python manage.py check`)
- [ ] Lint passes (`ruff check mysite`)
- [ ] If settings/deploy changed, `python manage.py check --deploy` reviewed
- [ ] If `polls` changed, `python manage.py test polls` reviewed
- [ ] If models changed, migration impact reviewed (`makemigrations --check` or migration rationale)

## Risk & Rollback
- Risk level: low / medium / high
- Rollback plan:

## Verification
- [ ] Verified key endpoints locally (`/`, `/polls/`, `/healthz/`)
- [ ] Migration impact reviewed (if applicable)
