# Branch and Clone Strategy

Obiettivo: evitare conflitti tra task paralleli e sessioni agente.

## Regole

1. Un branch per tema:
   - `feature/...`
   - `fix/...`
   - `chore/...`
2. Un clone per stream di lavoro parallelo.
3. Una sessione agente per clone.
4. Prima di cambiare branch: working tree pulito.

## Setup consigliato

- `C:\repo\DjangoTutorial` -> onboarding/processo
- `C:\repo\DjangoTutorial-ui` -> task UI

## Switch sicuro

PowerShell:

```powershell
.\scripts\safe-switch-branch.ps1 -Branch fix/example -CreateFromMain
```

Git Bash:

```bash
bash scripts/safe-switch-branch.sh fix/example --create-from-main
```

