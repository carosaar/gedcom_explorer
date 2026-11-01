
# 📙 Changelog – GEDCOM Explorer

Alle relevanten Änderungen am Projekt werden hier dokumentiert.

Das Format orientiert sich an „Keep a Changelog“.

---

## [1.3.1] – 2026‑03‑24

### Fixed
- **HUSB/WIFE‑Spalten wurden nicht befüllt**  
  Ursache: `flush_eintrag()` wurde bei jedem L1‑TAG ausgeführt, auch bei `HUSB` und `WIFE`.  
  Dadurch wurden die eingelesenen Werte vorzeitig verworfen, bevor der relevante L1‑TAG verarbeitet wurde.  
  Lösung: `flush_eintrag()` wird nun **nicht mehr** bei `HUSB` und `WIFE` ausgeführt; die Werte bleiben erhalten und werden korrekt in die CSV übernommen.

---

## [1.3] – 2026-03-24

### Added
- Auto-Complete und Live-Filterung für L1-TAG-Eingabe  
- Validierung von L1-TAGs mit Fehlermeldung  
- Verbesserte Untertag-Darstellung (dynamisch, kein Abschneiden)  
- Neues Format `.gexp` für Definitionsdateien  
- Automatische Namensvergabe für Definitionsdateien  
- Überarbeitetes GUI-Layout  

### Changed
- Bezeichnung „Hauptmerkmal (TAG)“ → „Hauptmerkmal (L1-TAG)“  
- Standardwert für CONT/CONC-Vorschau angepasst  
- Optimierte Fenstergeometrie  
- Verbesserter Info-Dialog  

### Fixed
- Layoutprobleme bei Untertags behoben  
- Zentrierung von Buttons korrigiert  
- Stabilere Auto-Complete-Funktion  

---

## [1.2] – internes Release (in 1.3 enthalten)

### Added
- CONT/CONC-Vorschau mit Zeichenlimit  
- Trennzeichen für CONT/CONC  
- Automatische Ergänzung „(...)“ bei NOTE-Tags  
- Jahrgangsspalten für DATE-Tags  
- Auswahl „Alle / Keine“ für Untertags  

---

## [1.1.0] – 2025-06-02

### Added
- Erste Version der GUI-Anwendung  
- CSV-Export  
- Untertag-Auswahl  
- CLI-Modus  
- JSON-basierte Definitionsdateien  