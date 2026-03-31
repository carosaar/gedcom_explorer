# 📄 Dokumentation: `ged_parser.py`

## 🔖 Allgemeines

Dieses Modul verarbeitet GEDCOM-Dateien und extrahiert aus allen Datensätzen (alle L0-TAGs außer "0 HEAD" und "0 TRLR") gezielt Inhalte zu einem bestimmten **L1-TAG** (z. B. `BIRT`, `SOUR` etc.) sowie den zugehörigen **Untertags** (z. B. `DATE`, `PLAC`, `TEXT` usw.). Die extrahierten Daten werden in eine CSV-Datei exportiert.

---

## 🧩 Funktionsübersicht

### 1. `gedcom_explorer(pfad_zur_ged_datei, l1_tag, untertags_katalog, jahrgang_flag)`

Hauptfunktion des Moduls. Sie analysiert eine GEDCOM-Datei und erzeugt eine CSV-Datei mit den gewünschten Daten.

#### **Parameter:**

* `pfad_zur_ged_datei` (`str`): Pfad zur GEDCOM-Datei.
* `l1_tag` (`str`): Der zu untersuchende Level-1-TAG (z. B. `"BIRT"`).
* `untertags_katalog` (`dict`): Ein Dictionary mit GEDCOM-Strukturangaben (z. B. `"DATE"`, `"PLAC"`, `"TEXT"` usw.) als Schlüssel und den gewünschten Spaltennamen als Wert.
* `jahrgang_flag` (`bool`): Falls `True`, wird bei `DATE`-Tags ein zusätzliches Feld `Jahrgang` mit dem Jahr extrahiert.

#### **Beispielaufruf:**

```python
untertags_katalog = {
    "DATE": "Geburtsdatum",
    "PLAC": "Geburtsort",
    "TEXT": "Quelle"
}
gedcom_explorer("familie.ged", "BIRT", untertags_katalog, jahrgang_flag=True)
```

#### **Ablauf der Verarbeitung:**

* ~~Nur **INDI**- und **FAM**-Datensätze werden berücksichtigt.~~
* Pro Datensatz wird ausschließlich der angegebene `l1_tag` (z. B. `BIRT`) verarbeitet.
* Nur dessen **eigene** Untertags (Level 2–4) werden analysiert.
* Andere L1-TAGs im selben Datensatz werden ignoriert.
* Enthaltene GEDCOM-Zeiger (`@...@`) werden von ihren Attributen befreit.
* Wenn ein Tag mehrfach vorkommt, werden die Inhalte mit `" || "` verbunden.
* Falls ein `TEXT`- oder `NOTE`-Tag mit `CONC` oder `CONT` fortgeführt wird, wird `" (...)“` am Ende des Werts angehängt.
* `CONC` und `CONT` werden nicht verarbeitet, weil dies die Tabelle bei langen `TEXT`oder `NOTE` überlasten würde!
* Die L1-TAGs `WIFE` und `HUSB` werden immer ermittelt und gespeichert. 
 (Anmerkung: Sie werden nur bei `FAM`-Datensätzen entsprechende Werte enthalten und sind ansonsten leer)

---

## 🔍 Unterstützende Funktionen

### 2. `extrahiere_jahrgang(datum_raw)`

Extrahiert das Jahr (vierstellig) aus einem GEDCOM-Datum. Berücksichtigt auch Sonderformate wie `INT`, `ABT`, `CAL`. Bestimmte vage Formate (`BEF`, `AFT`, `BET`, ...) werden ignoriert.

### 3. `extrahiere_jahr_simple(text)`

Hilfsfunktion, um eine vierstellige Jahreszahl mit regulärem Ausdruck aus einem String zu extrahieren.

---

## 💡 Besondere Logik & Regeln

* ~~**Blockabgrenzung:** Nur Datenblöcke mit `0 @...@ INDI` oder `0 @...@ FAM` werden berücksichtigt.~~
* **Ebenenwechsel:** Sobald ein neuer L1-TAG kommt (`1 TAG`), wird geprüft, ob dieser dem gewünschten `l1_tag` entspricht. Nur dann erfolgt die Auswertung der Untertags.
* **Mehrfache Untertags:** Falls ein Untertag (z. B. `2 NOTE`) mehrfach unter dem gleichen `l1_tag` auftritt, werden alle Werte gesammelt und mit `" || "` verbunden.
* **Fortführungs-Tags:** `CONC` und `CONT` werden nicht direkt verarbeitet, sondern lediglich zur Markierung verwendet, dass ein `TEXT`/`NOTE`-Tag fortgesetzt wurde. Hierfür wird ein ` (...)` angehängt.
* **Gedcom-Zeiger (@...@):** Diese werden beim Speichern der Werte ohne die einschließenden `@` gespeichert.
* **CSV-Ausgabe:** Das Ergebnis wird in eine CSV-Datei mit folgendem Namensschema geschrieben:
  `Dateiname_l1tag.csv` (z. B. `familie_BIRT.csv`)
* Die Spaltenüberschriften der UnterTAGs sind vom Benutzer frei wählbar (Default ist der/die TAG-Name/n)
  * Beispiel 1 L1-TAG `INDI`: L2-TAG `BIRT` -> Default Überschrift ist: `BIRT`
  * Beispiel 2 L1-TAG `SOUR`: L3-TAG `TEXT` -> Default Überschrift ist: `DATA.TEXT`


---

## 📁 Ausgabe

Die CSV-Datei enthält folgende Spalten:

* `ID`: GEDCOM-Zeiger L0-TAGs.
* `Typ`: `"INDI"` oder `"FAM"`.
* `HUSB`: GEDCOM-Zeiger des Ehemannes (`1 HUSB @...@`).
* `WIFE`: GEDCOM-Zeiger der Ehefrau (`1 WIFE @...@`).
* `l1_tag`: z. B. `"BIRT"` oder `"SOUR"` (Inhalt der L1-TAG selbst, falls vorhanden).
* Weitere Spalten laut `untertags_katalog`.
* Optional: `Jahrgang`, wenn aktiviert und `DATE`-Tag vorhanden.

---

## 📌 Versionierung

* **Aktuelle Version:** `1.1.0`
* **Stand:** `02.06.2025`
* **Stabilität:** Funktionell getestet mit typischen GEDCOM-Dateien. Robuster Umgang mit fehlerhaften oder lückenhaften Strukturen.
