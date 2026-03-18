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
- `autonomous`: `approval_policy = "never"` con sandbox ancora `workspace-write`.

## Uso pratico

- Sessione standard: `codex`
- Sessione con profilo: `codex -p fast`
- Sessione con profilo conservativo: `codex -p safe`
- Sessione autonoma: `codex -p autonomous`

## Nota Windows

Se su Windows `codex login status` o `codex exec` falliscono con `Accesso negato. (os error 5)`, verifica la sezione `[windows]` nel tuo `config.toml` locale.

Configurazione che puo creare problemi in alcuni ambienti:

```toml
[windows]
sandbox = "elevated"
```

Fallback consigliato:

```toml
[windows]
sandbox = "unelevated"
```

Su Windows il valore di `windows.sandbox` e distinto dal `sandbox_mode` generale e accetta solo varianti Windows-specifiche.

## Quando usare `never`

`never` accelera molto il flusso, ma non avrai richieste di conferma.
Usalo solo quando il contesto e ben delimitato e con branch dedicato.
Per minimizzare rischio, abbinalo a `workspace-write` e non a `danger-full-access`.

## Nota importante

Il file `config.toml` e personale/locale.
Nel repository teniamo solo esempi (`*.example.toml`) per evitare leak e differenze non tracciabili tra ambienti.
