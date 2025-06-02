"""
Version: 1.1.0
Datum: 2025-06-02
v1.0.2a = v1.1.0
Alle Datensätze erlaubt außer 0 HEAD und 0 TRLR
ID, ID-TYP, HUSB, WIFE werden immer in die CSV-Tabelle übernommen
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

def gedcom_explorer(pfad_zur_ged_datei, l1_tag, untertags_katalog, jahrgang_flag):
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
            for struktur, spaltenname in untertags_katalog.items():
                wert = akt_untertagswerte.get(spaltenname, "")
                if struktur.endswith("TEXT") or struktur.endswith("NOTE"):
                    if spaltenname in fortfuehrung_text_tags:
                        wert += " (...)"
                eintrag[spaltenname] = wert

            if jahrgang_flag:
                for struktur, spaltenname in untertags_katalog.items():
                    if struktur.endswith("DATE"):
                        jahrgang = extrahiere_jahrgang(akt_untertagswerte.get(spaltenname, ""))
                        eintrag["Jahrgang"] = jahrgang

            eintraege.append(eintrag)

    with open(pfad_zur_ged_datei, "r", encoding="utf-8") as f:
        zeilen = f.readlines()

    for zeile in zeilen:
        parts = zeile.strip().split(" ", 2)
        if len(parts) < 2:
            continue
        ebene, tag = parts[0], parts[1]
        wert = parts[2] if len(parts) == 3 else ""

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

        if aktueller_l1_tag != l1_tag:
            continue

        if ebene in ["2", "3", "4"]:
            if tag in ("CONC", "CONT"):
                if letzte_struktur:
                    for struktur, spaltenname in untertags_katalog.items():
                        if struktur == letzte_struktur:
                            fortfuehrung_text_tags.add(spaltenname)
                continue

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

    dateiname = os.path.splitext(os.path.basename(pfad_zur_ged_datei))[0] + f"_{l1_tag}.csv"
    ausgabepfad = os.path.join(os.getcwd(), dateiname)

    feldnamen = list(eintraege[0].keys())
    with open(ausgabepfad, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=feldnamen, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for eintrag in eintraege:
            writer.writerow(eintrag)

    # print(f"Fertig\nCSV-Datei gespeichert unter: {ausgabepfad}")
    return ausgabepfad