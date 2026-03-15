# 14 - Autonomous Session Runner

Obiettivo: trasformare il backlog GitHub Project in una coda operativa per `codex exec`, cosi la sessione puo prendere un item, lavorarlo, verificarlo e poi passare al successivo senza un nuovo prompt manuale.

## Cosa fa

Lo script PowerShell `scripts/autonomous-session.ps1`:

- conferma che il clone corrente e un repo Git valido;
- richiede una working tree pulita all'avvio;
- legge il project canonico con `gh project`;
- sceglie il prossimo item `Todo` usando la regola del repository (`Priority`, poi `Size`);
- sposta l'item a `In progress`;
- invoca `codex exec` con prompt strutturato e output JSON vincolato da schema;
- esegue `scripts/preflight.ps1` dopo un risultato `done`, salvo `-SkipPreflight`;
- marca l'item `Done`, oppure lo riporta a `Todo` se il task e `blocked` o `needs_input`.

## Perche non basta il backlog flow documentale

`agent-docs/13-project-backlog-flow.md` definisce la logica di scelta del prossimo task.
Il runner aggiunge il pezzo che mancava: l'esecuzione ripetuta e non interattiva del worker Codex.

## Comando base

Da root del repository:

```powershell
.\scripts\autonomous-session.ps1
```

Questo usa di default:

- owner project `ruggeropaolobasile`
- project `1`
- profilo Codex `autonomous`
- `preflight` attivo
- massimo `2` tentativi per item

## Modalita utili

Lavorare un solo item e fermarsi:

```powershell
.\scripts\autonomous-session.ps1 -MaxItems 1
```

Saltare i check finali del repository:

```powershell
.\scripts\autonomous-session.ps1 -SkipPreflight
```

Provare batch continui con commit automatico dopo task verde:

```powershell
.\scripts\autonomous-session.ps1 -CommitOnDone
```

Nota: `-CommitOnDone` rende il loop davvero continuo su piu item, ma va usato solo su un branch pensato per batch automation. La strategia branch del repo resta valida: non cambiare branch automaticamente e non mischiare task eterogenei senza una scelta esplicita.

## Contratto di output del worker

Il file `scripts/autonomous-session.schema.json` impone un output finale JSON con:

- `status`: `done`, `blocked`, `needs_input`, `failed`
- `summary`: frase breve sul risultato
- `tests_run`: lista dei check eseguiti
- `notes`: opzionale

Questo permette al runner di decidere in modo deterministico come trattare l'item del backlog.

## Stop conditions reali

Il runner si ferma quando:

- non ci sono piu item `Todo`;
- la working tree non e piu pulita prima di prendere il task successivo;
- Codex chiede input umano (`needs_input`);
- `codex exec` fallisce;
- il task non passa `preflight` entro il numero massimo di tentativi.

## Limiti attuali

- versione iniziale solo PowerShell;
- non scrive commenti o note nel Project item quando un task torna a `Todo`;
- non cambia branch da solo per rispettare la policy del repository;
- senza `-CommitOnDone`, dopo un task completato con modifiche locali il loop si fermera prima dell'item successivo per evitare collisioni tra diff.

## Uso consigliato

Per sessioni lunghe e relativamente autonome:

1. aprire un clone dedicato;
2. partire da working tree pulita;
3. usare un branch esplicito per il batch;
4. avviare `.\scripts\autonomous-session.ps1 -CommitOnDone`;
5. monitorare periodicamente il repo e il Project board.
