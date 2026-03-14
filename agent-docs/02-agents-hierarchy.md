# AGENTS Hierarchy

Obiettivo: dare contesto giusto all'agente in base all'area modificata.

## Gerarchia attuale

- Root: `AGENTS.md` (regole globali repo)
- App: `mysite/polls/AGENTS.md` (logica applicativa)
- Settings: `mysite/mysite/settings/AGENTS.md` (config/deploy)

## Regola di precedenza

Vale sempre la regola piu specifica rispetto ai file toccati.

## Uso pratico

- Se tocchi `polls/*`: segui root + `polls/AGENTS.md`
- Se tocchi `settings/*`: segui root + `settings/AGENTS.md`
- Se tocchi solo docs/processo: root `AGENTS.md` e sufficiente
