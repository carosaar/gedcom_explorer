
# ![alt text](images/prg_logo_ico.png) GEDCOM Explorer – Version 1.1.0

## Übersicht

**GEDCOM Explorer** ist ein Python-Tool zur gezielten Extraktion strukturierter Daten aus GEDCOM-Dateien in das CSV-Format.  
Die Anwendung bietet eine benutzerfreundliche grafische Oberfläche (GUI), mit der man:

- eine GEDCOM-Datei auswählen,
- einen spezifischen Level-1-TAG (z. B. `BIRT`, `DEAT`, `OCCU`, etc.) bestimmen,
- die dazugehörigen Untertags (z. B. `DATE`, `PLAC`, `NOTE`, …) mit Checkboxen auswählen,
- eigene Spaltennamen für die CSV-Ausgabe vergeben und
- optional eine Jahrgangsspalte bei Datumstags erzeugen kann.

---

## Screenshot

![alt text](<images/Screenshot 2025-06-02 081628.png>)

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Die Datei `ged_parser.py` muss sich im gleichen Verzeichnis befinden wie `ged_explorer.py`.

### Installation der Abhängigkeiten

```bash
pip install tk
```

*Hinweis: Unter Windows ist `tkinter` meist bereits vorinstalliert.*

---

## Verwendung

```bash
python ged_explorer.py
```

1. GEDCOM-Datei auswählen
2. Level-1-TAG (L1-TAG) aus Dropdown wählen
3. Untertags auswählen und Spaltennamen anpassen
4. (Optional) Jahrgangsoption aktivieren
5. Auf **Ausgabe** klicken – eine CSV-Datei wird erstellt

---

## Dateiaufbau

* `ged_explorer.py`: GUI-Anwendung
* `ged_parser.py`: Logik zur GEDCOM-Verarbeitung und CSV-Erzeugung

---

## Ausgabe

Die erzeugte CSV-Datei enthält nur die selektierten Informationen und trägt denselben Namen wie die GEDCOM-Datei, ergänzt um den gewählten TAG.
Beispiel:
`familie.ged` → `familie_BIRT.csv`

---

## Changelog

### Version 0.1.0 (2025-05-30)

* 🛠 **Fehlerbehebung**: `TclError: Index -1 out of range` beim Dropdown-Auswahlfeld nach Dateiwechsel wurde behoben.
* ✅ **Verbesserung**: Automatisches Leeren und Reinitialisieren der Dropdown-Liste nach Auswahl einer neuen GEDCOM-Datei.
* ➕ **Neu**: Auswahlstruktur für Untertags mit Checkbox + Eingabefeld für benutzerdefinierte Spaltennamen.
* 📅 **Optional**: Aktivierbare Jahrgangsspalte bei Vorhandensein eines `DATE`-Tags.
* 📄 **CSV-Erzeugung**: Erfolgreiche Verarbeitung gibt Pfad zur CSV-Datei an GUI zurück.
* 🔒 **Robustheit**: Verbesserte Validierung von Dateipfaden und Benutzeraktionen.
* 🔍 **Intern**: Die Untertag-Auswertung unterstützt jetzt auch verschachtelte Strukturen bis Level 4.

### Version 1.1.0 (2025.06.02)

* ✅ **Verbesserung**: 
  * Die Beschränkung auf INDI- und FAM- Datensätze werden aufgehoben, 
  * Minimale Fenstergröße, 
  * Ausgabe eines L1-TAG auch ohne ausgewählte Untertags
  * Da die L1-TAGs WIFE und HUSB in der csv-Datei immer ausgegeben werden, sind sie  
    bei der Liste der Merkmale der Ebene 1 nicht enthalten. 
* ➕ **Neu**: Auswahl "Alle" oder "Keine" Untertags eingefügt
* ℹ️ Programm- und Fenster-Icon implementiert 
  Kompilieren mit 
  ```bash
  pyinstaller --onefile --windowed --icon=images\prg_logo.ico --add-data "images\prg_logo.ico;images" ged_explorer.py
  ```

---

## Lizenz

GNU General Public-Lizenz

---

## Autor

* Erstellt von Dieter Eckstein – 2025

