# Dokumentation des GUI-Moduls `ged_explorer.py` (Version 1.1.0)

## Überblick

### Beschreibung
Das GUI-Modul `ged_explorer.py` stellt eine graphische Benutzeroberfläche zur Verfügung, mit der Nutzer GEDCOM-Dateien einlesen und strukturierte Daten daraus extrahieren können. Über eine intuitive Oberfläche können Haupt-TAGs und zugehörige Untertags ausgewählt, Spaltennamen definiert sowie optionale Einstellungen wie die Ausgabe einer Jahrgangsspalte vorgenommen werden. Zusätzlich können Konfigurationsdateien im JSON-Format gespeichert und geladen werden, um Einstellungen zwischen Sitzungen zu sichern.
### Screenshot
![alt text](<images/Screenshot 2025-06-02 081628.png>)

### Zusammenhang
Das GUI kommuniziert mit der Logik im Modul `ged_parser.py` (genauer mit der Funktion `gedcom_explorer`) zur eigentlichen Verarbeitung der GEDCOM-Datei und Erzeugung der CSV-Ausgabe. Das GUI ist demnach nur für den Aufbau der Parameter der Funktion `gedcom_explorer` zuständig. 
Außerdem bietet es die Möglichkeit eine json-Parameterdatei zu erstellen um sie später nocheinmal zu laden oder mit der Terminalversion des Explorers zu verwenden.

---

## Features im Überblick

* Auswahl einer GEDCOM-Datei (\*.ged)
* Automatische Ermittlung und Anzeige der Level-1-TAGs (Hauptmerkmale) aus der Datei
* Ermittlung und Auswahl der verfügbaren Untertags zu einem Hauptmerkmal
* Checkboxen zur Auswahl der Untertags und Eingabefelder für benutzerdefinierte Spaltennamen
* Optionales Setzen einer Jahrgangsspalte bei Datumstags
* Speichern und Laden von Konfigurationsdateien (JSON) mit den Einstellungen: Dateipfad, Haupttag, Untertags und Jahrgangsflag
* Anzeige von Warnungen und Fehlermeldungen über Messageboxen
* Klare und übersichtliche Bedienoberfläche mit Scrollbalken bei Eingabefeldern

---

## Klassen und Funktionen

### Klasse `GedTagGUI`

Diese Klasse kapselt die gesamte GUI und deren Logik.

#### Attribute

* `root`: Das Tkinter-Hauptfenster.
* `dateipfad`: Pfad zur ausgewählten GEDCOM-Datei (String).
* `level1_tags`: Liste der im GEDCOM-Dokument gefundenen Haupt-TAGs.
* `untertags_mapping`: Dictionary der Untertags (Key: Strukturstring, Value: Spaltenname).
* `selected_tag`: Tkinter StringVar zur Bindung der Auswahl des Haupt-TAGs.
* `jahrgang_flag`: Tkinter BooleanVar, ob Jahrgangsspalte ausgegeben werden soll.
* `checkbox_vars`: Dictionary (Strukturstring → BooleanVar) für die Checkboxen der Untertags.
* `entry_fields`: Dictionary (Strukturstring → Entry Widget) für die Eingabefelder der Spaltennamen.
* `def_datei_pfad`: Pfad zur aktuellen geladenen oder gespeicherten Definitionsdatei (JSON).
* `nur_haupttag_auswahl`: Bool-Flag, das anzeigt, ob für den gewählten Haupt-TAG keine Untertags verfügbar sind.

#### Methoden

