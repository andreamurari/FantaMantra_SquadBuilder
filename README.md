# Campetto Mantra

Due tool separati, stesso motore di ruoli Mantra:

| Tool | File | A cosa serve | Dati |
|---|---|---|---|
| **Campetto Mantra** | `index.html` | L'asta: compri dal listone e vedi la rosa prendere forma | listone `.xlsx` di fantacalcio.it |
| **[Campetto Lega](#campetto-lega)** | `campetto_lega.html` | La lega a contratti: le rose delle 10 squadre sul campo | Postgres della lega, riletto ogni ora |

---

Tool per l'asta del Fantacalcio **Mantra**: un campetto interattivo per vedere come si sta
costruendo la rosa mentre l'asta va avanti.

**▶ [Apri il tool online](https://claude.ai/code/artifact/727c5d4a-a933-4586-bc1c-c6f8bc5d209c)** (usabile anche da telefono)

## Uso

Apri **`index.html`** con un doppio click (funziona offline, senza installare nulla), oppure
usa la [versione online](https://claude.ai/code/artifact/727c5d4a-a933-4586-bc1c-c6f8bc5d209c).

## Cosa fa

- **4 campetti affiancati**: per ognuno scegli uno degli 11 moduli Mantra di fantacalcio.it
  (3-4-3, 3-4-1-2, 3-4-2-1, 3-5-2, 3-5-1-1, 4-3-3, 4-3-1-2, 4-4-2, 4-1-4-1, 4-4-1-1, 4-2-3-1)
  e confronti come si dispone la stessa rosa nei diversi sistemi. Sopra ogni campetto: `⚡`
  schiera automaticamente chi è ancora libero (i migliori per FVM, priorità al ruolo più
  difensivo tra quelli del giocatore; chi non trova posto come titolare va riserva) e `🧹`
  svuota titolari, riserve e Jolly di quel solo campo.
- **Solo ruolo esatto**: in uno slot puoi mettere solo giocatori che hanno quel ruolo Mantra.
  Niente adattamento. Cliccando il pallino si apre il popup dello slot: **Libera lo slot**
  lo svuota, la `x` accanto a una riserva la toglie.
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
    (es. una `E` in un 4-3-3), oppure chi è stato nascosto a mano da **Rosa** (vedi sotto) —
    in quel caso non ci compare nemmeno.
- Il pallino in campo prende il **colore del ruolo** come su fantacalcio.it: Por giallo,
  difensori verde, centrocampo azzurro, trequarti/ali viola, attacco rosso.
- **Listone 2026/27** integrato (dal file `Quotazioni_Fantacalcio_*.xlsx`): cerca e filtra per
  ruolo Mantra; quando aggiungi un acquisto ti viene chiesto il **prezzo pagato** (pre-compilato
  con la quotazione), poi comunque modificabile dalla rosa.
- In **Rosa**, ogni giocatore ha tre tasti: `⊕` lo mette in ogni campo — nel primo slot libero
  compatibile come titolare, oppure come **riserva** (mostrata tra parentesi sotto il titolare)
  se non ci sono slot liberi; salta i campi senza nessuno slot per quel ruolo. `⊗` lo toglie da
  tutti i campi (titolare o riserva). `🗑️` lo rimuove del tutto dalla rosa (l'acquisto viene
  annullato). Cambiando modulo, una riserva viene promossa se il titolare del suo slot non è
  più valido. Le riserve si tolgono anche dal popup dello slot.
- Nel **Listone**, `🚫` depenna il giocatore quando lo compra un'altra squadra (testo barrato,
  non più aggiungibile; al suo posto compare `↩️` per ripristinarlo). La spunta *"Nascondi i
  depennati"* li toglie dai risultati.
- **Budget**: spesa, residuo e conteggio 0/25 con obiettivi per reparto (3/8/8/6).
- In alto, `🌙` **Tema** cambia chiaro/scuro e `↻` **Azzera tutto** cancella rosa, campi e
  budget (chiede conferma).
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

## Campetto Lega

Secondo tool, indipendente dal primo: **`campetto_lega.html`**. Niente asta e niente listone —
qui le rose arrivano dal **database Postgres della lega a contratti** (10 squadre, contratti
pluriennali, prestiti).

**▶ [Apri il tool](https://andreamurari.github.io/FantaMantra_SquadBuilder/campetto_lega.html)** —
rose aggiornate ogni ora, apribile da telefono e condivisibile.
([copia artifact](https://claude.ai/code/artifact/e2a6a127-b479-4a36-8fd8-9233436d6576), ferma
allo snapshot: vedi *Perché non legge il DB in diretta* più sotto.)

- **Selettore squadra**: scegli una delle 10 e ne vedi la rosa sui 4 campetti, così puoi
  studiare anche gli avversari. Gli schieramenti sono salvati per squadra.
- Stessa logica di **match ruolo esatto**, riserve e Jolly del Campetto Mantra: l'enum
  `ruolo_mantra` del database (`Por, Dd, Dc, Ds, B, E, M, C, W, T, A, Pc`) coincide con i ruoli
  che il campetto già gestisce.
- Per ogni giocatore: quotazione, **costo del contratto**, anno di **scadenza** (in rosso se
  scade entro l'anno prossimo), badge **U21** e, per chi è arrivato in prestito, da chi.
- In alto: numero di giocatori, **monte costi**, **crediti** disponibili e U21 in rosa.

### Come si aggiorna

Ogni ora la GitHub Action **`.github/workflows/rose.yml`** rilegge il database e riscrive
`lega.json`, che il sito rilegge a ogni apertura. Nessun intervento manuale.

- La connessione arriva dal secret **`LEGA_DB_URL`**, mai dal repo.
- L'action committa **solo se le rose sono davvero cambiate**: a parità di dati riusa il
  timestamp precedente, così i file restano identici al byte (altrimenti `generato` cambierebbe
  a ogni giro e il repo si riempirebbe di commit inutili).
- La data in fondo alla pagina è quindi quella dell'**ultimo cambiamento reale**, non
  dell'ultima esecuzione.

Due limiti di GitHub da tenere a mente: il cron delle Actions **slitta di 5-15 minuti**, e i
workflow schedulati vengono **disattivati dopo 60 giorni** di inattività del repo (basta un
commit per riattivarli).

Per rigenerare a mano, in locale:

1. Stringa di connessione in `.db_url` nella cartella del progetto, o in `LEGA_DB_URL`.
2. `pip install psycopg2-binary`
3. `python build_lega.py` → riscrive `lega.json` e il blocco `LEGA_DATA` in `campetto_lega.html`.

Lo script apre la sessione in **sola lettura** e legge solo `giocatore`, `squadra` (nome e
crediti) e `general_config`; le colonne credenziali di `squadra` non vengono mai toccate.

> `.db_url` è in `.gitignore`: la stringa di connessione **non va committata**. Il repo è
> pubblico, quindi qualunque credenziale finita qui sarebbe esposta.

### Perché non legge il DB in diretta

La pagina prova tre sorgenti in ordine: `lega.json` dalla stessa origine, poi un eventuale
mirror nella capability `db`, infine lo snapshot incorporato. Aprendo il file col doppio click
le prime due falliscono e resta lo snapshot: è previsto.

Una lettura diretta del database dal browser non è possibile, per quattro motivi indipendenti:

1. il repo non viene eseguito quando apri la pagina — è un file servito, non un processo;
2. un browser non parla il protocollo Postgres (TCP binario), solo HTTP e WebSocket;
3. come artifact, la CSP consente richieste di rete solo verso pochi CDN — Supabase escluso;
4. sul database **RLS è attiva ma non esiste nessuna policy**, quindi l'API REST di Supabase
   restituirebbe comunque zero righe al ruolo anonimo.

Da qui la scelta di far parlare col database la GitHub Action, che invece può farlo.

## Note

- Nessun build step, nessun account: `index.html` è autosufficiente. Unica dipendenza runtime
  i Google Fonts (Barlow / Barlow Condensed).
- Lo stato (rose, moduli, prezzi, depennati) è salvato nel `localStorage` del browser.
- `build_players.py` richiede solo `openpyxl` e non serve per usare il tool, solo per
  aggiornare il listone.
