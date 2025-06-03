
# ![alt text](images/prg_logo_ico.png) GEDCOM Explorer – Version 1.1.0

## Übersicht

**GEDCOM Explorer** ist ein Python-Tool zur gezielten Extraktion strukturierter Daten eines `L1-TAGs` und seinen UnterTAGs (`L2-L4 TAGs`) aus GEDCOM-Dateien in eine Tabelle im `CSV`-Format.  
Die Anwendung bietet 
* eine benutzerfreundliche grafische Oberfläche (GUI), mit der man:
  - eine GEDCOM-Datei auswählen,
  - einen spezifischen Level-1-TAG (z. B. `BIRT`, `DEAT`, `OCCU`, etc.) bestimmen,
  - die dazugehörigen Untertags (z. B. `DATE`, `PLAC`, `NOTE`, …) mit Checkboxen auswählen,
  - eigene Spaltennamen für die CSV-Ausgabe vergeben und
  - optional eine Jahrgangsspalte bei Datumstags erzeugen kann.
  - Speichern der eingestellten werte in eine Definitionsdatei im `JSON`-Format
* eine Konsolenversion (CLI), die in Batchdateien verwendet weden kann

---
## Bildschirmfoto
![alt text](<images/Screenshot 2025-06-02 184419.png>)

---
## Zweck des Programmes
### Problem des GEDCOM-Formats
Das GEDCOM-Format erlaubt es, die Werte der TAGs beliebig zu wählen. Es gibt ausßer für den L0-TAG keine Syntaxvorschriften. Dies kann dazu beitragen, dass in einem Genealogieprojekt gleiche oder ähnliche Informationen unter verschiedenen TAGs abgelegt werden oder Projekt-Konventionen zur Schreibweise von TAG-Werten nicht eingehalten werden können, weil die Genealogieprogramme keine Syntaxprüfung durchführen.
### Konsequenz
Eine Überprüfung der einheitlichen Informationszuordnung zu TAGs und die Kontrolle selbst vorgegebener Syntaxkonventionen ist nicht möglich. Es besteht daher die Gefahr, dass mit der Zeit das Projekt für eine systematische Auswertung, die Verwendung in Programmen zur strukturierten Darstellung der genealogischen Daten oder auch einfach zur Weitergabe schlicht unbrauchbar sind.
### Problemlösung
Eine tabellarische Übersicht eines TAGs und seiner UnterTAGs ermöglicht eine schnelle Information über die erfassten TAG-Wert. Eine Tabelle im CSV-Format kann in einer Tabellenkalkulation oder einer Datenbank standardmäßig verwendet werden und ermöglicht dort dann umfangreiche Systaxprüfungen in den TAG-Werten.
Entdeckte Fehler können dann über den Zeiger des L0-TAG im Genealogieprojekt oder in der GED-Datei lokalisiert und schließlich verbessert werden. 

---
## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Die Datei `ged_parser.py` muss sich im gleichen Verzeichnis befinden wie `ged_explorer.py`.
- Die Datei `prg_logo.ico` muss sich im Ordner `images` befinden

### Installation der Abhängigkeiten

```bash
pip install tk
```
*Hinweis: Unter Windows ist `tkinter` meist bereits vorinstalliert.*

---

### Kompilieren 
  ```bash
  pyinstaller --onefile --windowed --icon=images\prg_logo.ico --add-data "images\prg_logo.ico;images" ged_explorer.py
  ```

## Verwendung
### GUI-Oberfläche
```bash
python ged_explorer.py
```

1. GEDCOM-Datei auswählen
2. Level-1-TAG (L1-TAG) aus Dropdown wählen
3. Untertags auswählen und Spaltennamen anpassen
4. (Optional) Jahrgangsoption aktivieren
5. Auf **Ausgabe** klicken – eine CSV-Datei wird erstellt
6. optional Programmfestlegungen als Definitionsdatei im JSON-Format speichern
   für die spätere Wiederverwendung oder den Konsolenmodus

### Konsolen-Modus (CLI)
```bash
python ged_explorer.py --konsole definitionen.json
```
### Ausführbare Datei
ged_explorer kann plattformunabhängig kompiliert werden
> Hinweis: 
Eine Windows-EXE ist im Verzeichnis `/dist` bereits zur direkten Verwendung hinterlegt.
Eine Installation ist nicht erforderlich.

---
## Dateiaufbau
* `ged_explorer.py`: GUI-Anwendung und CLI-Steuerung   [🔍 Modul-Dokumentation](ged_explorer_Dokumentation.md)
* `ged_parser.py`: Logik zur GEDCOM-Verarbeitung und CSV-Erzeugung   [🔍 Modul-Dokumentation](ged_parser_Dokumentation.md)

---
## Ausgabe
Die erzeugte CSV-Datei enthält nur die selektierten Informationen und trägt denselben Namen wie die GEDCOM-Datei, ergänzt um den gewählten TAG.
Beispiel:
`familie.ged` → `familie_BIRT.csv`

---
## Hauptmerkmale
* ✅ **L1-TAG** Auswahl aus allen ermittelten L1-TAGs 
  **Ausnahme**: Keine L1-TAGs `WIFE` und `HUSB`, da diese Zeiger in der CSV-Datei immer ausgegeben werden. 
* ✅ Spaltenauswahl für Untertags (L2-L4) mit Eingabemöglichkeit für benutzerdefinierte Spaltennamen.
  🔍 **Intern**: Die Untertag-Auswertung unterstützt auch verschachtelte Strukturen bis Level 4.  
  📅 **Optional**: Aktivierbare Jahrgangsspalte bei Vorhandensein eines `DATE`-TAGs.
  ➕ **Neu**: Auswahl `Alle` oder `Keine` Untertags
* 📄 **CSV-Erzeugung**: Erfolgreiche Verarbeitung gibt Pfad zur CSV-Datei an GUI zurück.
* 🔒 **Robustheit**: Validierung von Dateipfaden und Benutzeraktionen.
* ✅ Keine Beschränkung auf INDI- und FAM- Datensätze 
* ✅ **CLI**: Ausführug als Konsolenprogramm mit dem Parameter `--konsole` zur Verwendung in batch-Programmen
  Dem Programm wird als weiterer Parameter eine **Definitionsdatei im JSON-Format** mitgegeben.

## Einschränkungen
* ❌ UnterTAGs `CONT` und `CONC` werden **nicht** ausgewertet. 
  Der Wert im übergeordneten TAG (z.B. `NOTE`) wird um das Fortsetzungszeichen ` (...)` erweitert.
  z.B. Spalte `NOTE`: `Die Notiz hat Folgezeilen (...)`
* ❌ mehrfach auftretende UnterTAGs gleichen Namens (z.B. `NOTE`) werden in einer einzigen Spalte übernommen. 
  Die Werte der einzeln auftretenden gleichen UnterTAGs werden mit Kaskadierungszeichen  ` || ` verbunden
  z.B. Spalte `NOTE`: `Dies ist ein wichtiger Hinweis || Und noch eine Extra-Notiz`

---

## Lizenz

GNU General Public-Lizenz
> Die Nutzung des Programmes und der Quellcode ist für private und kommerzielle Nutzung frei.
> Bei Verwendung des Quellcodes bitte ich um einen Hinweis auf dieses github-Projekt und 
> eine kurze Info an mich.

---

## Autor

* Dieter Eckstein – 2025
  https://www.carosaar.de


