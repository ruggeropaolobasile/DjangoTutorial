# AGENTS.md

Istruzioni operative per agenti AI (Codex/CLI/IDE) su questo repository.

## Obiettivo del progetto

Mantenere il progetto Django tutorial stabile in locale (`sqlite`) e in produzione (`postgres` via `DATABASE_URL`), con modifiche piccole e verificabili.

## Struttura da conoscere

- `mysite/manage.py`
- `mysite/mysite/settings/base.py`
- `mysite/mysite/settings/local.py`
- `mysite/mysite/settings/production.py`
- `mysite/polls/`
- `scripts/dev.ps1`, `scripts/dev.sh`, `scripts/preflight.*`, `scripts/safe-switch-branch.*`

## Gerarchia AGENTS.md

- Questo file vale a livello repository.
- I file `AGENTS.md` in sottocartelle aggiungono regole locali.
- In conflitto, vince la regola piu specifica (piu vicina ai file toccati).

## Comandi minimi di verifica

Da root (PowerShell):

```powershell
.\scripts\session-context.ps1
.\scripts\preflight.ps1
```

Preflight obbligatorio prima di modifiche o branch switch:

```powershell
.\scripts\workspace-preflight.ps1
```

Da `mysite/` con virtualenv attivo:

```bash
python manage.py check
python manage.py test
ruff check .
ruff format --check .
```

## CLI tools and MCP

- CLI tools preferiti nel repository:
  - `git` (branch, diff, commit, push)
  - `python manage.py` (check/test/migrate)
  - `ruff` (lint/format checks)
- script locali: `scripts/dev.ps1`, `scripts/preflight.ps1`, `scripts/safe-switch-branch.ps1`
- per conferma sessione/worktree: `scripts/session-context.ps1`
- MCP:
  - stato attuale: nessun server MCP di progetto obbligatorio configurato.
  - quando introdurre MCP: solo se aggiunge contesto reale utile (es. issue tracker, monitoring, design source).
  - regola: documentare ogni MCP introdotto in `docs/onboarding` con scopo, permessi minimi e fallback senza MCP.

## Regole di modifica

- Preferire cambi minimi e mirati; evitare refactor non richiesti.
- Non toccare `.venv/`, `.venv311/`, cache, file generati automaticamente.
- Non modificare `db.sqlite3` salvo richiesta esplicita.
- Se serve una migration: crearla e verificare `python manage.py migrate`.
- Mantenere compatibilita con configurazione `DJANGO_ENV` e variabili ambiente esistenti.
- Non assumere che Explorer VS Code, terminale integrato e sessione agente puntino alla stessa root: verificare sempre `repo_root`, `branch` e `role` con `scripts/workspace-preflight.ps1`.

## Strategia branch

- Base branch: `main`.
- Un task = un branch dedicato (`feature/*`, `fix/*`, `chore/*`).
- L'agente usa il branch attualmente checkoutato e non cambia branch da solo, salvo richiesta esplicita.
- Merge su `main` solo tramite PR con CI verde.

## Concorrenza sessioni

- Non eseguire due sessioni agente sullo stesso clone contemporaneamente.
- Se servono lavori paralleli, usare clone separati del repository.
- Prima di cambiare branch: working tree pulito (`git status`) o stash nominato.

## Session lock

- Una chat/sessione agente vale per un solo clone del repository.
- Il contesto canonico della sessione va fissato all'inizio con `.\scripts\session-context.ps1`
  oppure, in fallback, con:
  - `git rev-parse --show-toplevel`
  - `git branch --show-current`
  - `git rev-parse --short HEAD`
  - `git status --short`
- Quel contesto resta valido finche non viene rifatta una verifica esplicita.
- Nessun cambio clone e ammesso implicitamente nella stessa chat.
- Se emerge un contesto diverso tra chat, IDE e terminale, fa fede il terminale del clone attivo dopo la verifica dei comandi sopra.
- Se serve lavorare su un clone diverso, aprire una nuova sessione/chat.

## Definition of Done

1. Il comportamento richiesto e implementato.
2. Le route/pagine coinvolte rispondono correttamente.
3. `python manage.py check` non segnala errori.
4. Test rilevanti eseguiti (o motivare se non eseguiti).
5. Il diff non include file non pertinenti.

## Agentic loop (punto 2)

- Ogni task deve chiudersi con un loop `modifica -> verifica -> fix -> riverifica`.
- Se un controllo viene ripetuto spesso a mano dopo l'esecuzione dell'agente, va codificato in script/checklist.

## Errori reali e miglioramento continuo (punto 3)

- Mantenere un log leggero dei problemi reali incontrati (gotchas) e della correzione adottata.
- Ogni errore ricorrente deve produrre almeno uno tra: regola AGENTS, check/script, test, nota onboarding.

## File task-specific (punto 4)

- Per task non banali, seguire un `.md` dedicato invece di sovraccaricare questo file.
- `AGENTS.md` resta corto: regole globali qui, dettagli operativi nei playbook task-specific.
- Per task grandi/multi-step, usare `agent-docs/PLANS.md` come documento vivo.
- Ogni ExecPlan deve usare il template `agent-docs/execplan-template.md`.
- Nei prompt, ancorare quando possibile il task a file/cartelle precise.

## Dove trovare i dettagli

- Onboarding index: `agent-docs/README.md`
- Strategia branch/clone: `agent-docs/01-branch-and-clone-strategy.md`
- Gerarchia agents: `agent-docs/02-agents-hierarchy.md`
- Processo PR/CI: `agent-docs/03-pr-ci-process.md`
- Preflight/switch: `agent-docs/04-preflight-and-safe-switch.md`
- MCP starter: `agent-docs/05-mcp-github-starter.md`
- Agentic loops: `agent-docs/07-unlock-agentic-loops.md`
- Gotchas e miglioramento continuo: `agent-docs/08-real-mistakes-and-gotchas.md`
- Playbook task-specific: `agent-docs/09-task-specific-playbooks.md`
- Codex config/profili: `agent-docs/10-codex-config-and-profiles.md`
- Prompting best practices: `agent-docs/11-prompting-best-practices.md`
- Session lock playbook: `agent-docs/12-session-lock.md`
- Project backlog flow: `agent-docs/13-project-backlog-flow.md`
- Planning template: `agent-docs/PLANS.md`
- ExecPlan template: `agent-docs/execplan-template.md`

## Formato risposta agente

- Prima: soluzione in 1-3 righe.
- Poi: file toccati + motivazione sintetica.
- Infine: comandi eseguiti e risultato.
- Se qualcosa non e verificabile localmente, dichiararlo esplicitamente.

