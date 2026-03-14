# 10 - Codex config.toml e profili

Obiettivo: configurare default ripetibili per le sessioni Codex, oltre a `AGENTS.md`.

## Cosa controlla `config.toml`

`AGENTS.md` guida il comportamento nel repository.
`config.toml` imposta i default della sessione CLI (modello, effort, sandbox, approval, feature toggle, profili).

## File di esempio nel repo

- `agent-docs/examples/codex-config.example.toml`

Usalo come base locale, poi personalizza in base al tuo livello di rischio/velocita.

## Profili consigliati

- `fast`: risposte rapide, costo/latency minori, controlli piu leggeri.
- `balanced`: profilo predefinito consigliato per lavoro quotidiano.
- `safe`: piu conservativo, sandbox restrittiva e policy severa.

## Uso pratico

- Sessione standard: `codex`
- Sessione con profilo: `codex -p fast`
- Sessione con profilo conservativo: `codex -p safe`

## Nota importante

Il file `config.toml` e personale/locale.
Nel repository teniamo solo esempi (`*.example.toml`) per evitare leak e differenze non tracciabili tra ambienti.
