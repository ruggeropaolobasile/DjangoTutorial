# AGENTS.md (settings)

Istruzioni specifiche per modifiche in `mysite/mysite/settings/`.

## Obiettivo area

Questa cartella governa configurazione runtime locale e produzione.
Le modifiche qui hanno impatto alto su sicurezza, deploy e avvio applicazione.

## Regole locali

- `base.py` e la fonte principale; `local.py` e `production.py` devono restare override minimi.
- Non introdurre segreti hardcoded nei file.
- Qualsiasi nuova variabile ambiente deve essere:
  - letta con fallback esplicito;
  - documentata in `README.md` se rilevante per deploy o sviluppo.
- Se modifichi sicurezza/proxy/cookie/host, verificare sempre anche il path produzione (`DJANGO_ENV=production`).
- Mantenere compatibilita con Render/Railway (`PUBLIC_DOMAIN`, `RENDER_EXTERNAL_HOSTNAME`, `RAILWAY_PUBLIC_DOMAIN`).

## Check minimi per task su settings

Da `mysite/` con virtualenv attivo:

```bash
python manage.py check
DJANGO_ENV=production DEBUG=False SECRET_KEY=prod-check-key PUBLIC_DOMAIN=example.com python manage.py check --deploy
```

## Criterio di completezza

Una modifica in `settings` e completa quando:

1. l'app avvia in locale senza regressioni;
2. `check --deploy` non introduce nuove criticita inattese;
3. README e/o note operative sono aggiornate se cambia la configurazione richiesta.
