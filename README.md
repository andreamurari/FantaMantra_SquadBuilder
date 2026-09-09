# Campetto Mantra

Tool per l'asta del Fantacalcio **Mantra**: un campetto interattivo per vedere come si sta
costruendo la rosa mentre l'asta va avanti.

**▶ [Apri il tool online](https://claude.ai/code/artifact/727c5d4a-a933-4586-bc1c-c6f8bc5d209c)** (usabile anche da telefono)

## Uso

Apri **`index.html`** con un doppio click (funziona offline, senza installare nulla), oppure
usa la [versione online](https://claude.ai/code/artifact/727c5d4a-a933-4586-bc1c-c6f8bc5d209c).

## Cosa fa

- **4 campetti affiancati**: per ognuno scegli uno degli 11 moduli Mantra di fantacalcio.it
  (3-4-3, 3-4-1-2, 3-4-2-1, 3-5-2, 3-5-1-1, 4-3-3, 4-3-1-2, 4-4-2, 4-1-4-1, 4-4-1-1, 4-2-3-1)
  e confronti come si dispone la stessa rosa nei diversi sistemi.
- **Solo ruolo esatto**: in uno slot puoi mettere solo giocatori che hanno quel ruolo Mantra.
  Niente adattamento. `⌫` svuota il campo.
- **Match ruolo**: un giocatore entra in uno slot **solo se il suo ruolo più difensivo
  coincide col ruolo più offensivo dello slot**.
  - lato **giocatore** conta il ruolo **più difensivo** (ordine
    `Por < Dc=B < Ds=Dd < M < E < C < T=W < A < Pc`): un `E/W` è una **E**, un `Dd/Dc` una **Dc**,
    un `M/C` una **M**;
  - lato **modulo** uno slot doppio conta come il ruolo **più offensivo**: `M/C`→C, `E/W`→W,
    `W/A`→A, `T/A`→A, `C/T`→T, `A/Pc`→Pc (`Dc/B` a pari livello valgono entrambi);
  - quindi un `E/W` non entra in uno slot `E/W` (che vale W) e finisce nei **Jolly**; entra
    invece in uno slot `E` puro. Con due `M/C` in un 3-4-2-1: uno titolare sulla `M`, l'altro
    riserva sulla `M`, lo slot `M/C` resta per una `C`.
  - Il pallino mostra il ruolo **completo** dello slot (`M/C`, `E/W`…); il colore è quello del
    ruolo principale del giocatore.
  - Sotto ogni campo la sezione **Jolly** mostra chi non ha nessun ruolo previsto dal modulo
    (es. una `E` in un 4-3-3). Il **circle-x** nasconde un giocatore da ogni campo (via da campo
    *e* Jolly, resta in rosa); la gomma *svuota campo* azzera campo e Jolly di quel campo. Il
    **circle-plus** lo rimette in campo, `⚡` ripristina tutto.
- Il pallino in campo prende il **colore del ruolo** come su fantacalcio.it: Por giallo,
  difensori verde, centrocampo azzurro, trequarti/ali viola, attacco rosso.
- **Listone 2026/27** integrato (dal file `Quotazioni_Fantacalcio_*.xlsx`): cerca e filtra per
  ruolo Mantra; quando aggiungi un acquisto ti viene chiesto il **prezzo pagato** (pre-compilato
  con la quotazione), poi comunque modificabile dalla rosa.
- In **Rosa**, ogni giocatore ha due tasti: `⊞` lo mette in ogni campo — nel primo slot libero
  compatibile come titolare, oppure come **riserva** (mostrata tra parentesi sotto il titolare)
  se non ci sono slot liberi; salta i campi senza nessuno slot per quel ruolo. `⊟` lo toglie da
  tutti i campi (titolare o riserva). Cambiando modulo, una riserva viene promossa se il titolare
  del suo slot non è più valido. Le riserve si tolgono anche dal popup dello slot.
- Nel **Listone**, il tasto `✗` **depenna** il giocatore quando lo compra un'altra squadra
  (testo barrato, non più aggiungibile; `↩` per ripristinarlo). La spunta *"Nascondi i
  depennati"* li toglie dai risultati.
- **Budget**: spesa, residuo e conteggio 0/25 con obiettivi per reparto (3/8/8/6).
- Tutto viene salvato nel browser (localStorage), niente account.

## Aggiornare il listone

I dati dei giocatori sono incollati dentro `index.html` come array JavaScript (`const RAW = [...]`,
riga ~531). Si rigenerano dal file Excel con lo script **`build_players.py`**.

### Procedura normale (nuovo file da fantacalcio.it)

1. Scarica il listone aggiornato da fantacalcio.it → **Quotazioni → Esporta** (Excel).
2. Metti il file `.xlsx` nella cartella del progetto (nome tipo `Quotazioni_Fantacalcio_*.xlsx`).
   Puoi tenere anche il vecchio: lo script usa **il `.xlsx` più recente** della cartella.
3. Installa la dipendenza una volta sola: `pip install openpyxl`
4. Esegui: `python build_players.py`
5. Ricarica `index.html` nel browser (o ripubblica l'artifact). `git commit` per salvare.

Lo script legge il foglio **`Tutti`** e le colonne `Nome`, `Squadra`, `R`, `RM`, `Qt.A M`,
`FVM M`. I ruoli Mantra multipli (`Ds;E`) vengono convertiti in `Ds/E`.

### Se modifichi l'Excel a mano (aggiungere/cambiare righe)

Puoi aggiungere giocatori o correggere quotazioni direttamente nel `.xlsx`, purché la struttura
resti quella dell'export di fantacalcio.it:

- **Foglio** chiamato `Tutti` (se lo rinomini, lo script usa il primo foglio).
- **Riga 1** = titolo, **riga 2** = intestazioni, **dati dalla riga 3** in poi.
- Non spostare/rinominare le colonne usate: `Nome`, `Squadra`, `R`, `RM`, `Qt.A M`, `FVM M`
  (l'ordine non conta, i nomi sì; altre colonne vengono ignorate).
- Per ogni riga nuova compila almeno `Nome`; le righe con `Nome` vuoto vengono saltate.
- `R` = ruolo macro (`P`/`D`/`C`/`A`), `RM` = ruoli Mantra separati da `;` (es. `Dd;E`).
- `Qt.A M` = quotazione asta Mantra (numero), `FVM M` = fantavalore di mercato (numero).

Poi esegui `python build_players.py` come sopra.

### Nomi accentati corrotti

L'export di fantacalcio.it a volte scrive i caratteri accentati come `�` (es. `Montip�`).
Lo script li corregge con la mappa `FIX` in cima a `build_players.py`. Se dopo l'esecuzione
compare l'avviso `ATTENZIONE, nomi ancora corrotti`, aggiungi le coppie
`"Nome� corrotto": "Nome corretto"` alla mappa `FIX` e rilancia lo script.

## Note

- Nessun build step, nessun account: `index.html` è autosufficiente. Unica dipendenza runtime
  i Google Fonts (Barlow / Barlow Condensed).
- Lo stato (rose, moduli, prezzi, depennati) è salvato nel `localStorage` del browser.
- `build_players.py` richiede solo `openpyxl` e non serve per usare il tool, solo per
  aggiornare il listone.
