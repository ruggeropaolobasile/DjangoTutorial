# Preflight and Safe Switch

Obiettivo: ridurre errori operativi prima di commit/switch branch.

## Preflight

PowerShell:

```powershell
.\scripts\preflight.ps1
.\scripts\preflight.ps1 -SkipTests
.\scripts\preflight.ps1 -DeployChecks
```

Git Bash:

```bash
bash scripts/preflight.sh
SKIP_TESTS=1 bash scripts/preflight.sh
DEPLOY_CHECKS=1 bash scripts/preflight.sh
```

## Safe branch switch

PowerShell:

```powershell
.\scripts\safe-switch-branch.ps1 -Branch chore/example -CreateFromMain
```

Git Bash:

```bash
bash scripts/safe-switch-branch.sh chore/example --create-from-main
```