* `__init__(self, root)`: Initialisiert das GUI, setzt Variablen und ruft `create_widgets` auf.
* `create_widgets(self)`: Baut alle GUI-Elemente auf, organisiert Layout, bindet Events.
* `datei_waehlen(self)`: Öffnet Dateidialog zur Auswahl der GEDCOM-Datei, lädt Level-1-TAGs, aktualisiert GUI.
* `lese_level1_tags(self)`: Liest aus der GEDCOM-Datei alle Level-1-TAGs innerhalb von `INDI` oder `FAM`.
* `finde_untertags(self, tag)`: Ermittelt alle Untertags (Level 2 bis 4) eines gewählten Haupt-TAGs.
* `on_tag_selected(self, event)`: Eventhandler für die Auswahl eines Haupt-TAGs, zeigt Untertags an, aktiviert Jahrgangsoption.
* `zeige_untertags(self, untertags)`: Baut dynamisch Checkboxen und Eingabefelder für Untertags auf.
* `daten_ausgeben(self)`: Validiert Eingaben, ruft die Verarbeitungsfunktion `gedcom_explorer` auf, zeigt Erfolg oder Fehler an.
* `konfig_laden(self)`: Öffnet Datei-Dialog für JSON-Konfigurationsdatei, lädt Einstellungen und aktualisiert GUI.
* `konfig_speichern(self)`: Öffnet Datei-Speicher-Dialog, speichert aktuelle Einstellungen im JSON-Format.
* `setze_gui_werte(self, daten)`: Setzt die GUI-Elemente entsprechend der geladenen Konfigurationsdaten.
* `zeige_info(self)`: Zeigt Informationsfenster mit Programmhinweisen.

---

## JSON-Konfigurationsdatei

Die Konfigurationsdatei speichert die wichtigsten Parameter zur Wiederherstellung des Arbeitszustands:

```json
{
  "gedcom_datei": "Pfad/zur/Datei.ged",
  "haupttag": "TAGNAME",
  "untertags": {
    "TAG1": "Spaltenname1",
    "TAG2": "Spaltenname2"
  },
  "jahrgang_flag": true
}
```

* **gedcom\_datei**: Vollständiger Pfad zur GEDCOM-Datei.
* **haupttag**: Der ausgewählte Haupt-TAG.
* **untertags**: Mapping ausgewählter Untertags auf benutzerdefinierte Spaltennamen.
* **jahrgang\_flag**: Boolean, ob Jahrgangsspalte bei Datum ausgegeben werden soll.

---

## Bedienung
Das Programm kann mit dem python interpreter gestartet werden. Dazu müssen die py-Scripte im gleichen Verzeichnis und die Icon-Datei (`prg_logo.ico`) im Verzeichnis `images` liegen.
Es kann auch mit `pyinstaller` kompiliert werden und als ausführbare Datei gestartet werden. Eine Installations ist nicht erforderlich.

### Mit GUI-Oberfläche

1. **GEDCOM-Datei auswählen:** Klick auf „📂 Öffnen“, wähle eine `.ged` Datei.
2. **Haupt-TAG wählen:** Im Dropdown erscheinen die Level-1-TAGs, wähle einen aus.
3. **Untertags auswählen:** Checkboxen und Eingabefelder für Untertags erscheinen.
4. **Jahrgangsoption:** Bei Datumstags kann die Ausgabe einer Jahrgangsspalte aktiviert werden.
5. **Konfiguration speichern:** Benutze den Bereich „Definitionsdatei“ um Einstellungen als JSON zu speichern.
6. **Konfiguration laden:** Lade gespeicherte Einstellungen, um schnell wieder in den vorherigen Zustand zurückzukehren.
7. **Daten ausgeben:** Klick auf „📄 Ausgabe“ startet die Verarbeitung, die CSV-Datei wird erzeugt.

### als Terminalprogramm
GEDCOM-Explorer kann mit dem Parameter `--konsole` auch als Terminalprogramm genutzt werden. 
Auf der Kommandoebene ist dem Programm eine zurvor von der GUI-Version erstellte Definitionsdatei im json-Format als Parameter mitzugeben:
```bash
python .\ged_explorer.py --konsole .\beispiel.json
```
oder als ausführbares Programm:
```bash
ged_explorer --konsole .\beispiel
```

---

## Technische Hinweise

* Das GUI basiert auf `tkinter` und ist plattformunabhängig.
* Die Verarbeitungslogik (Parsing und CSV-Erzeugung) wird im Modul `ged_parser.py` bereitgestellt.
* Es wird UTF-8 als Standard-Encoding verwendet.
* Fehler während der Verarbeitung werden über Messageboxen dem Nutzer angezeigt.

---

## Mögliche Erweiterungen

* Validierung der Spaltennamen auf zulässige Zeichen.
* Automatische Vervollständigung der Spaltennamen.
* Mehrere Haupt-TAGs gleichzeitig auswählen.
* Fortschrittsanzeige bei langer Verarbeitung.
* Anpassung an verschiedene GEDCOM-Versionen.


