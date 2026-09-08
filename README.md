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
- **Schieramento automatico** (`⚡` e `⊞`):
  - lato **giocatore** si guarda il ruolo **più difensivo** — ordine
    `Por < Dc=B < Ds=Dd < M < E < C < T=W < A < Pc` (un M/C è una M, un Dc/Dd è una Dc);
  - lato **modulo** uno slot doppio vale sempre come il suo ruolo **più offensivo**
    (lo slot `M/C` è una C, `W/A` è una A, `A/Pc` è una Pc);
  - se quel ruolo è tutto occupato il giocatore va in **riserva**, senza scalare a un ruolo
    meno difensivo. Es. con due M/C in un 3-4-2-1: uno titolare sulla M, l'altro riserva,
    e lo slot M/C resta libero per una C.
  - Il pallino mostra il ruolo effettivamente ricoperto.
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

## Note

- Per aggiornare il listone, rigenera la lista `RAW` in `index.html` dal nuovo xlsx.
