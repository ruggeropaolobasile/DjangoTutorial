# [TASK] Sessioni Codex agganciate al workspace sbagliato

## Obiettivo
Evitare che una chat Codex operi sul clone/repo sbagliato rispetto alla finestra VS Code visibile, causando cambi branch o modifiche su una working copy diversa da quella attesa.

## Contesto
- Area/file: configurazione locale Codex, onboarding operativo, procedure di verifica workspace.
- Problema attuale: una sessione aperta in una finestra che mostra `DjangoTutorial-ui` puo risultare ancora agganciata a `C:\repo\DjangoTutorial`, mentre il terminale integrato e l'Explorer mostrano un'altra cartella. Questo genera confusione su branch, file toccati e repo effettivo.

## Vincoli
- Non assumere che terminale integrato, Explorer e sessione agente puntino sempre alla stessa root.
- Introdurre controlli leggeri e ripetibili prima di eseguire modifiche o switch di branch.

## Criteri di accettazione
- [ ] Esiste una procedura standard per verificare root repo, branch e ruolo del clone all'inizio di ogni task.
- [ ] La documentazione chiarisce la differenza tra workspace VS Code, terminale corrente e root reale della sessione agente.
- [ ] Esiste almeno un comando/check semplice per identificare subito `repo`, `branch` e `role`.
- [ ] Le istruzioni spiegano come lavorare in parallelo con clone separati senza collisioni.

## Validazione
- [ ] Verificare su due clone distinti che il controllo mostri valori diversi per root/branch/role.
- [ ] Verificare che la documentazione indichi come riaprire la chat dalla cartella corretta.
- [ ] Verificare che il flusso non richieda modifiche a file generati o a database locali.

## Branch suggerito
- `fix/workspace-chat-mismatch`

## Passi per riprodurre
1. Aprire due finestre VS Code su clone diversi, ad esempio `C:\repo\DjangoTutorial` e `C:\repo\DjangoTutorial-ui`.
2. Avviare o riutilizzare sessioni Codex nelle due finestre.
3. Osservare che una sessione puo continuare a operare sulla root precedente anche se la UI della finestra mostra l'altro clone.
4. Eseguire i check Git e confrontare root reale, branch e stato della working tree.

## Impatto
- Rischio di modificare il repo sbagliato.
- Rischio di cambiare branch in una working copy diversa da quella prevista.
- Rischio di messaggi fuorvianti su stato del progetto e verifiche.

## Fix proposto
- Documentare un preflight obbligatorio di workspace all'inizio del task.
- Mantenere clone separati con ruolo esplicito (`video`, `ui`) e un controllo rapido di identita repo.
- Aggiornare onboarding/playbook con esempi concreti per distinguere sessione agente e terminale integrato.
