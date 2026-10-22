# moonraker.conf nelle cartelle delle stampanti

Ogni cartella di questo repo (`G1-0038-25/`, `G1-TEMPLATE/`, …) contiene un `moonraker.conf`. Il file esiste in **due formati**, e quello sbagliato per una stampante le blocca Moonraker. Questo documento spiega perché e cosa fare quando si rifà la SD di una stampante.

## Come arriva il file sulla stampante

1. Si flasha la SD con un'immagine G1OS. In `~/printer_data/config/moonraker.conf` c'è il file dell'immagine (dal template `Configs/moonraker.conf` di [G1-Configs](https://github.com/gingeradditive/G1-Configs)).
2. Nella pagina INIT di g1-flask si inserisce il numero di serie, per esempio `G1-0038-25`.
3. g1-flask confronta, per ogni file della cartella `G1-0038-25/` su `main`, lo SHA dell'ultimo commit che lo ha modificato con quello salvato in `~/printer_data/database/G1.Conf`. Dopo l'INIT non c'è nessuno SHA salvato, quindi tutti i file risultano da aggiornare e nel menu di Mainsail compare **UPDATE G1**.
4. UPDATE G1 scarica i file della cartella e **sostituisce** quelli in `~/printer_data/config/`, compreso `moonraker.conf`.

Conseguenze:
- dopo il primo UPDATE G1 ogni stampante usa il `moonraker.conf` di questo repo, non quello dell'immagine;
- ogni stampante scarica **solo la cartella del proprio numero di serie**: modificare `G1-0038-25/moonraker.conf` riguarda solo G1-0038-25;
- ogni commit che tocca il file di una cartella fa comparire UPDATE G1 su quella stampante;
- il factory reset cancella i file scaricati (compreso `moonraker.conf`), che tornano con l'UPDATE G1 successivo.

## I due formati

L'unica differenza è la sezione di crowsnest (la webcam).

**Formato vecchio**: sezione scritta nel file, senza `primary_branch`:
```ini
[update_manager crowsnest]
type: git_repo
path: ~/crowsnest
origin: https://github.com/mainsail-crew/crowsnest.git
managed_services: crowsnest
is_system_service: True
```

**Formato nuovo**: la sezione viene da un file creato dall'immagine G1OS:
```ini
[include moonraker-crowsnest.conf]
```

Il formato nuovo corregge il bug B26 di G1OS: crowsnest tiene un branch per ogni versione maggiore (`master` = v4, `v5`, in futuro `v6`…). Senza `primary_branch` Moonraker si aspetta `master`, mentre le immagini recenti installano v5; Mainsail propone un Recover che installa la v4 e il servizio crowsnest non parte più. Le immagini G1OS nuove copiano in `moonraker-crowsnest.conf` la sezione fornita da crowsnest stesso, con il branch giusto per la versione installata.

Il formato nuovo è il `Configs/moonraker.conf` di G1-Configs copiato così com'è: per creare o aggiornare un file nel formato nuovo si copia quel template (o `G1-TEMPLATE/moonraker.conf`, che è uguale).

## La regola

> Il formato nuovo va **solo** nella cartella di una stampante che ha già la SD con un'immagine G1OS che crea `moonraker-crowsnest.conf`.

Sulle immagini vecchie (3.0.1 e precedenti) quel file non esiste. Se una di queste stampanti riceve il formato nuovo, Moonraker non parte (`No files matching include directive [include moonraker-crowsnest.conf]`): Mainsail non si collega, non si possono usare UPDATE G1 né Recover, e si recupera solo via SSH.

L'errore opposto è innocuo: una stampante con l'immagine nuova che riceve il formato vecchio funziona, ma torna ad avere l'avviso di crowsnest e il Recover che lo rompe.

Per questo **non si convertono tutte le cartelle insieme**: ogni cartella si aggiorna quando si rifà la SD di quella stampante.

### Come capire quale immagine ha una stampante

Via SSH (`ssh pi@<ip>`):
```bash
ls ~/printer_data/config/moonraker-crowsnest.conf   # esiste → immagine nuova
cat /etc/g1os-release                                # es. "G1OS release 3.0.1 (trixie)"
```
Fa fede la presenza di `moonraker-crowsnest.conf`.

### Quali cartelle sono già nel formato nuovo

```bash
grep -l "include moonraker-crowsnest.conf" */moonraker.conf
```

## Procedura: rifare la SD di una stampante

1. Flashare la SD con l'immagine G1OS nuova e avviare la stampante.
2. Controllare che esista `~/printer_data/config/moonraker-crowsnest.conf` (vedi sopra). Se manca, **fermarsi**: l'immagine è vecchia.
3. Fare INIT con il numero di serie della stampante.
4. In questo repo copiare `G1-TEMPLATE/moonraker.conf` sopra `<SERIALE>/moonraker.conf`, solo per quella cartella, e fare commit e push su `main`:
   ```bash
   cp G1-TEMPLATE/moonraker.conf G1-0038-25/moonraker.conf
   git add G1-0038-25/moonraker.conf
   git commit -m "moonraker: G1-0038-25 to the new format (SD reflashed with G1OS <versione>)"
   git push
   ```
   I passi 3 e 4 si possono invertire: conta che il formato nuovo arrivi dopo il flash.
5. Nella pagina di g1-flask premere UPDATE G1, poi riavviare Moonraker (o la stampante).
6. Verificare: Mainsail si collega, nessun avviso su crowsnest nell'Update Manager, `git -C ~/crowsnest branch --show-current` risponde col branch di default di crowsnest (oggi `v5`).

## Stampanti nuove

`addnewmachine.py` copia `G1-TEMPLATE`, quindi le cartelle nuove nascono nel formato nuovo. Una stampante nuova va flashata **solo** con un'immagine nuova: una SD vecchia rimasta in magazzino le bloccherebbe Moonraker al primo UPDATE G1.

## Se una stampante si è bloccata

Sintomo: dopo UPDATE G1 Mainsail non si collega a Moonraker, e `journalctl -u moonraker` riporta `No files matching include directive`.

Via SSH:
```bash
cp ~/crowsnest/resources/moonraker_update.txt ~/printer_data/config/moonraker-crowsnest.conf
sudo systemctl restart moonraker
```
Il file viene dalla versione di crowsnest installata, quindi ha il branch giusto per quella stampante. Poi rimettere il formato vecchio nella sua cartella in questo repo, finché la SD non viene rifatta con un'immagine nuova; altrimenti il problema si ripresenta al factory reset successivo.

## Riferimenti

- G1OS, `docs/known-issues.md`: B26 (crowsnest) e i bug correlati.
- G1OS `modules/generic/53-crowsnest`: crea `moonraker-crowsnest.conf`.
- G1-Configs `Flask/scripts/checkforupdate_script.py` e `update_script.py`: UPDATE G1.
