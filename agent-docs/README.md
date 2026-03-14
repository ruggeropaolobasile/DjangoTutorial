# Onboarding Index

Percorso consigliato (in ordine):

1. [`00-video-logical-map.md`](00-video-logical-map.md)
2. [`01-branch-and-clone-strategy.md`](01-branch-and-clone-strategy.md)
3. [`02-agents-hierarchy.md`](02-agents-hierarchy.md)
4. [`03-pr-ci-process.md`](03-pr-ci-process.md)
5. [`04-preflight-and-safe-switch.md`](04-preflight-and-safe-switch.md)
6. [`05-mcp-github-starter.md`](05-mcp-github-starter.md)
7. [`06-video-step-04-17-to-08-12.md`](06-video-step-04-17-to-08-12.md)
8. [`07-unlock-agentic-loops.md`](07-unlock-agentic-loops.md)
9. [`08-real-mistakes-and-gotchas.md`](08-real-mistakes-and-gotchas.md)
10. [`09-task-specific-playbooks.md`](09-task-specific-playbooks.md)
11. [`PLANS.md`](PLANS.md)
12. [`execplan-template.md`](execplan-template.md)
13. [`10-codex-config-and-profiles.md`](10-codex-config-and-profiles.md)
14. [`11-prompting-best-practices.md`](11-prompting-best-practices.md)
15. [`12-session-lock.md`](12-session-lock.md)
16. [`13-project-backlog-flow.md`](13-project-backlog-flow.md)

## Checklist rapida (done)

- [ ] Sto lavorando nel clone corretto (`DjangoTutorial` vs `DjangoTutorial-ui`)
- [ ] Branch corretto e working tree pulito prima dello switch
- [ ] Ho identificato quale `AGENTS.md` si applica (root/polls/settings)
- [ ] Ho eseguito `preflight` o check equivalenti
- [ ] PR template compilato (Agent Context + checklist tecnica)

## Nota operativa

Il file `__sync_test.txt` e usato solo come marker manuale di sincronizzazione chat.
Non includerlo nei commit standard.

## Backlog canonico

Per la sequenza dei task, il backlog canonico del workspace e il GitHub Project dell'utente:

- `https://github.com/users/ruggeropaolobasile/projects/1`

Regola di selezione:

- una sessione usa un solo clone e un solo backlog canonico
- per `DjangoTutorial`, il Project sopra e la coda principale salvo playbook piu specifici
- `agent-docs/13-project-backlog-flow.md` definisce come scegliere il prossimo item

## Handoff utile

- `agent-docs/issues/video-session-handoff.md`: stato minimo per riaprire una nuova sessione sul clone video corretto.
