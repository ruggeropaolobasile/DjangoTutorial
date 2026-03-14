# AGENTS.md (polls)

Istruzioni specifiche per modifiche dentro `mysite/polls/`.

## Obiettivo area

`polls` contiene logica applicativa, URL, template e admin della demo Django.

## Regole locali

- Preferire view class-based gia presenti (`IndexView`, `DetailView`, `ResultsView`) salvo motivazione chiara.
- Mantenere coerenza URL names (`polls:index`, `polls:detail`, `polls:results`, `polls:vote`).
- Se tocchi `models.py`, valutare sempre:
  - migration necessaria
  - impatto su admin (`admin.py`)
  - impatto su test (`tests.py`)
- Se tocchi `views.py`, aggiornare o aggiungere test di comportamento in `tests.py`.
- Evitare query non filtrate su contenuti futuri: rispettare la logica `pub_date__lte=timezone.now()` dove applicabile.

## Check minimi per task su polls

Da `mysite/` con virtualenv attivo:

```bash
python manage.py check
python manage.py test polls
ruff check polls
```

## Criterio di completezza

Una modifica in `polls` e completa quando:

1. comportamento richiesto verificato via test o caso manuale esplicito;
2. template e view restano allineati (niente URL/name rotti);
3. admin continua a caricare senza errori.
