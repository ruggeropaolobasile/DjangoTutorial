# PLANS.md

Regole ufficiali del repository per scrivere e mantenere ExecPlans.
Un ExecPlan e un documento di implementazione eseguibile per task grandi/multi-step.

## How to use ExecPlans and PLANS.md

Quando scrivi un ExecPlan, segui questo file alla lettera.
Quando implementi un ExecPlan, non chiedere "next steps": prosegui al milestone successivo finche il piano e completato.
Quando prendi decisioni o cambi direzione, aggiorna il piano subito.
Un nuovo contributore deve poter ripartire da zero leggendo solo il piano.

## Requirements

Requisiti non negoziabili:

- Ogni ExecPlan deve essere self-contained: deve includere tutto il necessario per un principiante.
- Ogni ExecPlan deve essere un documento vivo: va aggiornato durante il lavoro.
- Ogni ExecPlan deve portare a comportamento funzionante e osservabile, non solo a modifiche di codice.
- Ogni termine tecnico non ovvio deve essere definito in linguaggio semplice.
- Ogni assunzione deve essere esplicitata nel piano.

## Formatting

Quando l'ExecPlan viene inviato in chat, deve stare in un singolo blocco fenced `md`.
Quando l'ExecPlan viene salvato in un file `.md` che contiene solo il piano, non usare i triple backticks esterni.
Usa prosa chiara; evita liste lunghe non necessarie.
Checklist obbligatorie solo nella sezione `Progress`.

## Guidelines

Scrivi per un principiante del repo:

- spiega cosa cambia per l'utente e come vederlo funzionare;
- indica file e percorsi repository-relative precisi;
- indica directory e comandi esatti da eseguire;
- mostra output attesi e criteri di successo osservabili;
- preferisci passi idempotenti e con recovery esplicito.

Non delegare decisioni chiave al lettore.
Quando c'e ambiguita, scegli nel piano e spiega il motivo.

## Milestones

I milestone raccontano la storia del lavoro: obiettivo, lavoro, risultato, prova.
Ogni milestone deve essere verificabile in modo indipendente e aggiungere valore incrementale.
`Progress` e milestone sono distinti: i milestone spiegano il flusso, `Progress` traccia lo stato fine-grained.

## Living plans and design decisions

Ogni ExecPlan deve includere e mantenere aggiornate queste sezioni:

- `Progress` (obbligatoria, con checkbox e timestamp)
- `Surprises & Discoveries`
- `Decision Log`
- `Outcomes & Retrospective`

Ogni revisione significativa deve aggiornare tutte le sezioni impattate e aggiungere in fondo una nota di revisione con motivo.

## Prototyping and parallel implementations

Se ci sono incertezze elevate, aggiungi milestone espliciti di prototipazione.
I prototipi devono essere additivi, testabili e con criteri chiari di promozione/scarto.
Sono ammessi percorsi paralleli temporanei (nuovo + vecchio) se riducono il rischio; va definito come validarli e ritirare il percorso legacy in sicurezza.

## ExecPlan skeleton

Ogni nuovo ExecPlan deve usare questo scheletro minimo.
Template copiabile: `agent-docs/execplan-template.md`.

Sezioni richieste nel piano:

1. Titolo action-oriented.
2. Purpose / Big Picture.
3. Progress.
4. Surprises & Discoveries.
5. Decision Log.
6. Outcomes & Retrospective.
7. Context and Orientation.
8. Plan of Work.
9. Concrete Steps.
10. Validation and Acceptance.
11. Idempotence and Recovery.
12. Artifacts and Notes.
13. Interfaces and Dependencies.

## Repository defaults (DjangoTutorial)

Per default usa queste validazioni:

- Da `mysite/`:
  - `python manage.py check`
  - `python manage.py test`
  - `ruff check .`
  - `ruff format --check .`

Se il task tocca deploy/settings, aggiungi anche il check deploy appropriato e documenta output atteso.
