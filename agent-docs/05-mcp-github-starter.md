# MCP Starter (GitHub)

Obiettivo: aggiungere un MCP utile al tuo flusso issue/PR senza complicare il progetto.

## Cosa abilita

- Lettura rapida di issue/PR dal contesto agente.
- Supporto a review e task planning con contesto GitHub reale.

## Principi di sicurezza

- Non committare token o segreti nel repository.
- Tenere la configurazione MCP in file locale utente (non versionato).
- Preferire server MCP ufficiali e versioni pin/controllate.

## Configurazione consigliata

1. Crea un token GitHub con scope minimi necessari (repo/PR/issue in base al tuo uso).
2. Esporta il token in env var locale (`GITHUB_TOKEN`).
3. Usa il template in `agent-docs/examples/codex-mcp-github.example.toml`.

## Nota pratica

Per questo progetto l'MCP GitHub e opzionale: il flusso base resta funzionante anche senza MCP.

