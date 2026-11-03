---
name: preventivi
description: Inserisce nel sito un preventivo dei lavori di casa e lo confronta con gli altri. Usala ogni volta che l'utente manda o nomina un preventivo, un'offerta, un computo o un prezzo di una ditta (testo, foto, PDF, file nella cartella Preventivi), o chiede quale preventivo conviene.
---

# Preventivi della casa

I preventivi vivono in `budget.html`, nella lista `PREVENTIVI`. La pagina calcola da sola grafici, tabella, confronti e la sezione "Quale conviene": il lavoro è leggere bene il preventivo e scriverlo nei campi giusti.

I preventivi che contano sono di **manodopera** (muratore, idraulico, elettricista), non di arredi o cucina. Il riferimento è il computo `LAVORI` in `budget.html`: ogni lavoro con quantità dalla pianta e prezzo unitario di manodopera; le stime di `VOCI` si calcolano da lì.

## Procedura per ogni preventivo

1. **Leggi tutto il documento.** Se è una foto o un PDF, salva l'originale in `Preventivi/` con nome `AAAA-MM-GG ditta.ext` (la cartella non va su GitHub).
2. **Metti gli importi nelle voci di `VOCI`, che sono per mestiere:** `muratore`, `idraulico`, `elettricista`. I muri da demolire non sono portanti e l'utente non vuole un tecnico: niente trave né voce per il tecnico. L'utente ragiona così: ogni preventivo è di un artigiano. Un'impresa che fa più mestieri va divisa sulle voci; se non dà il dettaglio, dividi in modo ragionevole, scrivilo in `note` e chiedi il dettaglio in `controlla`. Se arriva un lavoro di un altro mestiere (imbianchino, cucina, serramenti), aggiungi una voce a `VOCI` con una stima indicativa e dillo all'utente. In `comprende` elenca i lavori del preventivo (muro salotto, porta cucina, pavimenti...) così si vede se due muratori coprono le stesse cose.
3. **IVA:** `ivaInclusa: true` se gli importi la comprendono, altrimenti `false` con `iva` (10 per ristrutturazioni, 22 per mobili e forniture). Mai indovinare: se non è scritto, mettilo in `controlla`.
4. **Confronto a parità:** confronta con gli altri preventivi sulle stesse voci. Se questo esclude qualcosa che un altro comprende (smaltimento, materiali, ponteggi, pratiche, certificazioni, posa), aggiungi in `extra` il costo stimato IVA inclusa. Vale anche all'indietro: se il nuovo comprende qualcosa che i vecchi escludevano, aggiorna gli `extra` dei vecchi.
4b. **Confronto col computo:** per ogni lavoro di `LAVORI`, vedi se il preventivo lo comprende e con quale quantità. Se una ditta dà prezzi unitari, confrontali con quelli del computo; se più preventivi seri cadono fuori dalla fascia, correggi il prezzo in `LAVORI` e dillo. Se il preventivo comprende materiali di finitura (piastrelle, sanitari, prese), segnalalo: va confrontato togliendoli. Se c'è un lavoro che nel computo non esiste, aggiungilo.
5. **Scrivi `giudizio`** (2–3 frasi: prezzo rispetto a stima e altri, completezza, punti deboli) e **`controlla`** (domande concrete da fare alla ditta). Aggiorna anche i giudizi dei vecchi preventivi se il confronto cambia.
6. **Valutazione:** compila `valutazione` con i 10 criteri di `CRITERI` (`'ok'`, `'parziale'` o `'no'`, più una nota breve che dice perché). Le regole:
   - `dettaglio`: ogni lavoro con quantità e prezzo (computo metrico); un prezzo unico a corpo è `no`.
   - `materiali`: chiaro cosa è fornitura e posa e cosa solo posa (pavimenti, piastrelle, sanitari, porte, frutti).
   - `iva`: detto se è compresa e con quale aliquota.
   - `esclusioni`: smaltimento, massetti, ponteggi, dichiarazione di conformità, pulizia, assistenza muraria. Tutti compresi o esclusi esplicitamente: `ok`; alcuni: `parziale`.
   - `quantita`: mq, punti luce, metri scritti e coerenti con le misure della casa (pianta in `index.html`).
   - `tempi`: durata e data di inizio.
   - `pagamenti`: anticipo al massimo 20–30%, poi stati di avanzamento, saldo a lavori controllati. Anticipo più alto: `no`.
   - `garanzie`: validità del prezzo, lavori extra solo concordati per iscritto, assicurazione.
   - `prezzo`: dentro la stima e vicino agli altri preventivi a parità; molto sotto (oltre il 20%) o sopra: `parziale` o `no`. Quando arriva un nuovo preventivo, rivedi questo criterio anche per i vecchi.
   - `forma`: scritto, datato, dopo sopralluogo, con partita IVA.
   Il voto su 10 lo calcola la pagina. Nella risposta in chat riporta il voto e i punti mancanti come domande da fare alla ditta.
7. **Stato:** `ricevuto` di default; `scelto` o `scartato` solo se l'utente lo dice.
8. **Controlla la pagina** nel browser: si apre senza errori, i punti stanno nelle voci giuste.
9. **Rispondi in chat** con: cosa hai inserito, il voto, il totale a parità, quale conviene per ogni voce toccata e perché, le domande da fare alla ditta. Poi chiedi se fare commit e push.

## Attenzione

- Il sito è pubblico (GitHub Pages): nel file metti solo nome della ditta e cifre, mai indirizzi, telefoni, codici fiscali o dati personali.
- Il più basso non è sempre il migliore: segnala prezzi molto sotto la stima, preventivi vaghi ("a corpo" senza dettaglio), anticipi alti, tempi non indicati.
- Le stime in `VOCI` sono indicative: correggile se più preventivi seri cadono tutti fuori dalla fascia, e dillo.
