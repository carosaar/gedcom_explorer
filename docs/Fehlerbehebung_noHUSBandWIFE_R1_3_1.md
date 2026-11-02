# 🛠 Fehlerbehebungsdokumentation  
## Problem: Spalten **HUSB** und **WIFE** bleiben leer

### **Fehlerbeschreibung**

Beim Export der GEDCOM‑Daten in eine CSV‑Datei wurden die Spalten **HUSB** und **WIFE** nicht befüllt, obwohl die GEDCOM‑Datei gültige Einträge wie:

```
1 HUSB @I123@
1 WIFE @I456@
```

enthielt.

Die restlichen Daten (Untertags, L1‑TAG‑Werte, Jahrgangsspalten) wurden korrekt verarbeitet.  
Nur die Ehepartner‑Zeiger fehlten vollständig in der Ausgabe.

---

## **Ursache**

Der Parser behandelt **jeden** L1‑TAG gleich — auch solche, die nicht zum gesuchten Haupt‑TAG gehören.

Der relevante Codeblock:

```python
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
```

### **Problem im Ablauf**

1. `1 HUSB` wird eingelesen → `husb = "I123"`  
2. **Sofort danach** wird `flush_eintrag()` ausgeführt  
3. Da `HUSB` nicht der gesuchte L1‑TAG ist, wird der Eintrag verworfen  
4. Gleiches passiert bei `1 WIFE`  
5. Erst beim nächsten relevanten L1‑TAG (z. B. `1 BIRT`, `1 SOUR`, `1 MARR`) beginnt die echte Verarbeitung  
6. Zu diesem Zeitpunkt sind die Werte von `husb` und `wife` bereits verloren

### **Kurz gesagt:**  
Der Parser hat die Werte korrekt eingelesen, aber **vorzeitig wieder gelöscht**, bevor der Datensatz gespeichert wurde.

---

## **Lösung**

Der `flush_eintrag()`‑Aufruf muss **unterdrückt werden**, wenn der L1‑TAG lediglich HUSB oder WIFE ist.

### **Korrigierter Codeblock**

```python
if ebene == "1":
    if tag == "HUSB":
        husb = wert.strip("@")
        continue
    elif tag == "WIFE":
        wife = wert.strip("@")
        continue

    # Nur bei echten L1-TAGs flushen
    flush_eintrag()
    akt_untertagswerte = {}
    fortfuehrung_text_tags = set()
    aktueller_l1_tag = tag
    akt_l1_tag = wert.strip("@") if re.match(r"^@[^@]+@$", wert) else wert
    continue
```

### **Wirkung der Änderung**

- HUSB/WIFE werden eingelesen  
- Sie bleiben im Speicher erhalten  
- Sie werden erst beim nächsten relevanten L1‑TAG in die CSV geschrieben  
- Die Spalten erscheinen nun korrekt gefüllt

---

## **Ergebnis**

Nach der Anpassung werden die Spalten:

```
HUSB, WIFE
```

in der CSV‑Ausgabe korrekt befüllt — unabhängig davon, welcher L1‑TAG ausgewertet wird.

---

