---
name: preventivi
description: Inserisce nel sito un preventivo dei lavori di casa e lo confronta con gli altri. Usala ogni volta che l'utente manda o nomina un preventivo, un'offerta, un computo o un prezzo di una ditta (testo, foto, PDF, file nella cartella Preventivi), o chiede quale preventivo conviene.
---

# Preventivi della casa

I preventivi vivono in `budget.html`, nella lista `PREVENTIVI`. La pagina calcola da sola grafici, tabella, confronti e la sezione "Quale conviene": il lavoro è leggere bene il preventivo e scriverlo nei campi giusti.

## Procedura per ogni preventivo

1. **Leggi tutto il documento.** Se è una foto o un PDF, salva l'originale in `Preventivi/` con nome `AAAA-MM-GG ditta.ext` (la cartella non va su GitHub).
2. **Metti gli importi nelle voci di `VOCI`, che sono per mestiere:** `muratore`, `idraulico`, `elettricista`, `pratiche` (tecnico). L'utente ragiona così: ogni preventivo è di un artigiano. Un'impresa che fa più mestieri va divisa sulle voci; se non dà il dettaglio, dividi in modo ragionevole, scrivilo in `note` e chiedi il dettaglio in `controlla`. Se arriva un lavoro di un altro mestiere (imbianchino, cucina, serramenti), aggiungi una voce a `VOCI` con una stima indicativa e dillo all'utente. In `comprende` elenca i lavori del preventivo (muro salotto, porta cucina, pavimenti...) così si vede se due muratori coprono le stesse cose.
3. **IVA:** `ivaInclusa: true` se gli importi la comprendono, altrimenti `false` con `iva` (10 per ristrutturazioni, 22 per mobili e forniture). Mai indovinare: se non è scritto, mettilo in `controlla`.
4. **Confronto a parità:** confronta con gli altri preventivi sulle stesse voci. Se questo esclude qualcosa che un altro comprende (smaltimento, materiali, ponteggi, pratiche, certificazioni, posa), aggiungi in `extra` il costo stimato IVA inclusa. Vale anche all'indietro: se il nuovo comprende qualcosa che i vecchi escludevano, aggiorna gli `extra` dei vecchi.
5. **Scrivi `giudizio`** (2–3 frasi: prezzo rispetto a stima e altri, completezza, punti deboli) e **`controlla`** (domande concrete da fare alla ditta). Aggiorna anche i giudizi dei vecchi preventivi se il confronto cambia.
6. **Stato:** `ricevuto` di default; `scelto` o `scartato` solo se l'utente lo dice.
7. **Controlla la pagina** nel browser: si apre senza errori, i punti stanno nelle voci giuste.
8. **Rispondi in chat** con: cosa hai inserito, il totale a parità, quale conviene per ogni voce toccata e perché, le domande da fare alla ditta. Poi chiedi se fare commit e push.

## Attenzione

- Il sito è pubblico (GitHub Pages): nel file metti solo nome della ditta e cifre, mai indirizzi, telefoni, codici fiscali o dati personali.
- Il più basso non è sempre il migliore: segnala prezzi molto sotto la stima, preventivi vaghi ("a corpo" senza dettaglio), anticipi alti, tempi non indicati.
- Le stime in `VOCI` sono indicative: correggile se più preventivi seri cadono tutti fuori dalla fascia, e dillo.
