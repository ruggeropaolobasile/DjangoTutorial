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

## Anti-pattern

Evita prompt troppo generici come:

- `migliora tutto polls`
- `sistema il progetto`
- `fai refactor generale`

Sono richieste troppo larghe e aumentano il rischio che l'agente esplori zone non pertinenti.
