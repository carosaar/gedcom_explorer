# 🟦 **GitHub Release: GEDCOM Explorer 1.3**

## 🚀 Highlights dieses Releases

**GEDCOM Explorer 1.3** ist ein großes Funktions‑ und Usability‑Update, das die Arbeit mit GEDCOM‑Dateien deutlich komfortabler, schneller und zuverlässiger macht.  
Dieses Release integriert außerdem alle Verbesserungen des internen Releases 1.2.

---

## ✨ Neue Funktionen

### 🔍 Intelligente L1‑TAG‑Eingabe
- **Auto‑Complete** während der Eingabe  
- **Live‑Filterung** der verfügbaren L1‑TAGs  
- **ENTER‑Bestätigung** ohne Öffnen der Dropdown‑Liste  
- **automatische Validierung** bei Fokusverlust  
- **Fehlermeldung bei ungültigem L1‑TAG**  
- **automatische Markierung** des gesamten Inhalts beim Klick ins Feld  

Damit fühlt sich die L1‑TAG‑Auswahl wie ein modernes Suchfeld an.

---

### 🧩 Verbesserte Untertag‑Verwaltung
- Mindesthöhe des Untertag‑Bereichs  
- dynamische Anpassung an Fenstergröße  
- kein Abschneiden der Untertags mehr  
- kompakteres Layout mit weniger Leerraum  
- Auswahl „Alle“ / „Keine“ Untertags

---

### 💾 Neue Definitionsdateien (.gexp)
- neues Format: `.gexp` statt `.json`  
- automatischer Vorschlagsname:  
  **`<GEDCOM>_<L1‑TAG>.gexp`**  
- kompatibel mit GUI und CLI  
- vollständige Speicherung aller Einstellungen

---

### 🖥️ GUI‑Verbesserungen
- modernisiertes, kompakteres Layout  
- zentrierter **Ausgabe**‑Button  
- optimierte Fenstergeometrie  
- klarere Bezeichnung: **Hauptmerkmal (L1‑TAG)**  
- Standardwert für CONT/CONC‑Vorschau: **0**

---

## 🛠️ Verbesserungen aus Release 1.2 (integriert)
- CONT/CONC‑Vorschau mit Zeichenlimit  
- Trennzeichen für CONT/CONC  
- automatisches Fortsetzungszeichen `(...)` bei NOTE  
- Jahrgangsspalten bei DATE‑Tags  
- Auswahl „Alle“ / „Keine“ Untertags

---

## 🐞 Fehlerbehebungen
- Untertags wurden teilweise abgeschnitten → Layout korrigiert  
- Buttons waren nicht mehr mittig → neue Frame‑Struktur  
- Dropdown reagierte nicht korrekt auf Eingaben → stabilisierte Auto‑Complete‑Logik  
- Fokuswechsel ohne gültigen L1‑TAG → jetzt mit Fehlermeldung und Fokus‑Rücksprung  

---

## 📦 Download

Die kompilierten Versionen befinden sich im Abschnitt **Assets** dieses Releases:

- `ged_explorer.exe` (Windows, standalone)  
- Quellcode als `.zip` und `.tar.gz`

---

## 📚 Dokumentation

- **README.md** vollständig aktualisiert  
- **CHANGELOG.md** neu hinzugefügt  
- Modul‑Dokumentationen für `ged_explorer.py` und `ged_parser.py` unverändert gültig

---

## 👤 Autor

Dieter Eckstein – 2025/2026  
https://www.carosaar.de

