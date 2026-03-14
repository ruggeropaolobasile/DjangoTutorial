Progetto di test tutorial Django

## Prossimo passo (adesso)

Per andare online subito, fai questo:
Non aspettiamo altre modifiche codice: manca solo il deploy dalla dashboard del provider.


1. Apri Render e crea un servizio con **New > Blueprint**.
2. Seleziona questo repository GitHub.
3. Conferma la creazione delle risorse dal file `render.yaml`.
4. Attendi il deploy e apri `https://<tuo-dominio>.onrender.com/healthz/`.
5. Se `healthz` è OK, verifica anche `/`, `/polls/` e `/admin/`.

Se non usi Render, puoi seguire la sezione “Deploy online (PaaS generica)” qui sotto con le stesse variabili d'ambiente.

## Configurazione push su GitHub

Se hai già il repository su GitHub, configura il remote `origin` e fai push del branch corrente:

```bash
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/ruggeropaolobasile/DjangoTutorial.git
git push -u origin work
```

Se vuoi pubblicare il branch `work` direttamente come `main`:

```bash
git push -u origin work:main
```

## Deploy online senza VPN (consigliato: Render free)

Se Railway non è disponibile, puoi pubblicare gratis su **Render**. Non serve VPN:
Render espone direttamente un dominio pubblico (`*.onrender.com`).

### Deploy rapido su Render

1. Fai fork/push del repository su GitHub.
2. Vai su Render > **New** > **Blueprint**.
3. Seleziona il repository e conferma: Render userà `render.yaml` già presente.
4. Attendi il primo deploy.
5. Verifica gli endpoint:
   - `https://<tuo-dominio>.onrender.com/healthz/`
   - `https://<tuo-dominio>.onrender.com/`
   - `https://<tuo-dominio>.onrender.com/polls/`
   - `https://<tuo-dominio>.onrender.com/admin/`

## Deploy online (PaaS generica)

Puoi deployare su qualsiasi piattaforma che supporti Python + variabili d'ambiente
(es. Render, Fly.io, Railway, VPS personale).

### Variabili d'ambiente da configurare

- `SECRET_KEY`: obbligatoria in produzione.
- `DEBUG=False`
- `ALLOWED_HOSTS=<tuo-dominio-pubblico>` (es. `example.com`)
  - Se `DEBUG=False`, devi impostare `ALLOWED_HOSTS` oppure `PUBLIC_DOMAIN` (fail-fast all'avvio se mancano).
- `CSRF_TRUSTED_ORIGINS=https://<tuo-dominio-pubblico>`
- `PUBLIC_DOMAIN` (opzionale ma consigliata: accetta sia `example.com` sia `https://example.com/`; viene aggiunta automaticamente a `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`)
- `DATABASE_URL=<connection-string-postgres>` (consigliata in produzione; in locale resta SQLite di default)
- (opzionale) `SECURE_SSL_REDIRECT=True`

Note compatibilità:
- `RENDER_EXTERNAL_HOSTNAME` è supportata automaticamente.
- Per retrocompatibilità è supportata anche `RAILWAY_PUBLIC_DOMAIN`.

### Startup del servizio

In repository è presente un esempio Railway (`railway.json`) con:

1. `python manage.py migrate`
2. `python manage.py collectstatic --noinput`
3. `gunicorn mysite.wsgi --bind 0.0.0.0:$PORT`

> Nota: questi comandi vengono eseguiti nella cartella `mysite/` tramite `cd mysite && ...` nel `startCommand`.

### Verifica finale

Dopo il deploy controlla:

- `https://<tuo-dominio>/healthz/`
- `https://<tuo-dominio>/`
- `https://<tuo-dominio>/polls/`
- `https://<tuo-dominio>/admin/`

`/healthz/` restituisce `200` con `{"status": "ok"}` quando app e DB sono raggiungibili; restituisce `503` se il database non è disponibile.
