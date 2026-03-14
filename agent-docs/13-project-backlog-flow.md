# Project Backlog Flow

Questo playbook rende il GitHub Project la coda operativa della sessione, in modo che l'agente possa scegliere il prossimo task senza dipendere dalla chat.

## Source of truth

Per la sequenza dei task, la fonte canonica e il GitHub Project del repository.

I documenti in `agent-docs/` restano la fonte di dettaglio tecnico:

- use case
- test case
- ExecPlan
- boundary e recovery

In sintesi:

- GitHub Project dice `cosa viene dopo`
- `agent-docs/` dice `come lavorarlo`

## Required fields

Ogni item usato nel ciclo autonomo deve avere almeno:

- `Status`
- `Priority`
- `Size`

Campi consigliati quando servono:

- `Repository`
- `Target date`
- `Assignees`

## Status model

Stati minimi supportati:

- `Todo`
- `In progress`
- `Done`

Uso corretto:

- `Todo`: pronto per essere scelto
- `In progress`: task attualmente lavorato nella sessione
- `Done`: task completato e verificato

Se serve gestire blocchi, il team puo aggiungere in futuro uno stato esplicito `Blocked`. Fino a quel momento, un task bloccato resta in `Todo` ma il motivo deve essere scritto nel piano locale.

## Pick Next Item Rule

Quando la sessione ha chiuso un task e non esiste una stop condition reale, l'agente deve scegliere il prossimo item cosi:

1. filtrare gli item con `Status = Todo`
2. ordinare per `Priority` da piu alta a piu bassa (`P0`, `P1`, `P2`)
3. a parita di priority, preferire il `Size` piu piccolo (`XS`, `S`, `M`, `L`, `XL`)
4. tra item equivalenti, preferire quello che:
   - richiede meno file
   - richiede meno decisioni di prodotto
   - ha validation piu chiara

Se il primo item non e compatibile col boundary corrente:

1. registrare il motivo nel piano locale
2. saltare al successivo item `Todo`
3. non fermarsi se esiste ancora almeno un item compatibile

## Transition Rule

Quando l'agente inizia un task:

- spostare l'item a `In progress`

Quando l'agente chiude il loop `modifica -> verifica -> fix -> riverifica`:

- spostare l'item a `Done`

Quando l'agente scopre che il task richiede una decisione forte o un boundary non ancora chiarito:

- lasciare traccia del blocker nel piano locale
- passare al prossimo item `Todo` compatibile, se esiste

## Stop rule

La sessione non si ferma solo perche:

- ha chiuso un checkpoint
- ha finito una slice documentale
- ha chiuso un item piccolo

La sessione si ferma solo se:

- non esistono piu item `Todo`
- tutti gli item `Todo` sono incompatibili col boundary corrente
- si verifica una stop condition forte gia definita nei playbook o nel piano

## Recommended batch shape

Per mantenere la catena fluida, il Project non dovrebbe restare con zero `Todo`.

Target pratico:

- tenere sempre almeno `5` item `Todo`
- mantenere un mix di taglie:
  - 2 item `S`
  - 2 item `M`
  - 1 item `L` opzionale

## Relationship with session lock

Il backlog flow non sostituisce il `session lock`.

Prima di scegliere il prossimo item, la sessione deve sapere con certezza:

- quale clone e attivo
- quale branch e attivo
- quale HEAD e attivo
- quale working tree e attivo

Solo dopo si sceglie il prossimo item dal Project.
