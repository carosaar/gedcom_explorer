# ged_explorer.py – Version 1.3 (modernisiertes Layout)
# Datum: 2025-06-XX

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import argparse
import sys
from ged_parser import gedcom_explorer


class GedTagGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GEDCOM Explorer – Version 1.3")
        self.root.geometry("820x520")
        self.root.minsize(750, 500)

        # Variablen
        self.dateipfad = ""
        self.level1_tags = []
        self.selected_tag = tk.StringVar()
        self.jahrgang_flag = tk.BooleanVar()
        self.checkbox_vars = {}
        self.entry_fields = {}
        self.nur_haupttag_auswahl = False
        self.definitionsdatei = ""
        self.defdatei_label_var = tk.StringVar()

        # CONT/CONC-Optionen
        self.cont_preview_length_var = tk.IntVar(value=0)
        self.cont_separator_var = tk.StringVar(value=" ")

        self.create_widgets()


    # ---------------------------------------------------------
    # GUI-Elemente
    # ---------------------------------------------------------

    def create_widgets(self):


        # -----------------------------------------------------
        # Datei-Auswahl
        # -----------------------------------------------------
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=8, pady=4)

        ttk.Label(file_frame, text="GEDCOM-Datei:").pack(side="left", padx=4)
        self.dateipfad_var = tk.StringVar()
        self.dateipfad_entry = ttk.Entry(file_frame, textvariable=self.dateipfad_var)
        self.dateipfad_entry.pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(file_frame, text="📂 Öffnen", command=self.datei_waehlen).pack(side="left", padx=4)


        # -----------------------------------------------------
        # Haupttag-Auswahl
        # -----------------------------------------------------
        tag_frame = ttk.Frame(self.root)
        tag_frame.pack(fill="x", padx=8, pady=4)

        ttk.Label(tag_frame, text="Hauptmerkmal (L1-TAG):").pack(side="left", padx=4)
        self.dropdown = ttk.Combobox(tag_frame, textvariable=self.selected_tag)
        self.dropdown.bind("<Button-1>", self.select_all_l1)
        self.dropdown.bind("<FocusOut>", self.on_l1_focus_out)
        self.dropdown.bind("<Return>", self.confirm_l1_tag)
        self.dropdown.bind("<KeyRelease>", self.filter_l1_tags)        
        self.dropdown.pack(side="left", fill="x", expand=True, padx=4)
        self.dropdown.bind("<<ComboboxSelected>>", self.on_tag_selected)


        # -----------------------------------------------------
        # Optionen (Jahrgang + CONT/CONC)
        # -----------------------------------------------------
        option_frame = ttk.LabelFrame(self.root, text="Optionen")
        option_frame.pack(fill="x", padx=8, pady=4)

        # Jahrgang
        ttk.Checkbutton(
            option_frame,
            text="Jahrgangsspalten bei DATE-TAGs erzeugen",
            variable=self.jahrgang_flag
        ).grid(row=0, column=0, sticky="w", padx=4, pady=4)

        # CONT/CONC
        ttk.Label(option_frame, text="Max. CONT/CONC-Zeichen:").grid(row=1, column=0, sticky="w", padx=4)
        cont_combo = ttk.Combobox(
            option_frame,
            state="readonly",
            width=6,
            values=[0, 20, 50, 100],
            textvariable=self.cont_preview_length_var
        )
        cont_combo.grid(row=1, column=1, sticky="w", padx=4)

        ttk.Label(option_frame, text="Trennzeichen:").grid(row=1, column=2, sticky="w", padx=4)
        ttk.Entry(option_frame, textvariable=self.cont_separator_var, width=10).grid(row=1, column=3, sticky="w", padx=4)

        ttk.Label(option_frame, text='Fortsetzungszeichen "(...)" wird automatisch angefügt.').grid(
            row=1, column=4, sticky="w", padx=10
        )


        # -----------------------------------------------------
        # Untertags-Bereich
        # -----------------------------------------------------
        self.unter_frame = ttk.LabelFrame(self.root, text="Untertags")
        self.unter_frame.pack(fill="both", expand=True, padx=8, pady=4)

        # Mindesthöhe setzen
        self.unter_frame.configure(height=200)
        self.unter_frame.pack_propagate(True)
        # Radiobuttons
        self.untertags_option = tk.StringVar(value="Individuell")
        opt_frame = ttk.Frame(self.unter_frame)
        opt_frame.pack(anchor="w", pady=4)

        ttk.Radiobutton(opt_frame, text="Alle", variable=self.untertags_option, value="Alle",
                        command=self.on_options_radiobutton_changed).pack(side="left", padx=4)
        ttk.Radiobutton(opt_frame, text="Keine", variable=self.untertags_option, value="Keine",
                        command=self.on_options_radiobutton_changed).pack(side="left", padx=4)

        # Untertags-Container
        self.frame_checkboxes = ttk.Frame(self.unter_frame)
        self.frame_checkboxes.pack(anchor="nw", padx=4, pady=2)


        # -----------------------------------------------------
        # Definitionsdatei
        # -----------------------------------------------------
        def_frame = ttk.Frame(self.root)
        def_frame.pack(fill="x", padx=8, pady=4)

        ttk.Label(def_frame, text="Definitionsdatei:").pack(side="left", padx=4)
        self.defdatei_entry = ttk.Entry(def_frame, textvariable=self.defdatei_label_var)
        self.defdatei_entry.pack(side="left", fill="x", expand=True, padx=4)

        ttk.Button(def_frame, text="📂 Laden", command=self.definition_laden).pack(side="left", padx=4)
        ttk.Button(def_frame, text="💾 Speichern", command=self.definition_speichern).pack(side="left", padx=4)


        # -----------------------------------------------------
        # Untere Button-Leiste
        # -----------------------------------------------------
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x", padx=8, pady=(4, 6), anchor="s")

        # Linker Bereich
        left_frame = ttk.Frame(bottom)
        left_frame.pack(side="left", anchor="w")
        ttk.Button(left_frame, text="ℹ️ Info", command=self.zeige_info).pack(side="left", padx=4)

        # Mittlerer Bereich (zentriert)
        center_frame = ttk.Frame(bottom)
        center_frame.pack(side="left", expand=True)
        ttk.Button(center_frame, text="📄 Ausgabe", command=self.daten_ausgeben).pack(padx=4)

        # Rechter Bereich
        right_frame = ttk.Frame(bottom)
        right_frame.pack(side="right", anchor="e")
        ttk.Button(right_frame, text="❌ Beenden", command=self.root.quit).pack(side="right", padx=4)

    # ---------------------------------------------------------
    # Untertags anzeigen (10 pro Spalte)
    # ---------------------------------------------------------

    def zeige_untertags(self, untertags):

        for widget in self.frame_checkboxes.winfo_children():
            widget.destroy()

        self.checkbox_vars.clear()
        self.entry_fields.clear()

        if not untertags:
            return

        max_zeilen = 10

        for idx, struktur in enumerate(untertags):
            var = tk.BooleanVar()
            self.checkbox_vars[struktur] = var

            def make_callback(v=var):
                return lambda *args: self.on_checkbox_changed()
            var.trace_add("write", make_callback())

            zeile = idx % max_zeilen
            spalte = idx // max_zeilen

            ttk.Checkbutton(self.frame_checkboxes, text=struktur, variable=var).grid(
                row=zeile, column=spalte * 2, sticky="w", padx=2, pady=1
            )

            entry = ttk.Entry(self.frame_checkboxes, width=18)
            entry.insert(0, struktur)
            entry.grid(row=zeile, column=spalte * 2 + 1, sticky="w", padx=(0, 10), pady=1)
            self.entry_fields[struktur] = entry

        # Spaltenbreite stabilisieren
        for col in range((len(untertags) // max_zeilen + 1) * 2):
            self.frame_checkboxes.grid_columnconfigure(col, minsize=160)


    # ---------------------------------------------------------
    # Restliche Funktionen (unverändert)
    # ---------------------------------------------------------

    def zeige_info(self):
        info_text = (
            "Dieses Programm dient dazu, strukturierte Daten aus GEDCOM-Dateien in eine csv-Datei zu extrahieren.\n"
            "Wählen Sie eine GEDCOM-Datei, dann ein Hauptmerkmal (L1-TAG), und wählen Sie anschließend "
            "die relevanten Untertags und Spaltennamen.\nOptional können Jahrgangsspalten bei DATE-TAGs erzeugt werden.\n\n"
            "- Es werden alle Datensätze verarbeitet.\n"
            "- Spalte 1 enthält immer den Datensatzzeiger\n"
            "  Spalte 2 enthält immer den Datensatztyp INDI, FAM, SOUR, OBJ...\n"
            "- Zeiger werden ohne einschließende '@' gespeichert.\n"
            "- Speichern und Laden von Einstellungen\n  (Definitionsdateien im GEXP-Format).\n"
            "- Start als Konsolenprogramm mit einer Definitionsdatei\n  Parameter: --konsole\n"
            "- Die Zeiger HUSB und WIFE werden immer in den\n  Spalten 3 und 4 eingetragen (soweit vorhanden).\n\n"
            "Neu in Version 1.3.0:\n"
            "- NOTE.CONT/CONC-Vorschau mit begrenzter Zeichenzahl und Trennzeichen\n"
            "- Modernisiertes, kompakteres Layout\n"
            "- Neue Dateiendung für Definitionsdateien: .gexp\n\n"
            "© 2025-2026 by Dieter Eckstein"
        )
        messagebox.showinfo("Info", info_text)

    def datei_waehlen(self):
        datei = filedialog.askopenfilename(filetypes=[["GEDCOM Dateien", "*.ged"]])
        if datei:
            self.dateipfad = datei
            self.dateipfad_var.set(datei)
            self.level1_tags = self.lese_level1_tags()
            self.dropdown["values"] = self.level1_tags
            self.selected_tag.set("")
            self.zeige_untertags([])
            self.jahrgang_flag.set(False)

    def lese_level1_tags(self):
        tags = set()
        is_tag = False
        with open(self.dateipfad, "r", encoding="utf-8") as f:
            for zeile in f:
                if zeile.startswith("0 "):
                    parts = zeile.strip().split()
                    is_tag = len(parts) >= 3 and parts[2] not in ("HEAD", "TRLR")
                elif is_tag and zeile.startswith("1 "):
                    parts = zeile.strip().split()
                    if len(parts) >= 2 and parts[1] not in ("CONT", "CONC", "HUSB", "WIFE"):
                        tags.add(parts[1])
        return sorted(tags)

    def finde_untertags(self, tag):
        untertags = set()
        erfasse = False
        is_tag = False
        prev_tags = ["", "", ""]
        with open(self.dateipfad, "r", encoding="utf-8") as f:
            for zeile in f:
                parts = zeile.strip().split(" ", 2)
                if len(parts) < 2:
                    continue
                ebene, curr_tag = parts[0], parts[1]
                if ebene == "0":
                    is_tag = len(parts) >= 3
                elif ebene == "1" and is_tag:
                    erfasse = (curr_tag == tag)
                    prev_tags = ["", "", ""]
                elif erfasse and ebene in ("2", "3", "4") and curr_tag not in ("CONT", "CONC"):
                    index = int(ebene) - 2
                    if index < len(prev_tags):
                        prev_tags[index] = curr_tag
                    strukturteile = prev_tags[:index] + [curr_tag]
                    untertags.add(".".join(filter(None, strukturteile)))
        return sorted(untertags)

    def on_tag_selected(self, event):
        tag = self.selected_tag.get()
        if not tag:
            return
        untertags = self.finde_untertags(tag)
        self.zeige_untertags(untertags)

    def filter_l1_tags(self, event):
        # Tasten, bei denen wir NICHT autovervollständigen
        ignore_keys = ("Up", "Down", "Left", "Right", "Return", "Tab", "Escape")
        edit_keys = ("BackSpace", "Delete")

        # aktueller Text, den der Benutzer sieht
        eingabe = self.dropdown.get()
        eingabe_upper = eingabe.upper()

        # komplette Liste
        alle_tags = self.level1_tags

        # Wenn nichts eingegeben ist: komplette Liste anzeigen
        if eingabe == "":
            self.dropdown["values"] = alle_tags
            return

        # Prefix-Filter: nur Tags, die mit der Eingabe beginnen
        treffer = [tag for tag in alle_tags if tag.upper().startswith(eingabe_upper)]

        # Wenn keine Treffer: Liste nicht leeren, sondern alles anzeigen
        if not treffer:
            self.dropdown["values"] = alle_tags
            return

        # Gefilterte Liste setzen
        self.dropdown["values"] = treffer

        # Bei Navigations-/Edit-Tasten kein Auto-Complete erzwingen
        if event.keysym in ignore_keys or event.keysym in edit_keys:
            return

        # Auto-Complete: ersten Treffer nehmen und nur ergänzen
        erster = treffer[0]

        # Wenn der erste Treffer genau der Eingabe entspricht → nichts ergänzen
        if erster.upper() == eingabe_upper:
            return

        # Inhalt auf ersten Treffer setzen
        self.dropdown.delete(0, tk.END)
        self.dropdown.insert(0, erster)

        # Nur den ergänzten Teil markieren
        self.dropdown.icursor(len(eingabe))
        self.dropdown.select_range(len(eingabe), tk.END)    

    def confirm_l1_tag(self, event=None):
        eingabe = self.dropdown.get().upper()

        # Wenn Eingabe leer → nichts tun
        if not eingabe:
            return

        # Trefferliste wie beim Filtern
        treffer = [tag for tag in self.level1_tags if tag.upper().startswith(eingabe)]

        # Wenn es Treffer gibt → ersten übernehmen
        if treffer:
            self.dropdown.set(treffer[0])
            self.selected_tag.set(treffer[0])
            self.on_tag_selected(None)

    def on_l1_focus_out(self, event=None):
        eingabe = self.dropdown.get().strip().upper()

        # Leeres Feld → nichts tun
        if eingabe == "":
            return

        # Prüfen, ob Eingabe ein gültiger L1-TAG ist
        gueltige_tags = [tag.upper() for tag in self.level1_tags]

        if eingabe in gueltige_tags:
            # gültig → Untertags laden
            self.selected_tag.set(eingabe)
            self.on_tag_selected(None)
        else:
            # ungültig → Fehlermeldung und Fokus zurück
            messagebox.showerror(
                "Ungültiger L1-TAG",
                f"'{eingabe}' ist kein gültiger L1-TAG.\nBitte einen gültigen Wert eingeben."
            )
            # Fokus zurück auf das Feld
            self.dropdown.focus_set()
            # Markieren, damit der Benutzer direkt überschreiben kann
            self.dropdown.select_range(0, tk.END)


    def select_all_l1(self, event=None):
        # Markiert den gesamten Inhalt, sobald in das Feld geklickt wird
        self.dropdown.after(1, lambda: self.dropdown.select_range(0, tk.END))



    def on_options_radiobutton_changed(self):
        option = self.untertags_option.get()
        if option == "Alle":
            for var in self.checkbox_vars.values():
                var.set(True)
        elif option == "Keine":
            for var in self.checkbox_vars.values():
                var.set(False)

    def on_checkbox_changed(self):
        werte = [var.get() for var in self.checkbox_vars.values()]
        if all(werte):
            self.untertags_option.set("Alle")
        elif not any(werte):
            self.untertags_option.set("Keine")
        else:
            self.untertags_option.set("Individuell")

    def daten_ausgeben(self):
        if not self.dateipfad or not self.selected_tag.get():
            messagebox.showwarning("Warnung", "Bitte Datei und TAG wählen.")
            return

        katalog = {
            struktur: self.entry_fields[struktur].get().strip()
            for struktur, var in self.checkbox_vars.items()
            if var.get()
        }

        try:
            csv_datei = gedcom_explorer(
                self.dateipfad,
                self.selected_tag.get(),
                katalog,
                self.jahrgang_flag.get(),
                cont_preview_length=self.cont_preview_length_var.get(),
                cont_separator=self.cont_separator_var.get()
            )
            messagebox.showinfo("Erfolg", f"CSV-Datei erstellt:\n{csv_datei}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def definition_speichern(self):
        if not self.dateipfad or not self.selected_tag.get():
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine GEDCOM-Datei und ein L1-TAG aus.")
            return

        gedcom_pfad = self.dateipfad
        haupttag = self.selected_tag.get()

        # Basisname der GEDCOM-Datei
        basisname = os.path.splitext(os.path.basename(gedcom_pfad))[0]

        # Neuer vorgeschlagener Dateiname
        vorgeschlagener_name = f"{basisname}_{haupttag}.gexp"

        daten = {
            "gedcom_datei": gedcom_pfad,
            "haupttag": haupttag,
            "untertags": {
                struktur: self.entry_fields[struktur].get().strip()
                for struktur, var in self.checkbox_vars.items()
                if var.get()
            },
            "jahrgang_flag": self.jahrgang_flag.get(),
            "cont_preview_length": self.cont_preview_length_var.get(),
            "cont_separator": self.cont_separator_var.get()
        }

        pfad = filedialog.asksaveasfilename(
            defaultextension=".gexp",
            filetypes=[("GEDCOM Explorer Definition", "*.gexp")],
            initialfile=vorgeschlagener_name,
            title="Definitionsdatei speichern"
        )

        if pfad:
            with open(pfad, "w", encoding="utf-8") as f:
                json.dump(daten, f, indent=2, ensure_ascii=False)
            self.defdatei_label_var.set(pfad)    
        daten = {
            "gedcom_datei": self.dateipfad,
            "haupttag": self.selected_tag.get(),
            "untertags": {
                struktur: self.entry_fields[struktur].get().strip()
                for struktur, var in self.checkbox_vars.items()
                if var.get()
            },
            "jahrgang_flag": self.jahrgang_flag.get(),
            "cont_preview_length": self.cont_preview_length_var.get(),
            "cont_separator": self.cont_separator_var.get()
        }

        pfad = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title="Definitionsdatei speichern"
        )
        if pfad:
            with open(pfad, "w", encoding="utf-8") as f:
                json.dump(daten, f, indent=2, ensure_ascii=False)
            self.defdatei_label_var.set(pfad)


    def definition_laden(self):
        pfad = filedialog.askopenfilename(filetypes=[("GEDCOM Explorer Definition", "*.gexp")])
        if not pfad:
            return

        with open(pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)

        self.dateipfad = daten["gedcom_datei"]
        self.dateipfad_var.set(self.dateipfad)
        self.level1_tags = self.lese_level1_tags()
        self.dropdown["values"] = self.level1_tags

        self.selected_tag.set(daten["haupttag"])
        self.on_tag_selected(None)

        for struktur, var in self.checkbox_vars.items():
            var.set(struktur in daten["untertags"])

        for struktur, name in daten["untertags"].items():
            if struktur in self.entry_fields:
                self.entry_fields[struktur].delete(0, "end")
                self.entry_fields[struktur].insert(0, name)

        self.jahrgang_flag.set(daten.get("jahrgang_flag", False))
        self.cont_preview_length_var.set(daten.get("cont_preview_length", 50))
        self.cont_separator_var.set(daten.get("cont_separator", " "))

        self.defdatei_label_var.set(pfad)


# ---------------------------------------------------------
# CLI-Modus
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="GEDCOM-Explorer GUI/CLI")
    parser.add_argument('--konsole', metavar='DEFINITION.json')
    args = parser.parse_args()

    if args.konsole:
        with open(args.konsole, "r", encoding="utf-8") as f:
            daten = json.load(f)

        csv_datei = gedcom_explorer(
            daten["gedcom_datei"],
            daten["haupttag"],
            daten["untertags"],
            daten["jahrgang_flag"],
            cont_preview_length=daten.get("cont_preview_length", 50),
            cont_separator=daten.get("cont_separator", " ")
        )
        print("CSV-Datei erstellt:", csv_datei)
    else:
        root = tk.Tk()
        app = GedTagGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()