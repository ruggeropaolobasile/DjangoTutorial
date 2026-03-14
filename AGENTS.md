# AGENTS.md

Istruzioni operative per agenti AI (Codex/CLI/IDE) su questo repository.

## Obiettivo del progetto

Applicazione Django di tutorial con:
- app principale `polls`
- configurazione `settings` separata per `local` e `production`
- workflow di deploy su Render

L'obiettivo durante le modifiche e mantenere il progetto stabile in locale (`sqlite`) e in produzione (`postgres` via `DATABASE_URL`).

## Struttura da conoscere

- `mysite/manage.py`: entrypoint Django
- `mysite/mysite/settings/base.py`: configurazione condivisa
- `mysite/mysite/settings/local.py`: override sviluppo locale
- `mysite/mysite/settings/production.py`: override produzione
- `mysite/polls/`: app tutorial (models, views, templates, admin)
- `scripts/dev.ps1` e `scripts/dev.sh`: avvio sviluppo one-command

## Comandi standard

Da root:

```powershell
.\scripts\dev.ps1
```

Da `mysite/` con virtualenv attivo:

```bash
python manage.py migrate
python manage.py test
python manage.py check
ruff check .
ruff format --check .
```

## Regole di modifica

- Preferire cambi minimi e mirati; evitare refactor non richiesti.
- Non toccare `.venv/`, `.venv311/`, cache o file generati automaticamente.
- Non modificare `db.sqlite3` salvo richiesta esplicita.
- Se serve una migration: creare migration + verificare `python manage.py migrate`.
- Mantenere compatibilita con configurazione `DJANGO_ENV` e variabili ambiente esistenti.

## Definition of Done

Una task e completa quando:

1. Il comportamento richiesto e implementato.
2. Le route/pagine coinvolte rispondono correttamente.
3. `python manage.py check` non segnala errori.
4. Se possibile, test rilevanti eseguiti (o motivare se non eseguiti).
5. Il diff non include file non pertinenti.

## Prompt patterns consigliati

Usare richieste esplicite e verificabili.

Feature:

```text
Implementa <feature> in polls, aggiorna template e urls se serve.
Vincoli: non cambiare il comportamento esistente di <area>.
Esegui check finali e mostrami file toccati + motivazione.
```

Bugfix:

```text
Riproduci e correggi il bug <descrizione>.
Aggiungi test di regressione in polls/tests.py.
Mostrami causa radice, fix e come verificarlo.
```

Code review:

```text
Fai review del diff corrente con priorita a bug/regressioni.
Elenca findings per severita con file/linea e proposta di fix.
```
