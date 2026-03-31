#  ![alt text](docs/prg_logo_ico.png) GEDCOM Explorer

![Version](https://img.shields.io/badge/version-1.3-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-stable-green)

Ein leistungsstarkes Tool zur Analyse und Extraktion von GEDCOM-Daten in strukturierte CSV-Dateien.

---

## 🚀 Features

- 🔍 Intelligente L1-TAG-Auswahl (Auto-Complete + Filter)
- 🧩 Flexible Untertag-Auswahl
- 📅 Jahrgangs-Erkennung aus DATE-Tags
- 📝 Unterstützung für CONT/CONC
- 💾 Konfigurationsdateien (.gexp)
- 🖥️ GUI + CLI-Modus

---

## 📦 Download

👉 Aktuelle Version im Bereich **Releases** herunterladen

---

## ⚡ Schnellstart

1. ZIP-Datei herunterladen  
2. Entpacken  
3. Installer ausführen
4. `ged_explorer.exe` starten  

---

## ⚠️ Windows-Hinweis

Beim ersten Start ggf.:

→ „Weitere Informationen“  
→ „Trotzdem ausführen“

---

## 🖼️ Screenshot

![alt text](docs/Screenshot.png)

---

## 🧩 Funktionsprinzip

1. GEDCOM-Datei auswählen
2. L1-TAG festlegen
3. Untertags wählen
4. CSV exportieren

---

## 🖥️ CLI / Batch-Nutzung

Der GEDCOM Explorer kann auch ohne GUI direkt über eine Definitionsdatei gestartet werden:

```bash
ged_explorer.exe definition.gexp
```

💡 Einsatzmöglichkeiten
Automatisierte Verarbeitung per Batch-Datei
Integration in Skripte oder Workflows
Wiederholbare Auswertungen mit gespeicherten Konfigurationen

Beim Start mit einer .gexp-Datei wird die Verarbeitung direkt ausgeführt, ohne die grafische Oberfläche zu öffnen.

---

## 📚 Dokumentation

* CHANGELOG.md
* RELEASE.md

---

## 📄 Lizenz

Siehe LICENSE
