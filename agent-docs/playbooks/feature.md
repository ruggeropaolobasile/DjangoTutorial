# Playbook - Feature

## Input minimo

- Obiettivo funzionale.
- Area/file coinvolti.
- Vincoli di compatibilita.

## Flusso

1. Implementa modifica minima.
2. Aggiorna route/template solo se necessario.
3. Esegui loop di verifica (`check`, `test`, `ruff`).
4. Prepara PR con impatto e validazioni eseguite.

## Output atteso

- Elenco file toccati con motivazione.
- Comandi eseguiti con esito.
- Limiti/not done esplicitati.
