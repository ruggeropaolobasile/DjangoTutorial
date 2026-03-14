# Video Logical Map (Text + Visual)

Fonte: `Getting started with Codex` (`px7XlbYgk7I`), analizzato con trascrizione + snapshot capitoli.

## 00:00 - Introduzione e modello operativo

- Segnale testuale: uso di Codex come agente per delegare task ripetitivi.
- Segnale visivo: slide "How AI Native Teams Plan, Build, Test, and Ship" con fasi end-to-end.
- Applicazione nel repo:
  - processo esplicito in `AGENTS.md` (global + locali),
  - branch strategy e quality gate documentati.

## 04:00 - Setup iniziale e first runs

- Segnale testuale: install CLI/IDE, login, primo run su repo.
- Segnale visivo: demo ambiente locale/repo in esecuzione.
- Applicazione nel repo:
  - workflow standardizzato in `README.md`,
  - script operativi (`dev`, `safe-switch-branch`, `preflight`).

## 08:12 - AGENTS.md come contesto persistente

- Segnale testuale: `AGENTS.md` come "README per agenti", gerarchia root + subdirectory.
- Segnale visivo: contenuti orientati a piani/istruzioni strutturate (Plans/ExecPlan).
- Applicazione nel repo:
  - `AGENTS.md` root con regole globali,
  - `mysite/polls/AGENTS.md`,
  - `mysite/mysite/settings/AGENTS.md`.

## 14:14 - Configurazione sandbox/approval

- Segnale testuale: scelta esplicita del livello di approvazione e sandbox.
- Segnale visivo: slide "Codex Approval and Sandbox Settings".
- Applicazione nel repo:
  - policy di esecuzione dichiarate nelle istruzioni operative,
  - enfasi su check prima dei cambi branch/PR.

## 16:26 - Prompting consistente

- Segnale testuale: prompt strutturati e ripetibili.
- Segnale visivo: esempi pratici di prompt in editor.
- Applicazione nel repo:
  - prompt templates in `AGENTS.md` e `README.md`,
  - formato risposta agente standardizzato.

## 27:02 - CLI/IDE tips

- Segnale testuale: usare prompt file, flussi rapidi e ripetibili.
- Segnale visivo: editor con prompt markdown (`add-tests.md`).
- Applicazione nel repo:
  - checklists nel PR template,
  - script `preflight` per routine pre-PR.

## 34:59 - MCP

- Segnale testuale: estendere contesto tramite strumenti esterni.
- Segnale visivo: slide MCP con esempi (Figma/Jira/Datadog/Statsig).
- Applicazione nel repo (stato):
  - base pronta (processo documentato),
  - integrazione MCP specifica del team da definire in step successivo.

## 46:50 - Advanced workflows

- Segnale testuale: headless/SDK e task paralleli.
- Segnale visivo: introduzione use case avanzati.
- Applicazione nel repo:
  - separazione clone/branch per parallelismo sicuro,
  - runbook anti-conflitto in `README.md`.

## 52:02 - Risorse e aggiornamenti continui

- Segnale testuale: docs/cookbook/changelog come fonte continua.
- Segnale visivo: slide risorse finali.
- Applicazione nel repo:
  - onboarding orientato a miglioramenti incrementali e commit piccoli.

## Prossimi step consigliati

1. Consolidare PR di onboarding/processo (`chore/codex-onboarding-from-video`).
2. Aprire una task applicativa reale su `fix/...` o `feature/...` usando i template prompt.
3. Eventuale estensione MCP in base agli strumenti reali del team.
