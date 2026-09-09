# -*- coding: utf-8 -*-
"""
Estrae le rose della lega dal database Postgres (Supabase) e le scrive come
snapshot JSON dentro campetto_lega.html, tra i marcatori LEGA_DATA.

Sola lettura: la sessione viene aperta con readonly=True e si toccano solo
le tabelle public.squadra / public.giocatore / public.general_config.
Le colonne sensibili di `squadra` (username, hash_password, id_telegram)
non vengono mai lette.

Credenziali: variabile d'ambiente LEGA_DB_URL, oppure un file `.db_url`
nella cartella del progetto (gitignorato, NON committarlo).

Uso:  python build_lega.py
"""
import json
import os
import re
import sys
from datetime import date, datetime

try:
    import psycopg2
except ImportError:
    sys.exit("Serve psycopg2:  pip install psycopg2-binary")

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "campetto_lega.html")
# le stesse rose come file a sé: è ciò che la pagina su GitHub Pages
# rilegge a ogni apertura, aggiornato ogni ora dalla GitHub Action
JSON_OUT = os.path.join(HERE, "lega.json")
START = "/* === LEGA_DATA START (generato da build_lega.py) === */"
END = "/* === LEGA_DATA END === */"

# la pseudo-squadra dei giocatori liberi: non è una rosa
FREE = "Svincolato"


def db_url():
    url = os.environ.get("LEGA_DB_URL")
    if url:
        return url.strip()
    path = os.path.join(HERE, ".db_url")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    sys.exit(
        "Connessione mancante. Imposta LEGA_DB_URL oppure crea il file .db_url\n"
        "nella cartella del progetto con dentro la stringa postgresql://..."
    )


def fetch():
    conn = psycopg2.connect(db_url(), connect_timeout=30)
    conn.set_session(readonly=True, autocommit=True)
    try:
        cur = conn.cursor()

        cur.execute("select mercato_chiusura, aste_chiusura, u21_threshold_year from public.general_config limit 1")
        row = cur.fetchone()
        cfg = {
            "mercato_chiusura": row[0].isoformat() if row and row[0] else None,
            "aste_chiusura": row[1].isoformat() if row and row[1] else None,
            "u21": row[2] if row else None,
        }

        # crediti per squadra (niente credenziali: solo nome e crediti)
        cur.execute("select nome, crediti from public.squadra where nome <> %s order by nome", (FREE,))
        crediti = {n: (c or 0) for n, c in cur.fetchall()}

        cur.execute(
            """
            -- ruolo è ruolo_mantra[]: psycopg2 non decodifica gli array di enum
            -- e restituirebbe la stringa grezza "{Dd,E}", quindi si castano a text[]
            select squadra_att, id, nome, club, ruolo::text[], quot_att_mantra, costo,
                   tipo_contratto::text, scadenza_contratto, data_nascita,
                   detentore_cartellino
              from public.giocatore
             where squadra_att <> %s
             order by squadra_att, quot_att_mantra desc nulls last, nome
            """,
            (FREE,),
        )
        rose = {}
        for (sq, pid, nome, club, ruolo, quot, costo, tipo, scad, nasc, det) in cur.fetchall():
            rose.setdefault(sq, []).append(
                {
                    # id stabile dal DB: gli schieramenti salvati restano validi
                    # anche se la rosa cambia
                    "i": pid,
                    "n": nome,
                    "c": club or "",
                    # l'enum ruolo_mantra combacia con i ruoli del campetto
                    "rm": [r for r in (ruolo or []) if r and r != "PlaceHolderRole"],
                    "q": quot or 0,
                    "co": costo or 0,
                    "tc": tipo or "",
                    "sc": scad.isoformat() if scad else None,
                    "dn": nasc.isoformat() if nasc else None,
                    # cartellino altrui = è qui in prestito
                    "pr": det if det and det != sq else None,
                }
            )
        return cfg, crediti, rose
    finally:
        conn.close()


def timestamp_precedente(data):
    """Se le rose non sono cambiate, riusa il timestamp del file esistente.

    Senza questo `generato` cambierebbe a ogni esecuzione e i file
    risulterebbero sempre diversi: la GitHub Action committerebbe ogni ora
    anche a rose immutate. Riusando il vecchio valore i byte restano
    identici, e la data mostrata diventa quella dell'ultimo cambiamento
    vero (che è anche l'informazione più utile).
    """
    try:
        with open(JSON_OUT, encoding="utf-8") as f:
            vecchio = json.load(f)
    except (OSError, ValueError):
        return None
    a, b = dict(vecchio), dict(data)
    a.pop("generato", None)
    b.pop("generato", None)
    return vecchio.get("generato") if a == b else None


def main():
    cfg, crediti, rose = fetch()
    if not rose:
        sys.exit("Nessuna rosa trovata: controlla la connessione.")

    squadre = sorted(rose.keys())
    data = {
        "generato": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "cfg": cfg,
        "squadre": [
            {"nome": s, "crediti": crediti.get(s, 0), "rosa": rose[s]} for s in squadre
        ],
    }

    invariate = timestamp_precedente(data)
    if invariate:
        data["generato"] = invariate

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    blob = START + "\nconst LEGA = " + payload + ";\n" + END

    # 1) il file letto dal sito (GitHub Pages)
    with open(JSON_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(payload + "\n")

    # 2) la copia incorporata nell'HTML, usata quando la pagina è aperta
    #    come file locale e la fetch di lega.json non può funzionare

    if not os.path.exists(TARGET):
        sys.exit("Manca campetto_lega.html: crealo prima (deve contenere i marcatori LEGA_DATA).")

    with open(TARGET, encoding="utf-8") as f:
        html = f.read()
    if START not in html or END not in html:
        sys.exit("Marcatori LEGA_DATA non trovati in campetto_lega.html.")

    html = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        lambda _: blob,
        html,
        flags=re.S,
    )
    with open(TARGET, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    tot = sum(len(s["rosa"]) for s in data["squadre"])
    stato = "invariate dal " + invariate if invariate else "aggiornate"
    print(f"OK: {len(squadre)} squadre, {tot} giocatori ({stato}) -> lega.json + campetto_lega.html")
    for s in data["squadre"]:
        prestiti = sum(1 for p in s["rosa"] if p["pr"])
        costo = sum(p["co"] for p in s["rosa"])
        extra = f", {prestiti} in prestito" if prestiti else ""
        print(f"   {s['nome']:18s} {len(s['rosa']):3d} giocatori, costo {costo:4d}, {s['crediti']:4d} crediti{extra}")


if __name__ == "__main__":
    main()
