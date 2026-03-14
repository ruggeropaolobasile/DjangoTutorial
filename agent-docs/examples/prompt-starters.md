# Prompt Starters per Questo Repo

Scopo: trasformare le best practice di prompting in prompt copiabili, ancorati ai file reali del progetto.

## 1. Preflight sessione

Usalo all'inizio di una chat per evitare mismatch tra workspace visibile e root reale della sessione agente.

```text
Conferma reale della sessione: repo root, branch, head, status.
Contesto: stiamo lavorando in C:\repo\DjangoTutorial-video.
Vincoli: non modificare file, non cambiare branch.
Output: 4 righe con root, branch, commit HEAD e working tree.
```

## 2. Feature su polls

```text
Segui AGENTS.md + agent-docs/playbooks/feature.md.
Parti da mysite/polls/views.py, mysite/polls/urls.py e template correlati.
Obiettivo: implementa <feature concreta> in polls.
Vincoli: cambi minimi, niente refactor non richiesti, route esistenti compatibili.
Validazione: da mysite/ esegui python manage.py check, python manage.py test polls, ruff check .
Output: comportamento implementato, file toccati, verifiche eseguite.
```

## 3. Bugfix con regressione

```text
Segui AGENTS.md + agent-docs/playbooks/bugfix.md.
Parti da mysite/polls/tests.py e dai file coinvolti dal bug.
Obiettivo: correggi <bug descrivibile in una frase>.
Contesto: sintomo osservato <...>, comportamento atteso <...>.
Vincoli: fix minimo, aggiungi test di regressione se fattibile.
Validazione: da mysite/ esegui python manage.py test polls -v 2 e python manage.py check.
Output: root cause, fix applicato, test aggiunti o motivo per cui non erano fattibili.
```

## 4. Modifica settings/deploy

```text
Parti da mysite/mysite/settings/base.py e tocca local.py o production.py solo se serve.
Obiettivo: applica <cambio configurazione>.
Vincoli: nessun segreto hardcoded, compatibile con DJANGO_ENV e DATABASE_URL.
Validazione: da mysite/ esegui python manage.py check e python manage.py check --deploy.
Output: impatto del cambio, variabili ambiente coinvolte, rischi residui.
```

## 5. Review del branch

```text
Segui AGENTS.md + agent-docs/playbooks/review.md.
Obiettivo: fai review del diff corrente.
Contesto: branch attuale e file modificati.
Vincoli: priorita a bug, regressioni, rischi deploy e test mancanti.
Output: findings ordinati per severita con file/linea; se non ci sono finding, dichiaralo esplicitamente.
```

## 6. Micro-task UI delegabile al clone `ui`

Caso concreto adatto a una sessione separata sul clone UI: migliorare la UX della pagina di voto senza cambiare la logica server-side.

```text
Conferma reale della sessione: repo root, branch, head, status.
Segui AGENTS.md + mysite/polls/AGENTS.md + agent-docs/playbooks/feature.md.
Parti da mysite/polls/templates/polls/detail.html e mysite/polls/static/polls/style.css.
Obiettivo: migliora la UX della pagina di voto su desktop e mobile rendendo piu evidente l'opzione selezionata e piu chiara la gerarchia delle azioni.
Vincoli: non modificare models, views, urls o form POST; nessun JavaScript obbligatorio; mantieni compatibili i name/url esistenti.
Validazione: da mysite/ esegui python manage.py check, python manage.py test polls, ruff check polls.
Output: file toccati, comportamento visivo migliorato, verifiche eseguite e limiti residui.
```

Perche questo task e adatto al clone `ui`:

1. tocca solo template e CSS;
2. ha impatto visibile immediato;
3. non apre rischio su database, deploy o routing;
4. usa un prompt ancorato a file precisi, come suggerito dal video.

Se vuoi usare un prompt file invece di copiare testo in chat, vedi:

- `agent-docs/examples/prompts/ui-vote-page-polish.md`

## Nota didattica

La struttura comune e sempre questa:

1. punto di partenza preciso;
2. obiettivo concreto;
3. vincoli espliciti;
4. validazione verificabile.

Questo e il motivo per cui questi prompt funzionano meglio di richieste generiche come `sistema polls`.
