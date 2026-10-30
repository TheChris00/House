# House

Progetto di ristrutturazione della casa: planimetria dell'appartamento e camera di Christian e Gabriele.

Il sito è il file `index.html`. Contiene:

- la planimetria della casa e della camera, con le misure;
- il soggiorno com'è oggi: pianta con le misure e modello 3D della scansione (`soggiorno-scansione.glb`);
- la cucina com'è oggi: pianta con le misure, criticità e viste dalla scansione;
- tre disposizioni della camera, ognuna con modello 3D, impianto elettrico, luce del giorno, stile e colori, mobili e cose da fare.

Sito online: https://thechris00.github.io/House/

## Come si usa

Tocca una pianta o una foto per aprirla a tutto schermo: pizzica, usa la rotella o tocca due volte per ingrandire, trascina per spostarti. Sul telefono i modelli 3D si esplorano a schermo intero, così la pagina scorre senza intoppi.

## Aggiornare il sito

1. Apri `index.html` nel repository e clicca sull'icona della matita, oppure su **Add file → Upload files**.
2. Carica il nuovo `index.html` (e, se cambiano, i modelli `.glb`) e clicca **Commit changes**.
3. Dopo uno o due minuti il sito online è aggiornato.

## Web app

Dal telefono il sito si può aggiungere alla schermata Home e aprire come un'app. Servono anche questi file nel repository, nella stessa cartella di `index.html`: `manifest.webmanifest`, `sw.js`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`.

`sw.js` tiene una copia del sito per usarlo senza rete. La pagina si aggiorna da sola appena c'è connessione; se cambi `sw.js` o le icone, cambia anche il valore di `CACHE` in cima a `sw.js` (per esempio da `casa-v1` a `casa-v2`).

Le cose da fare spuntate restano salvate solo sul dispositivo su cui le hai spuntate.

Le misure vengono da un rilievo a mano e da una scansione 3D: vanno ricontrollate col metro prima di ordinare mobili su misura.
