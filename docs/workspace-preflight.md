# Workspace preflight per clone multipli

Questa procedura evita un problema frequente: la finestra VS Code puo mostrare un clone, mentre la sessione Codex o il terminale stanno ancora lavorando su un'altra working copy.

## Tre contesti diversi da non confondere

- `Explorer / finestra VS Code`: cartella visibile nella UI.
- `terminale integrato`: cartella corrente del terminale aperto.
- `sessione agente Codex`: root reale agganciata alla chat corrente.

Questi tre contesti possono divergere. Prima di modificare file, cambiare branch o lanciare comandi Git, esegui sempre un preflight.

## Check rapido standard

PowerShell, da root repo:

```powershell
.\scripts\workspace-preflight.ps1
```

Git Bash:

```bash
bash scripts/workspace-preflight.sh
```

Il comando stampa sempre:

- `repo_root`
- `repo_name`
- `branch`
- `role`
- stato `clean/dirty`

Se `workspace_path`, `session_cwd` e `repo_root` non coincidono, fermati e riallinea il contesto prima di procedere.

## Come assegnare un role al clone

Per distinguere rapidamente clone con ruoli diversi, crea un file locale non tracciato `.codex-role` nella root del clone:

```text
ui
```

oppure:

```text
video
```

Alternative supportate:

- variabile ambiente `CODEX_REPO_ROLE`
- parametro esplicito dello script

Esempi:

```powershell
.\scripts\workspace-preflight.ps1 -Role ui
```

```bash
CODEX_REPO_ROLE=video bash scripts/workspace-preflight.sh
```

Se non imposti nulla, il fallback e il nome della cartella repo.

## Flusso operativo consigliato all'inizio di ogni task

1. Esegui il preflight nel clone che pensi di avere aperto.
2. Controlla `repo_root`, `branch` e `role`.
3. Solo dopo esegui `git switch`, modifiche o test.
4. Se il risultato non corrisponde alla finestra visibile, chiudi quella chat Codex e riaprila dalla cartella corretta.

## Lavorare in parallelo con due clone

Esempio:

- `C:\repo\DjangoTutorial-ui` con role `ui`
- `C:\repo\DjangoTutorial` con role `video`

Verifica separata:

```powershell
.\scripts\workspace-preflight.ps1
.\scripts\workspace-preflight.ps1 -WorkspacePath C:\repo\DjangoTutorial
```

Se i due output mostrano `repo_root` o `role` inattesi, non eseguire branch switch nella sessione corrente.

## Come riaprire la chat dalla cartella giusta

La regola pratica e semplice:

1. apri VS Code direttamente sulla cartella del clone corretto
2. apri un nuovo terminale in quella finestra
3. esegui il preflight
4. avvia una nuova chat Codex da quella finestra, non riutilizzare una chat nata in un altro clone

## Uso consigliato nei prompt

All'inizio del task puoi chiedere esplicitamente:

```text
Esegui prima il workspace preflight e conferma repo_root, branch e role prima di fare modifiche.
```
