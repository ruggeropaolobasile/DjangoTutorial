# 11 - Prompting Best Practices

Obiettivo: dare a Codex contesto chiaro e un punto di partenza corretto, riducendo esplorazioni inutili del codebase.

## Idea chiave

Il prompt e il contesto piu importante della sessione.
Un buon prompt non dice solo "cosa fare", ma anche "dove guardare", "cosa non toccare" e "come verificare".

## Prompt anchoring

Quando possibile, ancora il prompt a un file o a una directory precisa.
Questo aiuta Codex a partire dalla zona giusta del repository invece di cercare in aree non rilevanti.

Esempi nel nostro repo:

- `Parti da mysite/polls/views.py e correggi la view index.`
- `Usa agent-docs/PLANS.md per scomporre il task in milestone.`
- `Controlla mysite/mysite/settings/production.py senza modificare polls.`

## Parti piccolo, poi amplia

Se stai iniziando o il problema e ambiguo, parti con task piccoli e verificabili.
Quando il comportamento dell'agente e affidabile, amplia gradualmente unita di lavoro e ambito.

## Usa Codex per scomporre

Se il task e troppo grande, chiedi prima una scomposizione:

- obiettivo
- file di partenza
- vincoli
- piano di verifica

Questo riduce il rischio di output troppo ampi o poco controllabili.

## Formula pratica

Prompt consigliato:

```text
Parti da <file o cartella>.
Obiettivo: <risultato concreto>.
Vincoli: <cosa non toccare>.
Validazione: <comandi o comportamento atteso>.
```

Per esempi gia adattati a questo repository vedi:

- `agent-docs/examples/prompt-starters.md`

## Quando il prompt non basta piu

Usa il livello di struttura minimo che tiene il task sotto controllo:

- solo prompt: per task piccoli, confinati a pochi file, con esito verificabile in un singolo loop;
- prompt + playbook: per task ricorrenti come `feature`, `bugfix` o `review`, dove serve un flusso standard oltre all'obiettivo;
- ExecPlan (`agent-docs/PLANS.md`): per task grandi o multi-step, con dipendenze, decisioni da tracciare o handoff tra sessioni.

Segnali che indicano che devi salire a un ExecPlan:

- il task tocca piu aree del repo;
- richiede milestone o ordine di esecuzione;
- ci sono incertezze tecniche da documentare;
- vuoi che una nuova sessione possa ripartire senza leggere la chat precedente.

Formula pratica per escalation:

```text
Usa AGENTS.md + agent-docs/PLANS.md.
Prepara un ExecPlan usando agent-docs/execplan-template.md.
Parti da <file/cartelle>.
Obiettivo: <risultato concreto>.
Validazione: <check osservabili>.
```

## Esempi concreti in questo repo

Esempi di task che stanno bene in un prompt semplice:

- ritoccare la UX della pagina voto partendo da `mysite/polls/templates/polls/detail.html` e `mysite/polls/static/polls/style.css`;
- aggiungere un test mirato in `mysite/polls/tests.py` per una view gia esistente;
- fare review del diff corrente con focus su `polls`.

Esempi di task che richiedono prompt + playbook:

- correggere un bug in `polls` con riproduzione, fix minimo e test di regressione;
- aggiungere una piccola feature a `polls` che tocca view, template e test ma resta confinata all'app;
- fare una review strutturata del branch con findings ordinati per severita.

Esempi di task che meritano un ExecPlan:

- riorganizzare i settings tra `base.py`, `local.py` e `production.py` con impatto su deploy;
- introdurre o cambiare il flusso di `scripts/preflight.ps1` e allineare README, AGENTS e CI;
- preparare una modifica multi-step che tocchi `polls`, documentazione, script e handoff tra clone `video` e clone `ui`.

Regola pratica:

Se il task puo essere descritto bene in 4-6 righe, tocca pochi file e si verifica in un unico ciclo, un prompt basta.
Se devi spiegare ordine, dipendenze, fallback o punti decisionali, sei gia nel territorio di un ExecPlan.

## Scala decisionale rapida

Usa questa sequenza come regola operativa nel repository:

1. Prompt semplice
   Per task piccoli e confinati.
2. Prompt file
   Quando vuoi riusare lo stesso task o delegarlo a un'altra sessione senza riscriverlo.
3. Prompt + playbook
   Quando oltre all'obiettivo serve anche un flusso standard di esecuzione.
4. ExecPlan
   Quando il task e multi-step, coinvolge piu aree o deve sopravvivere a handoff e cambi di direzione.

In dubbio, parti dal livello piu piccolo che rende il task chiaro.
Se durante il lavoro compaiono dipendenze o milestone, fai escalation esplicita al livello successivo.

## Anti-pattern

Evita prompt troppo generici come:

- `migliora tutto polls`
- `sistema il progetto`
- `fai refactor generale`

Sono richieste troppo larghe e aumentano il rischio che l'agente esplori zone non pertinenti.
