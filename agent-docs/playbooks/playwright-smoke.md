# Playbook - Playwright Smoke

## Obiettivo

Verificare in un browser reale il flow essenziale:

1. login
2. create poll
3. vote
4. results

## Setup minimo

Da root (PowerShell):

```powershell
.\scripts\session-context.ps1
.\scripts\playwright-smoke-setup.ps1
```

Il setup:

- applica migrate locali
- reseed demo data profilo `mvp`
- crea/aggiorna l'utente smoke `demo-user`
- stampa URL e credenziali da usare nel browser

Credenziali di default:

- username: `demo-user`
- password: `safe-password-123`

## Esecuzione Playwright

Usare la skill `playwright` oppure il wrapper CLI locale.

PowerShell:

```powershell
if (-not $env:CODEX_HOME) { $env:CODEX_HOME = "$HOME/.codex" }
$env:PWCLI = "$env:CODEX_HOME\\skills\\playwright\\scripts\\playwright_cli.ps1"
```

Flusso consigliato:

```powershell
& $env:PWCLI open http://127.0.0.1:8000/accounts/login/ --headed
& $env:PWCLI snapshot
```

Poi:

1. eseguire login con `demo-user` / `safe-password-123`
2. aprire `Create`
3. creare una poll nuova con una domanda univoca e almeno due scelte
4. confermare redirect alla pagina dettaglio
5. votare una scelta
6. verificare che la pagina results mostri la domanda appena creata e `Total votes collected: 1`

## Dati consigliati per la smoke poll

- question: `Smoke flow <timestamp>`
- choices:
  - `Option A`
  - `Option B`

## Esito atteso

- login riuscito con navbar `Signed in as demo-user`
- poll creata e visibile nella detail page
- submit vote riuscito
- results page raggiunta senza errori
- contatore totale voti aggiornato a `1`
