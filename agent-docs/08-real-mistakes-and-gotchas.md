# 08 - Real Mistakes and Gotchas

Obiettivo: trasformare errori reali in miglioramenti permanenti del processo.

## Regola base

Quando emerge un errore concreto (in locale, CI o PR review):

1. descrivere il problema in modo verificabile;
2. registrare la causa radice;
3. applicare la correzione minima;
4. aggiungere una protezione per evitare recidive (check, test, regola, script);
5. tracciare il cambiamento in PR.

## Template entry (Gotcha)

```md
## YYYY-MM-DD - <titolo breve>
- Contesto: <dove e successo>
- Sintomo: <errore osservato>
- Root cause: <causa reale>
- Fix applicato: <cosa abbiamo cambiato>
- Prevenzione: <test/check/regola aggiunta>
- Riferimenti: <commit/PR/file>
```

## Esempio reale (questo repo)

## 2026-03-14 - preflight PowerShell non falliva su errori nativi
- Contesto: review automatica su PR scripts.
- Sintomo: script preflight poteva terminare con successo anche con comandi falliti.
- Root cause: assenza di controllo esplicito su `$LASTEXITCODE` dopo comandi nativi.
- Fix applicato: gestione esplicita exit code e correzione isolamento env vars in `-DeployChecks`.
- Prevenzione: mantenere il controllo nel preflight e riusare il loop `modifica -> verifica -> riverifica`.
- Riferimenti: commit `c470627`, file `scripts/preflight.ps1`.

## Dove mantenere il log

- Questo file e il log centrale dei gotchas di processo.
- Se un gotcha e locale a una cartella specifica, aggiungere nota anche nel relativo `AGENTS.md` locale.
