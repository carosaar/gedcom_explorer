## Projektziel
Python-Script zum Extrahieren einer hierarchischen GEDCOM-Struktur einer genealogischen Datei (ged-Datei) in eine csv-Datei

Beispielhafte Anwendung:

  GED-Datei enthält: 
    `0 @Zeiger@ INDI, 1 BIRT , 1 DEAT, 1 MARR, 1 SOUR @<Zeiger>@`
  Nutzer wählt den TAG: `SOUR`

  Auswahl der anzuzeigenden Spalten dercsv-Datei:
  ```
    2 PAGE ✅ Spaltenname: "Fundort"
    2 DATA
    3 TEXT ✅ Spaltenname: "Zitat"
    2 WWW ✅ Spaltenname: "Link"
```
→ Ausgabe: DATEINAME_SOUR.csv mit Spalten: 
  `ID, Typ, Quelle, Fundort, Zitat, Link`
Die Daten der csv enthalten für jeden gefundenen Datensatz
  `<INDI-Zeiger>, Zeigertyp (INDI oder FAM), SOUR-Wert, PAGE-Wert, TEXT-Wert, WWW-Wert`
  Dabei werden Zeiger an den einschließenden `@@` erkannt und stets ohne die `@@`gespeichert:
  `"I123","INDI","S222","Zitatstelle","Erläuterung","https://internet.com"`

## Begriffe
* **GUI-Modul**: `ged_explorer.py` enthält die **GUI-Steuerung** zur Bestimmung der zu untersuchenden ged-Struktur und den Parser-Aufruf im Logik-Modul 
* **Logikmodul**: Funktionsbibliothek `ged_parser.py` mit der Funktionsbibliothek zur parser-Logik 
* **ged-Datei**: Die Eingabedatei im gedcomformat `<gedname>.ged`
* **TAG-Bezeichnung**: Die gencom-TAGs werden mit zusammen mit ihrer Ebene (L0-L4) bezeichnet:
  z.B.: 
   - `Ln-TAG`: allgemine Bezeichnung eines TAGs der Ebene `n`
   Beispiel: *L1-TAG* ein TAG der Ebene 1
   - `Ln-<TAG-Name>`: konkrete Bezeichnung des TAGs `<TAG-Name>` auf der Ebene `n`
   Beispiel: *L2-DATE* der DATE-TAG der auf der Ebene 2 der Hierachie steht
   oder *L3-DATE* der DATE-TAG, der auf der Ebene 3 der Hierarchie steht.
   - `TAG`: allgemeine Bezeichnung eines TAGs der Ebene 1 bis 4 
   - `TAG-Wert`: Der Text ("dies ist ein Text") oder ein Pointer (@I123@) auf einen Datensatz in der GED-Datei, der nach dem TAG
   - `UnterTAG`: allgemeine Bezeichnung eines TAGs der Ebene 2 bis 4
   - `Datensatz`: allgemeine Bezeichnung eines TAGs der Ebene 0
  **Besonderheit für L0-TAGs:**
  L0-TAGs definieren einen gencom-Datensatz mit einem **Datensatzzeiger** innerhalb der `@` Zeichen. Der **Datensatzbezeichner** nennt den Datensatztyp (INDI, FAM usw.). Der Datensatzzeiger wird auch als **Pointer** bezeichnet.
  *Anmerkung*: Im Projekt werden nur Datensätze des Typs `INDI` und `FAM` untersucht. Alle anderen Datensätze bleiben unberücksichtigt.

  Ein konkreter TAG im Zusammenhang seiner Hierarchie werden die TAGs als **TAG-Struktur **in der Reihenfolge ihrer Ebenen mit Punkt getrennt. Die Ebene 0 kann entfallen. dann gilt die TAG-Struktur für alle Datensätze (z.B. .NOTE)
  Beispiele:
  * `INDI.BIRT.PLAC.NOTE`:  der L3-TAG *NOTE* unterhalb des L2-TAG *PLAC* unterhalb des L1-TAG *BIRT* im Datensatz *INDI*
  * `.REFN`: der L1-TAG *REFN* in allen Datensätzen
  * `FAM._UID`: der L1-TAG *_UID* im Datensatz *FAM*

---

