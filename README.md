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

## Workflow Git consigliato

1. Lavora su branch feature (`feature/...`).
2. Esegui test/check in locale.
3. Fai PR o merge su `main` solo quando e stabile.
4. Push su `main` -> deploy automatico Render.

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
