# Video Step 04:17 -> 08:12 (Setup, Login, First Runs)

Questo documento traduce in pratica il blocco del video in cui passano da teoria a setup operativo.

## 1) Focus sessione

Messaggio del video:
- focus su CLI + IDE
- uso di un repository open source per seguire la demo

Applicazione pratica:
- scegli un clone dedicato per questo stream (`DjangoTutorial`)
- verifica subito branch/worktree:
  - `git branch --show-current`
  - `git status --short`

## 2) Installazione Codex CLI

Messaggio del video:
- install via package manager (brew/npm) per restare aggiornati rapidamente
- i rilasci sono frequenti

Applicazione pratica:
- verifica versione:
  - `codex --version`
- aggiornamento (se necessario):
  - `npm install -g @openai/codex@latest`

## 3) Installazione estensione IDE

Messaggio del video:
- installa estensione ufficiale OpenAI in VS Code
- abilita aggiornamenti automatici

Applicazione pratica:
- verifica estensione installata:
  - `code --list-extensions | Select-String openai.chatgpt`

## 4) Login

Messaggio del video:
- login da CLI o IDE, poi sessione pronta su entrambi i canali

Applicazione pratica:
- stato login:
  - `codex login status`

## 5) Slash command utile: status

Messaggio del video:
- `/status` mostra modello, directory, sandbox, approval, contesto sessione

Applicazione pratica:
- equivalente non-interattivo:
  - `codex exec "Mostrami modello, workdir e sandbox in 3 righe."`

## 6) Primo run su repository

Messaggio del video:
- clona repo demo e fai girare il progetto locale

Applicazione pratica (repo Django):
- primo run operativo equivalente:
  - `.\scripts\dev.ps1` (runtime locale completo)
- check rapido qualità:
  - `.\scripts\preflight.ps1 -SkipTests`

## Done del blocco 04:17->08:12

- [ ] CLI installata e verificata (`codex --version`)
- [ ] Estensione IDE verificata
- [ ] Login confermato (`codex login status`)
- [ ] Primo comando Codex eseguito
- [ ] Runtime progetto avviabile
