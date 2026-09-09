# Campetto Mantra

**▶ [Campetto Mantra](https://andreamurari.github.io/fantamantra-campetti/)** ·
**▶ [Campetto Lega](https://andreamurari.github.io/fantamantra-campetti/campetto_lega.html)**
— usabili anche da telefono, nessun account.

Due tool, stesso motore di ruoli Mantra, dati diversi:

| | Campetto Mantra (`index.html`) | Campetto Lega (`campetto_lega.html`) |
|---|---|---|
| Serve per | l'asta: compri dal listone, la rosa prende forma | la lega a contratti: le rose delle 10 squadre |
| Dati da | listone `.xlsx` di fantacalcio.it | Postgres della lega, riletto ogni ora |
| In più | budget, listone/ricerca, depennati | selettore squadra, contratti, scadenze, prestiti |

Entrambi sono pagine autosufficienti (HTML/CSS/JS in un file solo): apribili anche con un
doppio click, offline, senza installare nulla.

## Come funziona il campetto (comune a entrambi)

- **4 campetti affiancati**, un modulo Mantra ciascuno fra gli 11 di fantacalcio.it
  (3-4-3, 3-4-1-2, 3-4-2-1, 3-5-2, 3-5-1-1, 4-3-3, 4-3-1-2, 4-4-2, 4-1-4-1, 4-4-1-1, 4-2-3-1),
  per confrontare come si dispone la stessa rosa. Sopra ogni campo: `⚡` schiera
  automaticamente chi è libero (i migliori per valore, priorità al ruolo più difensivo) e
  `🧹` svuota titolari, riserve e Jolly di quel campo.
- **Solo ruolo esatto**, niente adattamento: un giocatore entra in uno slot solo se il suo
  ruolo **più difensivo** coincide col ruolo **più offensivo** dello slot (ordine
  `Por < Dc=B < Ds=Dd < M < E < C < T=W < A < Pc`). Uno slot doppio conta per il ruolo più
  offensivo (`M/C`→C, `E/W`→W, `W/A`→A, `A/Pc`→Pc); un giocatore doppio per il più difensivo
  (`E/W`→E, `Dd/Dc`→Dc). Quindi un `E/W` non entra in uno slot `E/W` (vale W): finisce fra i
  **Fuori campo**, sotto il campo — ambra se nessuno slot del modulo lo prevede, verde se
  sarebbe schierabile ma non è in campo.
- **Trascinamento** (anche da telefono): una riserva sul disco scambia col titolare; un
  titolare su un altro disco scambia i due; ogni titolare ha una panchina fino a **4 riserve**;
  fuori dal campo il giocatore torna disponibile. È l'unico modo per forzare un ruolo non
  esatto (il disco resta comunque segnato **grigio tratteggiato**); le automazioni (`⚡`, e
  l'equivalente `⊕` in Rosa) rispettano sempre il ruolo esatto.
- Il pallino prende il **colore del ruolo** di fantacalcio.it (Por giallo, difensori verde,
  centrocampo azzurro, trequarti/ali viola, attacco rosso) e mostra il ruolo completo dello
  slot (`M/C`, `E/W`…).
- In **Rosa**, ogni giocatore ha `⊕` (schiera in ogni campo, o riserva se non c'è slot libero)
  e `⊗` (togli da ogni campo, torna fra i Fuori campo). In alto, `🌙` cambia tema chiaro/scuro;
  lo stato si salva nel `localStorage` del browser, niente account.

## Campetto Mantra

- **Listone 2026/27** integrato: cerca e filtra per ruolo; aggiungendo un acquisto chiede il
  **prezzo pagato** (pre-compilato con la quotazione, poi modificabile dalla rosa). `🚫`
  depenna un giocatore preso da un'altra squadra (`↩️` per ripristinarlo).
- In **Rosa** un terzo tasto rimuove il giocatore del tutto (l'acquisto viene annullato) — in
  Campetto Lega non c'è, la rosa arriva dal database e non si modifica da qui.
- **Budget**: spesa, residuo, conteggio 0/25 con obiettivi per reparto (3/8/8/6). `↻` **Azzera
  tutto** cancella rosa, campi e budget (chiede conferma).

### Aggiornare il listone

I giocatori sono un array JavaScript dentro `index.html`, generato da **`build_players.py`**:

1. Scarica il listone da fantacalcio.it → Quotazioni → Esporta (Excel), mettilo nella cartella
   del progetto. Lo script usa il `.xlsx` più recente, va bene tenerne più di uno.
2. `pip install openpyxl`, poi `python build_players.py`.
3. `git commit` e `git push`: GitHub Pages si aggiorna da solo.

Legge il foglio **`Tutti`**, colonne `Nome`, `Squadra`, `R`, `RM`, `Qt.A M`, `FVM M` (l'ordine
non conta, i nomi sì); righe con `Nome` vuoto vengono saltate. Se modifichi l'Excel a mano,
mantieni questa struttura. I nomi con accenti corrotti (`Montip�`) si correggono aggiungendo
la coppia alla mappa `FIX` in cima allo script.

## Campetto Lega

- **Selettore squadra**: una delle 10, per studiare anche gli avversari. Schieramenti salvati
  per squadra.
- Per ogni giocatore: quotazione, **costo e tipo di contratto** (Indeterminato, Primavera,
  Fanta-prestito, Prestito reale, Hold), **scadenza** (rossa se entro l'anno prossimo), badge
  **U21**, e da chi arriva se è in prestito. In alto: giocatori, monte costi, crediti, U21.

### Come si aggiorna

Ogni ora la GitHub Action `.github/workflows/rose.yml` rilegge il database (in sola lettura,
credenziale nel secret `LEGA_DB_URL`, mai nel repo) e riscrive `lega.json`, che la pagina
rilegge a ogni apertura — nessun intervento manuale. Committa solo se le rose sono cambiate
davvero, così la data in fondo alla pagina è quella dell'ultimo cambiamento reale, non
dell'ultima esecuzione.

Un browser non può leggere il database direttamente (non parla il protocollo Postgres, e
comunque su Supabase non ci sono policy che aprano l'accesso anonimo): per questo a parlare
col database è la Action, non la pagina.

Per rigenerare a mano: stringa di connessione in `.db_url` (gitignorato) o `LEGA_DB_URL`,
`pip install psycopg2-binary`, `python build_lega.py`.

## Struttura del progetto

```
index.html                                     Campetto Mantra
campetto_lega.html                             Campetto Lega
lega.json                                      snapshot rose, riscritto ogni ora dalla Action
build_players.py / build_lega.py               xlsx / Postgres -> dati dentro i due tool
Quotazioni_Fantacalcio_Stagione_2026_27.xlsx   listone sorgente per build_players.py
.github/workflows/rose.yml                     la GitHub Action oraria
```

Nessuna cartella `src/`: due pagine autosufficienti, niente build. `.db_url` non compare
sopra perché non è mai nel repo (`.gitignore`).

## Licenza

[MIT](LICENSE).
