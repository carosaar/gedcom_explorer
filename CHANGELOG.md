# 📙 **CHANGELOG.md (neu)**

# Changelog – GEDCOM Explorer

Alle relevanten Änderungen am Projekt werden hier dokumentiert.

---

## [1.3] – 2026-03-24
### Added
- Auto‑Complete für L1‑TAG‑Eingabe
- Live‑Filterung der L1‑TAG‑Liste während der Eingabe
- ENTER‑Bestätigung für L1‑TAG
- automatische Validierung bei Fokusverlust
- Fehlermeldung bei ungültigem L1‑TAG
- Markieren des gesamten Inhalts beim Klick in das L1‑TAG‑Feld
- Mindesthöhe des Untertag‑Bereichs
- dynamische Anpassung des Untertag‑Bereichs an Fenstergröße
- zentrierter „Ausgabe“-Button durch neue Layoutstruktur
- neue Dateiendung `.gexp` für Definitionsdateien
- automatischer Vorschlagsname `<GEDCOM>_<L1‑TAG>.gexp`
- modernisiertes GUI‑Layout (kompakter, weniger Leerraum)

### Changed
- Bezeichnung „Hauptmerkmal (TAG)“ → „Hauptmerkmal (L1‑TAG)“
- Standardwert für CONT/CONC‑Vorschau: 0
- Definitionsdateien nicht mehr `.json`, sondern `.gexp`
- optimierte Fenstergeometrie
- überarbeiteter Info‑Dialog mit Versionshinweisen

### Fixed
- Untertag‑Liste wurde teilweise abgeschnitten → Layout korrigiert
- Buttons waren nicht mehr mittig → neue Frame‑Struktur
- Dropdown reagierte nicht korrekt auf Eingaben → stabilisierte Auto‑Complete‑Logik

---

## [1.2] – *internes Release, vollständig in 1.3 integriert*
### Added
- CONT/CONC‑Vorschau mit Zeichenlimit
- Trennzeichen für CONT/CONC
- automatische Ergänzung „(...)“ bei NOTE‑Tags
- Jahrgangsspalten bei DATE‑Tags
- Auswahl „Alle“ / „Keine“ Untertags

---

## [1.1.0] – 2025‑06‑02
### Initial Release
- vollständige GUI‑Anwendung
- CSV‑Erzeugung
- Untertag‑Auswahl
- CLI‑Modus
- JSON‑Definitionsdateien
