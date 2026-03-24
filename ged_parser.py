"""
Version: 1.2.2
Datum: 2025-06-XX

Optimierungen:
- CONT/CONC werden ausschließlich NOTE-TAGs zugeordnet
- Bei cont_preview_length = 0: keine Vorschau, keine Trennzeichen
- Fortsetzungszeichen "(...)" nur bei NOTE-TAGs
- Jahrgangsspalten pro DATE-Struktur (<Spaltenname>.JAHRGANG)
"""

import csv
import os
import re


def extrahiere_jahrgang(datum_raw):
    if not datum_raw:
        return ""

    if datum_raw.startswith("INT"):
        match = re.match(r"INT\s+([^\(]+)", datum_raw)
        if match:
            return extrahiere_jahr_simple(match.group(1).strip())

    if datum_raw.startswith("ABT") or datum_raw.startswith("CAL"):
        rest = datum_raw[3:].strip()
        return extrahiere_jahr_simple(rest)

    if re.match(r"^(BEF|AFT|BET|TO|FROM|AND|EST)\b", datum_raw):
        return ""

    return extrahiere_jahr_simple(datum_raw)


def extrahiere_jahr_simple(text):
    match = re.search(r"\b(\d{4})\b", text)
    return match.group(1) if match else ""


def gedcom_explorer(
    pfad_zur_ged_datei,
    l1_tag,
    untertags_katalog,
    jahrgang_flag,
    cont_preview_length=50,
    cont_separator=" "
):
    eintraege = []
    datensatz_typ = None
    datensatz_id = None
    akt_l1_tag = None
    akt_untertagswerte = {}
    fortfuehrung_text_tags = set()
    prev_tags = ["", "", ""]
    letzte_struktur = ""
    in_gueltigem_block = False
    aktueller_l1_tag = ""
    husb = ""
    wife = ""

    def flush_eintrag():
        if akt_l1_tag is not None and aktueller_l1_tag == l1_tag:
            eintrag = {
                "ID": datensatz_id,
                "Typ": datensatz_typ,
                "HUSB": husb,
                "WIFE": wife,
                l1_tag: akt_l1_tag,
            }

            # Untertags
            for struktur, spaltenname in untertags_katalog.items():
                wert = akt_untertagswerte.get(spaltenname, "")
                if spaltenname in fortfuehrung_text_tags:
                    wert += " (...)"
                eintrag[spaltenname] = wert

            # Jahrgangsspalten pro DATE-Struktur
            if jahrgang_flag:
                for struktur, spaltenname in untertags_katalog.items():
                    if struktur.endswith("DATE"):
                        wert = akt_untertagswerte.get(spaltenname, "")
                        jahr = extrahiere_jahrgang(wert)
                        eintrag[spaltenname + ".JAHRGANG"] = jahr

            eintraege.append(eintrag)

    # Datei einlesen
    with open(pfad_zur_ged_datei, "r", encoding="utf-8") as f:
        zeilen = f.readlines()

    for zeile in zeilen:
        parts = zeile.strip().split(" ", 2)
        if len(parts) < 2:
            continue
        ebene, tag = parts[0], parts[1]
        wert = parts[2] if len(parts) == 3 else ""

        # Neuer Datensatz
        if ebene == "0":
            flush_eintrag()
            akt_untertagswerte = {}
            fortfuehrung_text_tags = set()
            datensatz_id = ""
            datensatz_typ = ""
            akt_l1_tag = None
            aktueller_l1_tag = ""
            in_gueltigem_block = False
            husb = ""
            wife = ""

            match = re.match(r"0 @([^@]+)@ (\w+)", zeile)
            if match:
                datensatz_id = match.group(1)
                datensatz_typ = match.group(2)
                if datensatz_typ not in ("HEAD", "TRLR"):
                    in_gueltigem_block = True
            continue

        if not in_gueltigem_block:
            continue

        # L1-TAG
        if ebene == "1":
            if tag == "HUSB":
                husb = wert.strip("@")
            elif tag == "WIFE":
                wife = wert.strip("@")

            flush_eintrag()
            akt_untertagswerte = {}
            fortfuehrung_text_tags = set()
            aktueller_l1_tag = tag
            akt_l1_tag = wert.strip("@") if re.match(r"^@[^@]+@$", wert) else wert
            continue

        # Nur Untertags des gewählten L1-TAGs
        if aktueller_l1_tag != l1_tag:
            continue

        # CONT/CONC – nur für NOTE-TAGs
        if tag in ("CONC", "CONT"):
            if letzte_struktur and letzte_struktur.endswith("NOTE"):
                spaltenname = untertags_katalog.get(letzte_struktur)
                if spaltenname:
                    fortfuehrung_text_tags.add(spaltenname)

                    # Vorschau nur wenn > 0
                    if cont_preview_length > 0 and wert:
                        akt_untertagswerte.setdefault(spaltenname, "")
                        akt_untertagswerte[spaltenname] += cont_separator + wert[:cont_preview_length]

            continue

        # L2–L4 Untertags
        if ebene in ["2", "3", "4"]:
            index = int(ebene) - 2
            if index < len(prev_tags):
                prev_tags[index] = tag

            strukturteile = prev_tags[:index] + [tag]
            struktur = ".".join(filter(None, strukturteile))

            if struktur in untertags_katalog:
                spaltenname = untertags_katalog[struktur]
                value = wert.strip("@") if re.match(r"^@[^@]+@$", wert) else wert
                letzte_struktur = struktur

                if spaltenname in akt_untertagswerte and value:
                    if value not in akt_untertagswerte[spaltenname]:
                        akt_untertagswerte[spaltenname] += " || " + value
                else:
                    akt_untertagswerte[spaltenname] = value

    flush_eintrag()

    if not eintraege:
        return

    # CSV-Ausgabe
    dateiname = os.path.splitext(os.path.basename(pfad_zur_ged_datei))[0] + f"_{l1_tag}.csv"
    ausgabepfad = os.path.join(os.getcwd(), dateiname)

    feldnamen = ["ID", "Typ", "HUSB", "WIFE", l1_tag]
    feldnamen += list(untertags_katalog.values())

    if jahrgang_flag:
        for struktur, spaltenname in untertags_katalog.items():
            if struktur.endswith("DATE"):
                feldnamen.append(spaltenname + ".JAHRGANG")

    with open(ausgabepfad, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=feldnamen, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for eintrag in eintraege:
            writer.writerow(eintrag)

    return ausgabepfad