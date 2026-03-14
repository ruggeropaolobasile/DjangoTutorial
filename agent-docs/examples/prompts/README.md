# Prompt Files

Questa cartella raccoglie prompt file task-specifici pronti da riusare.

Quando usare un prompt file:

- quando lo stesso task viene rilanciato piu volte;
- quando vuoi delegare lavoro a un altro clone o a una nuova sessione;
- quando vuoi evitare di ricostruire ogni volta contesto, vincoli e validazione.

Regola pratica di naming:

- usa nomi brevi e action-oriented;
- includi area e risultato atteso quando utile;
- evita nomi generici come `task.md` o `prompt.md`.

Flusso consigliato:

1. parti da `agent-docs/examples/prompt-starters.md` se stai ancora definendo il task;
2. quando il task diventa ripetibile, promuovilo a prompt file in questa cartella;
3. se il task cresce e richiede milestone o handoff complessi, promuovilo a ExecPlan.

Prompt file disponibili:

- `ui-vote-page-polish.md`
