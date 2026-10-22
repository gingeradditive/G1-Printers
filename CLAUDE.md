# G1-Printers

Configurazioni per numero di serie delle stampanti Ginger G1: una cartella per stampante (`G1-0038-25/`, …) con `printer.cfg`, `kamp.cfg`, `moonraker.conf`, più `G1-TEMPLATE/`, copiato da `addnewmachine.py` per le stampanti nuove (vedi [README.md](README.md)). Ogni stampante scarica i file della propria cartella dal branch `main` con UPDATE G1 (app g1-flask di G1-Configs).

Prima di modificare un `moonraker.conf`, o quando si rifà la SD di una stampante, leggere [MOONRAKER.md](MOONRAKER.md). In breve:
- esistono due formati, e il formato nuovo (`[include moonraker-crowsnest.conf]`) blocca Moonraker sulle stampanti con un'immagine G1OS vecchia;
- convertire una cartella al formato nuovo solo dopo aver flashato quella stampante con l'immagine nuova, e mai tutte le cartelle insieme;
- un commit su `main` arriva alle stampanti al primo UPDATE G1: controllare quali cartelle tocca.
