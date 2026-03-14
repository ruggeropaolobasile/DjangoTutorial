# Session Lock

Questo playbook serve a evitare sovrapposizioni tra clone, branch, finestre VS Code e sessioni agente.

## Regola base

Una chat/sessione agente vale per un solo clone del repository.

Non si cambia clone implicitamente nella stessa conversazione.
Se serve lavorare su un altro clone, si apre una nuova sessione.

## Contesto canonico

All'inizio della sessione, oppure prima di task importanti, eseguire:

```powershell
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --short HEAD
git status --short
```

Il risultato di questi comandi definisce il contesto canonico della sessione:

- repo root
- branch
- commit corrente
- stato del working tree

Se chat, IDE e terminale mostrano contesti diversi, fa fede il terminale del clone attivo dopo questa verifica.

## Regole operative

- una sessione agente = un clone
- un clone puo avere piu branch, ma non piu sessioni concorrenti
- nessun cambio clone e ammesso senza nuova verifica esplicita
- se il contesto non coincide con quanto dichiarato in chat, correggere subito il contesto canonico

## Quando fermarsi

La sessione deve fermarsi e riallinearsi se:

- il terminale mostra un clone diverso da quello assunto in chat
- il branch reale e diverso da quello dichiarato
- il working tree non e nello stato atteso
- esistono piu finestre VS Code e non e chiaro quale rappresenti il clone attivo

## Obiettivo

Ridurre gli errori di contesto.
L'isolamento filesystem da solo non basta: serve anche isolamento conversazionale e procedurale.
