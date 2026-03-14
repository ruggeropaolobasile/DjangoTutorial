# 09 - Task-specific Playbooks

Obiettivo: evitare un `AGENTS.md` monolitico e guidare l'agente con istruzioni mirate per tipo di task.

## Regola

- Regole globali e invarianti in `AGENTS.md`.
- Passi dettagliati per singolo tipo di task in file dedicati sotto `agent-docs/playbooks/`.
- Quando apri issue/PR o dai un prompt operativo, cita il playbook applicabile.

## Playbook disponibili

- Feature: `agent-docs/playbooks/feature.md`
- Bugfix: `agent-docs/playbooks/bugfix.md`
- Code review: `agent-docs/playbooks/review.md`

## Come usarli in pratica

Prompt breve consigliato:

```text
Segui AGENTS.md + agent-docs/playbooks/<tipo>.md.
Obiettivo: <...>
Contesto: <...>
Vincoli: <...>
Validazione: <...>
```

Questo mantiene alta la precisione: poche regole globali + istruzioni contestuali.

