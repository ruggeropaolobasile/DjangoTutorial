# UI Vote Page Polish

Conferma reale della sessione: repo root, branch, head, status.

Segui `AGENTS.md` + `mysite/polls/AGENTS.md` + `agent-docs/playbooks/feature.md`.

Parti da:

- `mysite/polls/templates/polls/detail.html`
- `mysite/polls/static/polls/style.css`

Obiettivo:

- migliora la UX della pagina di voto su desktop e mobile;
- rendi piu evidente l'opzione selezionata;
- chiarisci la gerarchia visiva tra azione primaria, secondaria e link di ritorno.

Vincoli:

- non modificare `models.py`, `views.py`, `urls.py` o la logica POST del form;
- nessun JavaScript obbligatorio;
- mantieni compatibili i name/url esistenti;
- cambi minimi e mirati.

Validazione:

Da `mysite/` con virtualenv attivo esegui:

```bash
python manage.py check
python manage.py test polls
ruff check polls
```

Output richiesto:

- file toccati e motivo;
- miglioramenti visivi introdotti;
- comandi eseguiti con esito;
- eventuali limiti residui.
