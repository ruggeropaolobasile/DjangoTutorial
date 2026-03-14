# 07 - Unlock Agentic Loops

Obiettivo: ridurre lavoro manuale ripetitivo dopo che l'agente ha "finito".

## Principio

Se dopo ogni run fai sempre gli stessi passi (check, test, lint, verify), quei passi devono diventare un loop esplicito e ripetibile.

Loop standard nel progetto:

1. Implementa modifica minima.
2. Esegui verifica (`scripts/preflight.*` o check equivalenti).
3. Se fallisce: correggi la causa radice.
4. Riesegui verifica.
5. Solo con esito verde: prepara commit/PR.

## Applicazione concreta in DjangoTutorial

- Verifica primaria da root: `scripts/preflight.ps1` (o `.sh`).
- Verifica equivalente da `mysite/`:
  - `python manage.py check`
  - `python manage.py test`
  - `ruff check .`
  - `ruff format --check .`
- In PR, riportare sempre cosa e stato eseguito e con quale esito.

## Regola di evoluzione

Quando scopriamo un errore ricorrente:

1. aggiungiamo un controllo/script o una regola breve in `AGENTS.md`;
2. documentiamo il caso in onboarding;
3. includiamo il controllo nel flusso PR.

In questo modo il processo migliora ad ogni errore reale e l'agente diventa piu affidabile nel tempo.