## unspezifische Beschreibung des Logik-Moduls
  Das Logikmodul enthält alle Funktionen, die für die Untersuchung der gedcom-Datei und Erstellung der csv-Datei notwendigen Funktionen bereitstellt. Die Hauptfunktion ist ist `gedcom_explorer()`. Sie wird vom GUI-Modul mit den in der GUI festgelegten Parametern (z.B. ged-Datei, zu untersuchender L1-TAG und Unter-TAGs) aufgerufen.
  ### Eingabeparameter
  - `ged-Datei`: Pfad und Name der ged-Datei
  - `L1-TAG`: Name des L1-TAG, dessen UnterTAGs untersucht werden sollen
  - `UnterTAG`: Liste der UnterTAGStruktur des L1-TAG mit den gewählten Spaltennamen als py-Katalog der Form: [L2-TAG[.L3-TAG[.L4-TAG]]: Spaltenname]
  Beispiel: 
    `["DATE": "Datum", "PLAC": "Ort", "TYPE": "Art"]` oder
    `["PAGE": "Fundstelle", "DATA.TEXT": "Zitat", "WWW": "Link-Adresse"]`

  - `Flag`: logischer Wert, der angibt, ob eine Zusatzspalte `Jahrgang` nach einer Datumsspalte eingefügt wird, die das Jahr des Datums enthält.
  
  ### logischer Funktionsablauf
  * Suche in der ged-Datei in allen INDI- und FAM-Datensätzen nach dem `L1-TAG` (**`Eingabeparameter 1`**)
  Merke dir dabei `Datensatzzeiger` (ohne @-Zeichen) und `Datensatztyp` (`INDI` oder `FAM`)
  * Sammle zu jedem gefundenen `L1-TAG` die `TAG-Werte` der `Unter-TAG` aus dem Katalog (**`Eingabeparameter 2`**) 
    - Entferne bei L2-TAG mit einem Zeigerwert als alleinger TAG-Wert (z.B. `1 SOUR @S222@` oder `2 HUSB @I123@`) die einschließenden @-Zeichen. d.h.: `@@` wird nicht entfernt, wenn eim TAG-Wert weiterer Text steht (z.B. 2 NOTE Möglicherweise auch `@I123@`)
    - Folgt dem `Unter-TAG` ein `CONT` oder `CONC` Tag, so füge an den TAG-Wert des `Unter-TAG` die Zeichen ` (...)` hinzu.
    *Erklärung: Die Werte der TAGs `CONT` und `CONC` werden nicht gesammelt. Dese TAGs weisen darauf hin, dass ein NOTE-TAG oder TEXT-TAG weitere Zeilen als Wert haben. Auf die Folgezeilen wird lediglich mit  ` (...)` hingewiesen*
    - Werden zu einem L1-TAG mehrere gleiche Untertags gefunden, werden die Werte mit ` || ` verbunden.
    z.B. Es gibt im L1-TAG `SOUR` mehrere L2-TAGs `WWW`: Die Werte der beiden L2-TAGs werden zusammengeführt und mit ` || ` verbunden: `Https://link1.com || https://link2.de`
  * Wenn der **`Eingabeparameter 3`** `WAHR` ist wird in der csv-Datei nach der oder den DATE-Spalten eine weitere Spalte `Jahrgang`eingefügt, in der die Jahreszahl des davorstehenden `DATE`-TAG steht.
  `Jahrgang` wird aus dem GEDCOM-Datum nach bestimmten Regeln extrahiert:
    * INT <Datum> (Kommentar) → Jahr aus dem Teil vor der Klammer
    * ABT <Datum>, CAL <Datum> → Jahr aus dem Datum
    * BEF, AFT, BET, TO, EST, FROM, AND → ignorieren (leer lassen)
    * Unvollständige Datenformate wie 1900, JUN 1900, 12 JUN 1900 werden unterstützt.
    
    **Beispiele**:
    | GEDCOM-CODE                                     | Beispiel                          | Jahrgang |
    | ----------------------------------------------- | --------------------------------- | -------- |
    | `INT`                                           | `INT 12 JUN 1900 (geschätzt)`     | `1900`   |
    | `ABT`                                           | `ABT 1900`                        | `1900`   |
    | `CAL`                                           | `CAL JUN 1900`                    | `1900`   |
    | `BEF`, `AFT`, `BET`, `FROM`, `TO`, `EST`, `AND` | `BET 1900 AND 1910`               | *(leer)* |
    
    siehe hierzu eine bereits fertig gestellte Funktion: [^1] 

### Ausgabe
* Die Ausgabedatei ist im csv-Format UTF-8-Coding mit csv.QUOTE_ALL
* der Name der Datei wird zusammengesetzt `<gedname>_<L1-TAG>.csv`
Beispiel: Eingabedatei ist `..\eingabe.ged`, L1-TAG ist `SOUR` -> Ausgabedatei: `eingabe_SOUR.csv`
* die Ausgabedatei wird im Startverzeichnis des Programmes abgelegt und nicht im Verzeichnis der Eingabedatei!

---
## unspezifische Beschreibung des GUI-Moduls zur Erfassung der Eingabeparameter und Steuerung der Bearbeitung

**NOP folgt später**

 [^1]: Code-Block `Jahrgang aus DATE extrahieren`



 ---
 ## CODE-Block
 ### Jahrgang aus DATE extrahieren

```
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
```
