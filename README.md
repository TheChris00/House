# House

Progetto di ristrutturazione della casa: planimetria dell'appartamento e camera di Christian e Gabriele.

Il sito è il file `index.html`. Contiene:

- la planimetria in scala della casa com'è oggi e dopo i lavori, con un'animazione che passa dall'una all'altra, le misure di tutte le stanze e le piante di camera di Alessia, camera da letto, bagno, corridoio e ingresso;
- il salotto com'è oggi: pianta con le misure e modello 3D della scansione (`soggiorno-scansione.glb`);
- la cucina com'è oggi: pianta con le misure, criticità e viste dalla scansione;
- l'open space cucina-salotto: dodici disposizioni, tre dei genitori con penisola, tre solo con isola e sei alternative, con pianta, luci e prese, mensole, modello 3D, luce del sole e confronto; nel 3D si sceglie il pavimento (grès effetto rovere, parquet o il marmo di oggi);
- tre disposizioni della camera, ognuna con modello 3D (con il pavimento da scegliere), impianto elettrico, luce del giorno, stile e colori, mobili e cose da fare.

Il file `budget.html` è la pagina del budget, divisa per mestiere (muratore, idraulico, elettricista, tecnico): stime, grafici, confronto dei preventivi a parità di lavori e quale conviene per ogni voce. I preventivi si aggiungono nella lista `PREVENTIVI`: basta darli a Claude, che segue la procedura in `.claude/skills/preventivi`. Gli originali (foto, PDF) vanno nella cartella `Preventivi`, che resta solo sul computer.

Il file `materiali.html` è la scheda dei materiali: superfici di tutta la casa e, per ogni pavimento, confezioni e prezzo, con il file `materiali.xlsx` da scaricare. Pagina e Excel si generano insieme con `python3 materiali.py` (serve openpyxl): prodotti e prezzi si cambiano lì.

Il file `bagno.html` è una pagina a parte con la proposta per il bagno: due layout, le posizioni possibili per un bagno di servizio e i modelli 3D. È una proposta ancora da decidere.

Il file `clima.html` è la proposta per i climatizzatori: dove mettere i quattro split e i due motori esterni, il percorso dei tubi, le potenze e cosa predisporre durante i lavori. Anche questa è da decidere.

Sito online: https://thechris00.github.io/House/

## Come si usa

In basso scegli la stanza; in alto, le schede mostrano una sezione alla volta. Tocca una pianta o una foto per aprirla a tutto schermo: pizzica, usa la rotella o tocca due volte per ingrandire, trascina per spostarti. Sul telefono i modelli 3D si esplorano a schermo intero, così la pagina scorre senza intoppi.

## Aggiornare il sito

1. Apri `index.html` nel repository e clicca sull'icona della matita, oppure su **Add file → Upload files**.
2. Carica il nuovo `index.html` (e, se cambiano, i modelli `.glb`) e clicca **Commit changes**.
3. Dopo uno o due minuti il sito online è aggiornato.

## Web app

Dal telefono il sito si può aggiungere alla schermata Home e aprire come un'app. Servono anche questi file nel repository, nella stessa cartella di `index.html`: `manifest.webmanifest`, `sw.js`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`.

`sw.js` tiene una copia del sito per usarlo senza rete. La pagina si aggiorna da sola appena c'è connessione; se cambi `sw.js` o le icone, cambia anche il valore di `CACHE` in cima a `sw.js` (per esempio da `casa-v1` a `casa-v2`).

Le cose da fare spuntate restano salvate solo sul dispositivo su cui le hai spuntate.

Le misure vengono da un rilievo a mano e dalle scansioni 3D di tutte le stanze (cartella `Mappature 3d Casa nonna`): vanno ricontrollate col metro prima di ordinare mobili su misura.
