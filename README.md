# DjangoTutorial

App Django tutorial con deploy su Render e sviluppo locale guidato.

## Struttura progetto

- `mysite/` contiene il progetto Django
- `mysite/mysite/settings/` contiene configurazioni separate:
  - `base.py`
  - `local.py`
  - `production.py`
- `mysite/requirements/` contiene dipendenze separate (`base`, `dev`, `prod`)

La selezione settings avviene con `DJANGO_ENV`:

- `DJANGO_ENV=local` -> `mysite.settings.local`
- `DJANGO_ENV=production` -> `mysite.settings.production`
- default: `local`

## Sviluppo locale (best practice)

### Runtime sviluppo (1 comando)

PowerShell:
```powershell
.\scripts\dev.ps1
```

Opzioni utili:
```powershell
.\scripts\dev.ps1 -BindHost 0.0.0.0 -Port 8001 -SkipInstall
.\scripts\dev.ps1 -SkipMigrate
```

Se l'automazione browser si blocca su Chrome senza chiudere tutte le finestre:
```powershell
.\scripts\reset-playwright-chrome.ps1
```

Git Bash:
```bash
bash scripts/dev.sh
```

Opzioni utili:
```bash
HOST=0.0.0.0 PORT=8001 SKIP_INSTALL=1 bash scripts/dev.sh
SKIP_MIGRATE=1 bash scripts/dev.sh
```

### 1) Crea e attiva virtual environment

PowerShell:
```powershell
cd mysite
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Git Bash:
```bash
cd mysite
python -m venv .venv
source .venv/Scripts/activate
```

### 2) Installa dipendenze di sviluppo

```bash
pip install -r requirements/dev.txt
```

### 3) Configura variabili ambiente locali

Dal root del repository:
```bash
cp .env.example .env
```

Il progetto legge automaticamente `.env` (root repo o `mysite/.env`).

### 4) Inizializza DB locale

```bash
cd mysite
python manage.py migrate
python manage.py createsuperuser
```

### 5) Avvia il server

```bash
python manage.py runserver
```

App disponibile su `http://127.0.0.1:8000/`.

## Quality checks locali

Da `mysite/` con venv attivo:

```bash
python manage.py test
python manage.py check
ruff check .
ruff format --check .
```

Oppure da root (PowerShell):
```powershell
.\scripts\preflight.ps1
.\scripts\preflight.ps1 -SkipTests
.\scripts\preflight.ps1 -DeployChecks
```

## Workflow Git consigliato

1. Lavora su branch feature (`feature/...`).
2. Esegui test/check in locale.
3. Fai PR o merge su `main` solo quando e stabile.
4. Push su `main` -> deploy automatico Render.

### Switch branch in sicurezza

PowerShell:
```powershell
.\scripts\safe-switch-branch.ps1 -Branch fix/polls-vote-guard -CreateFromMain
.\scripts\safe-switch-branch.ps1 -Branch chore/codex-onboarding-from-video
```

Git Bash:
```bash
bash scripts/safe-switch-branch.sh fix/polls-vote-guard --create-from-main
bash scripts/safe-switch-branch.sh chore/codex-onboarding-from-video
```

## Quality Gate su PR

- CI GitHub Actions esegue:
  - `python manage.py check`
  - `python manage.py test`
  - `ruff check mysite`
  - `python manage.py check --deploy`
- `main` e protetto con status check obbligatori e review richiesta.

## Workflow Codex (dal video, adattato al repo)

Questo repository include un file [`AGENTS.md`](AGENTS.md) per dare a Codex contesto stabile su struttura, comandi e vincoli.

Gerarchia istruzioni agente:

- Root: [`AGENTS.md`](AGENTS.md) (regole globali repository)
- App: [`mysite/polls/AGENTS.md`](mysite/polls/AGENTS.md) (regole specifiche app polls)
- Settings: [`mysite/mysite/settings/AGENTS.md`](mysite/mysite/settings/AGENTS.md) (regole configurazione/deploy)

