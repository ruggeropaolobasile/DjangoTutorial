# Video Session Handoff

Scopo: permettere a una nuova sessione Codex di riprendere il lavoro sul video senza dipendere dalla memoria della chat precedente.

## Stato corretto da usare

- Clone corretto per il lavoro video: `C:\repo\DjangoTutorial-video`
- Branch corretto: `chore/codex-onboarding-from-video`
- Ultimo commit noto nel clone video: `e35953a`

## Stato della sessione che si sta chiudendo

- Questa sessione e agganciata a `C:\repo\DjangoTutorial`, non al clone video.
- Il lavoro rilevante per il video e stato gia trasferito nel clone dedicato `DjangoTutorial-video`.
- Per continuare il flusso video non usare questa sessione.

## Dove siamo nel video

- Ultimo timestamp discusso: `19:56`
- Tema corrente: starter tasks e prompting practices
- Prossimo blocco naturale: continuare da `20:00+`

## Documenti da leggere nella nuova sessione

- `AGENTS.md`
- `agent-docs/README.md`
- `agent-docs/10-codex-config-and-profiles.md`
- `agent-docs/11-prompting-best-practices.md`
- `agent-docs/issues/workspace-chat-mismatch.md`

## Prompt consigliato per la nuova sessione

```text
Conferma reale della sessione: repo root, branch, head, status.
Stiamo seguendo il video sul branch chore/codex-onboarding-from-video.
Riprendiamo dal timestamp 19:56 / 20:00 e continuiamo passo passo.
Leggi anche AGENTS.md, agent-docs/README.md e agent-docs/issues/workspace-chat-mismatch.md.
```

## Regola operativa

Se la nuova sessione non risponde con:

- repo root `C:/repo/DjangoTutorial-video`
- branch `chore/codex-onboarding-from-video`

allora non e agganciata al clone corretto e va riaperta dalla cartella giusta.