Prompt starter (copy-paste) consigliati:

```text
Obiettivo: Implementa <feature> in polls.
Contesto: mysite/polls/views.py, mysite/polls/urls.py, template correlati.
Vincoli: non cambiare comportamento delle route esistenti.
Validazione: python manage.py check && python manage.py test polls
Output: causa, file toccati, test eseguiti.
```

```text
Obiettivo: Correggi bug <descrizione> in polls.
Contesto: riproduci il bug e aggiungi test regressione in mysite/polls/tests.py.
Vincoli: cambi minimi, niente refactor non richiesti.
Validazione: python manage.py test polls -v 2
Output: root cause, fix, test aggiunti.
```

```text
Obiettivo: Modifica configurazione deploy/settings in sicurezza.
Contesto: mysite/mysite/settings/base.py (+ local.py/production.py se necessario).
Vincoli: nessun segreto hardcoded, compatibile Render.
Validazione: python manage.py check && python manage.py check --deploy
Output: variabili env introdotte/aggiornate e impatto.
```

```text
Obiettivo: Fai review del diff corrente.
Contesto: tutto il branch.
Vincoli: priorita a bug/regressioni/rischi deploy.
Validazione: indica test mancanti o non eseguiti.
Output: findings per severita con file/linea.
```

### Runbook anti-conflitto (sessioni multiple)

Se usi piu agenti in parallelo, evita di farli lavorare sullo stesso clone.

- Usa clone separati:
  - `C:\repo\DjangoTutorial` per onboarding/processo
  - `C:\repo\DjangoTutorial-ui` per lavoro UI
- Una sessione agente per clone.
- Prima di cambiare branch: working tree pulito (`git status`).
- Se hai WIP non committato: `git stash push -u -m "<nome-wip>"` prima dello switch.
- Preferisci commit piccoli e frequenti (1 blocco logico = 1 commit).

### Onboarding docs

- [`docs/onboarding/00-video-logical-map.md`](docs/onboarding/00-video-logical-map.md)
- [`docs/onboarding/01-branch-and-clone-strategy.md`](docs/onboarding/01-branch-and-clone-strategy.md)
- [`docs/onboarding/02-agents-hierarchy.md`](docs/onboarding/02-agents-hierarchy.md)
- [`docs/onboarding/03-pr-ci-process.md`](docs/onboarding/03-pr-ci-process.md)
- [`docs/onboarding/04-preflight-and-safe-switch.md`](docs/onboarding/04-preflight-and-safe-switch.md)

## Dipendenze

- Base comuni: `mysite/requirements/base.txt`
- Produzione: `mysite/requirements/prod.txt` (include `psycopg2-binary`)
- Sviluppo: `mysite/requirements/dev.txt`
- Render installa: `mysite/requirements.txt` (punta a `requirements/prod.txt`)

## Deploy Render (Blueprint)

1. Render -> New -> Blueprint
2. Seleziona il repository
3. Conferma creazione da `render.yaml`
4. Verifica endpoint:
   - `https://<tuo-dominio>.onrender.com/healthz/`
   - `https://<tuo-dominio>.onrender.com/`
   - `https://<tuo-dominio>.onrender.com/polls/`
   - `https://<tuo-dominio>.onrender.com/admin/`

## Variabili ambiente produzione

- `SECRET_KEY` (obbligatoria)
- `DEBUG=False`
- `PUBLIC_DOMAIN=<host pubblico>` oppure `ALLOWED_HOSTS=<host pubblico>`
- `CSRF_TRUSTED_ORIGINS=https://<host pubblico>`
- `DATABASE_URL=<postgres connection string>`
- opzionale: `SECURE_SSL_REDIRECT=True`

## Note operative

- `/healthz/` ritorna `200` se app+DB sono ok, `503` se DB non raggiungibile.
- Il piano free Render puo avere cold start dopo inattivita.
