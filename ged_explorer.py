# Version: 1.1.1
# Datum: 2025-06.02
# GUI- und CLI-Hybridmodul für ged_parser.py
# CLI-Start mit: python ged_explorer.py --konsole definitionsdatei.json
# * Layout Verbesserungen (minimale Fenstergröße)
# * alle Datensätze außer HEAD und TRLR erlaubt (Anpassung in ged_parser.py -> Version 1.0.2a)
# * Radiobuttons zur Auswahl aller oder keines Untertags
# * Ausgabe auch ohne Auswahl eines Untertags erlauben (mit Hinweis)
# * 1.1.1: L1-TAG "CHAN" wird einbezogen (Korrektur in Funktion finde_untertags())

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import argparse
import sys
from ged_parser import gedcom_explorer

if getattr(sys, 'frozen', False):
    # Wenn als EXE ausgeführt, Ressourcen aus dem temporären Verzeichnis laden
    base_path = sys._MEIPASS
else:
    # Im Interpreter: Ressourcen aus dem Projektverzeichnis laden
    base_path = os.path.abspath(".")

class GedTagGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GEDCOM Explorer – Version 1.1.1")
        self.root.geometry("800x600")
        self.root.minsize(width=600, height=600)
        self.dateipfad = ""
        self.level1_tags = []
        self.untertags_mapping = {}
        self.selected_tag = tk.StringVar()
        self.jahrgang_flag = tk.BooleanVar()
        self.checkbox_vars = {}
        self.entry_fields = {}
        self.nur_haupttag_auswahl = False
        self.definitionsdatei = ""
        self.defdatei_label_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Datei-Auswahl
        top_frame = tk.Frame(self.root, width=700, height=40)
        top_frame.pack(pady=10)
        top_frame.pack_propagate(False)
        tk.Label(top_frame, text="Gedcom-Datei:").pack(side=tk.LEFT, padx=(5, 5))
        entry_frame = tk.Frame(top_frame)
        entry_frame.pack(side=tk.LEFT, fill="x", expand=True)
        self.dateipfad_var = tk.StringVar()
        self.dateipfad_entry = tk.Entry(entry_frame, textvariable=self.dateipfad_var, state="readonly", relief="sunken", width=50)
        self.dateipfad_entry.pack(side=tk.TOP, fill="x", expand=True)
        scroll_x = tk.Scrollbar(entry_frame, orient="horizontal", command=self.dateipfad_entry.xview)
        scroll_x.pack(side=tk.BOTTOM, fill="x")
        self.dateipfad_entry.config(xscrollcommand=scroll_x.set)
        tk.Button(top_frame, text="📂 Öffnen", command=self.datei_waehlen).pack(side=tk.LEFT, padx=(10, 5))

        # Auswahl Dropdown
        auswahl_frame = tk.Frame(self.root)
        auswahl_frame.pack(pady=5)
        tk.Label(auswahl_frame, text="Wählen Sie ein Merkmal aus:").pack(side=tk.LEFT, padx=5)
        self.dropdown = ttk.Combobox(auswahl_frame, textvariable=self.selected_tag, state="readonly")
        self.dropdown.pack(side=tk.LEFT)
        self.dropdown.bind("<<ComboboxSelected>>", self.on_tag_selected)

        # Jahrgangs-Checkbox
        self.jahrgang_checkbox = tk.Checkbutton(self.root, text="Jahrgangsspalte bei Datum ausgeben", variable=self.jahrgang_flag)
        self.jahrgang_checkbox.pack(pady=5)

        # Untertags-Bereich
        self.untertags_label = tk.Label(self.root, text="Untertags-Auswahl")
        self.untertags_label.pack(pady=5)
        self.frame_untertags_rahmen = tk.LabelFrame(self.root, text="[  Auswahl der Detailmerkmale  ]")
        self.frame_untertags_rahmen.pack(padx=10, pady=5, fill="both", expand=True)
        self.frame_untertags = tk.Frame(self.frame_untertags_rahmen)
        self.frame_untertags.pack(padx=10, pady=10, fill="both", expand=True)

        # Radiobutton-Optionen (werden auch in zeige_untertags() nochmal erzeugt)
        self.untertags_option = tk.StringVar(value="Individuell")

        # Definitionsdatei-Bereich
        defdatei_frame = tk.Frame(self.root, width=700, height=40)
        defdatei_frame.pack(pady=5, fill="x")
        defdatei_frame.pack_propagate(False)
        tk.Label(defdatei_frame, text="Definitionsdatei:").pack(side=tk.LEFT, padx=(5, 5))
        entry_def_frame = tk.Frame(defdatei_frame)
        entry_def_frame.pack(side=tk.LEFT, fill="x", expand=True)
        self.defdatei_label_var = tk.StringVar()
        self.defdatei_entry = tk.Entry(entry_def_frame, textvariable=self.defdatei_label_var, state="readonly", relief="sunken", width=50)
        self.defdatei_entry.pack(side=tk.TOP, fill="x", expand=True)
        scroll_def_x = tk.Scrollbar(entry_def_frame, orient="horizontal", command=self.defdatei_entry.xview)
        scroll_def_x.pack(side=tk.BOTTOM, fill="x")
        self.defdatei_entry.config(xscrollcommand=scroll_def_x.set)
        buttons_def_frame = tk.Frame(defdatei_frame)
        buttons_def_frame.pack(side=tk.LEFT, padx=10)
        tk.Button(buttons_def_frame, text="📂 Laden", command=self.definition_laden).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_def_frame, text="💾 Speichern", command=self.definition_speichern).pack(side=tk.LEFT, padx=5)

        # Untere Button-Leiste
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        tk.Button(frame_bottom, text="ℹ️ Info", command=self.zeige_info).pack(side=tk.LEFT, padx=(0, 10))
        self.output_button = tk.Button(frame_bottom, text="📄 Ausgabe", command=self.daten_ausgeben)
        self.output_button.pack(side=tk.LEFT, expand=True)
        tk.Button(frame_bottom, text="❌ Beenden", command=self.root.quit).pack(side=tk.RIGHT, padx=(10, 0))

    def zeige_info(self):
        info_text = (
            "Dieses Programm dient dazu, strukturierte Daten aus GEDCOM-Dateien in eine csv-Datei zu extrahieren.\n"
            "Wählen Sie eine GEDCOM-Datei, dann ein Hauptmerkmal (TAG), und wählen Sie anschließend "
            "die relevanten Untertags und Spaltennamen.\nOptional kann eine Jahrgangsspalte erzeugt werden.\n\n"
            "- Es werden alle Datensätze verarbeitet.\n"
            "- Spalte 1 enthält immer den Datensatzzeiger\n"
            " Spalte 2 enthält immer den Datensatztyp INDI, FAM, SOUR, OBJ...\n"
            "- Zeiger werden ohne einschließende '@' gespeichert.\n\n"
            "- Speichern und Laden von Einstellungen\n (Definitionsdateien im JSON-Format).\n"
            "- Start als Konsolenprogramm mit einer Definitionsdatei\n Parameter: --konsole und \n"
            "- Die Zeiger HUSB und WIFE werden immer in den\n Spalte 3 und 4 eingetragen (soweit vorhanden).\n\n"
            "Neu in Version 1.0.2:\n"
            "- Verarbeitung allerDatensatztypen (bisher nur INDI und FAM)\n"
            "- Bearbeiten auch ohne Auswahl eines Untertag zulassen\n"
            "- Auswahlmöglichkeit Alle oder Kein Untertag\n\n"
            "© 2025 by Dieter Eckstein"
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
            self.dropdown.set("")
            self.untertags_mapping = {}
            self.zeige_untertags([])
            self.jahrgang_checkbox.config(state="disabled")
            self.definitionsdatei = ""
            self.defdatei_label_var.set("")

    def lese_level1_tags(self):
        tags = set()
        is_tag = False
        with open(self.dateipfad, "r", encoding="utf-8") as f:
            for zeile in f:
                if zeile.startswith("0 "):
                    parts = zeile.strip().split()
                    if len(parts) >= 3 and parts[2] not in ("HEAD", "TRLR"):
                        is_tag = True
                    else:
                        is_tag = False
                elif is_tag and zeile.startswith("1 "):
                    parts = zeile.strip().split()
                    if len(parts) >= 2 and parts[1] not in ("CONT", "CONC", "HUSB", "WIFE"):
                        tags.add(parts[1])
        return sorted(tags)

    def finde_untertags(self, tag):
        untertags = set()
        erfasse = False
        is_tag = False
        akt_tag = None
        prev_tags = ["", "", ""]
        with open(self.dateipfad, "r", encoding="utf-8") as f:
            for zeile in f:
                parts = zeile.strip().split(" ", 2)
                if len(parts) < 2:
                    continue
                ebene, curr_tag = parts[0], parts[1]
                if ebene == "0":
                    if len(parts) >= 3: # and parts[2] in ("INDI", "FAM"):
                        is_tag = True
                    else:
                        is_tag = False
                elif ebene == "1" and is_tag:
                    akt_tag = curr_tag
                    erfasse = (akt_tag == tag)
                    prev_tags = ["", "", ""]
                elif erfasse and ebene in ("2", "3", "4") and curr_tag not in ("CONT", "CONC"):
                    index = int(ebene) - 2
                    if index < len(prev_tags):
                        prev_tags[index] = curr_tag
                    strukturteile = prev_tags[:index] + [curr_tag]
                    struktur = ".".join(filter(None, strukturteile))
                    untertags.add(struktur)
        return sorted(untertags)

    def on_tag_selected(self, event):
        tag = self.selected_tag.get()
        if not tag:
            return
        untertags = self.finde_untertags(tag)
        if untertags:
            self.nur_haupttag_auswahl = False
            self.zeige_untertags(untertags)
            self.untertags_label.config(text="Untertags-Auswahl")
            hat_date = any("DATE" in u for u in untertags)
            if hat_date:
                self.jahrgang_checkbox.config(state="normal")
            else:
                self.jahrgang_checkbox.deselect()
                self.jahrgang_checkbox.config(state="disabled")
        else:
            self.nur_haupttag_auswahl = True
            self.zeige_untertags([])
            self.untertags_label.config(text="Keine Untertags für diesen TAG vorhanden.")
            self.jahrgang_checkbox.deselect()
            self.jahrgang_checkbox.config(state="disabled")

    def zeige_untertags(self, untertags):
        # Alles im Frame entfernen
        for widget in self.frame_untertags.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.entry_fields.clear()

        # Radiobuttons in eigenem Frame (mit pack)
        self.frame_options = tk.Frame(self.frame_untertags)
        self.frame_options.pack(anchor="w", pady=(0, 10))
        self.rb_alle = tk.Radiobutton(
            self.frame_options, text="Alle", variable=self.untertags_option, value="Alle",
            command=self.on_options_radiobutton_changed
        )
        self.rb_alle.pack(side="left", padx=5)
        self.rb_keine = tk.Radiobutton(
            self.frame_options, text="Keine", variable=self.untertags_option, value="Keine",
            command=self.on_options_radiobutton_changed
        )
        self.rb_keine.pack(side="left", padx=5)

        # Checkboxen und Entry-Felder in separatem Frame (mit grid)
        if not untertags:
            return

        self.frame_checkboxes = tk.Frame(self.frame_untertags)
        self.frame_checkboxes.pack(fill="both", expand=True)

        max_spalten = 3
        max_zeilen = 10

        for idx, struktur in enumerate(untertags):
            var = tk.BooleanVar()
            self.checkbox_vars[struktur] = var

            def make_callback(v=var):
                return lambda *args: self.on_checkbox_changed()
            var.trace_add("write", make_callback())

            zeile = idx % max_zeilen
            spalte = idx // max_zeilen

            cb = tk.Checkbutton(self.frame_checkboxes, text=struktur, variable=var)
            cb.grid(row=zeile, column=spalte*2, sticky="w")

            entry = tk.Entry(self.frame_checkboxes, width=15)
            entry.insert(0, struktur)
            entry.grid(row=zeile, column=spalte*2 + 1)
            self.entry_fields[struktur] = entry

        self.untertags_option.set("Individuell")

    def on_options_radiobutton_changed(self):
        option = self.untertags_option.get()
        if not self.checkbox_vars:
            return
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
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Datei und ein Merkmal aus.")
            return
        katalog = {}
        for struktur, var in self.checkbox_vars.items():
            if var.get():
                spaltenname = self.entry_fields[struktur].get().strip()
                if spaltenname:
                    katalog[struktur] = spaltenname
        # Falls keine Untertags gewählt wurden, Nutzer bestätigen lassen
        if not katalog and not self.nur_haupttag_auswahl:
            antwort = messagebox.askyesno(
                "Keine Untertags ausgewählt",
                "Sie haben keine Untertags ausgewählt.\n"
                "Möchten Sie wirklich fortfahren und nur den Haupttag exportieren?"
                )
            if not antwort:
                return  # Abbrechen        
        try:
            csv_datei = gedcom_explorer(self.dateipfad, self.selected_tag.get(), katalog, self.jahrgang_flag.get())
            messagebox.showinfo("Erfolg", f"CSV-Datei erfolgreich erstellt:\n{csv_datei}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Verarbeitung: {e}")

    def definition_speichern(self):
        if not self.dateipfad_var.get() or not self.selected_tag.get():
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine GEDCOM-Datei und einen Haupttag aus.")
            return
        gedcom_pfad = self.dateipfad_var.get()
        haupttag = self.selected_tag.get()
        untertags = {}
        for struktur, var in self.checkbox_vars.items():
            if var.get():
                spaltenname = self.entry_fields[struktur].get().strip()
                if spaltenname:
                    untertags[struktur] = spaltenname
        jahrgang_flag = self.jahrgang_flag.get()
        daten = {
            "gedcom_datei": gedcom_pfad,
            "haupttag": haupttag,
            "untertags": untertags,
            "jahrgang_flag": jahrgang_flag
        }
        start_dir = os.getcwd()
        basisname = os.path.splitext(os.path.basename(gedcom_pfad))[0]
        vorgeschlagener_name = f"{basisname}_{haupttag}.json"
        speicherpfad = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON-Dateien", "*.json")],
            initialdir=start_dir,
            initialfile=vorgeschlagener_name,
            title="Definitionsdatei speichern"
        )
        if speicherpfad:
            try:
                with open(speicherpfad, "w", encoding="utf-8") as f:
                    json.dump(daten, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Erfolg", f"Definitionsdatei gespeichert:\n{speicherpfad}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")

    def definition_laden(self):
        datei = filedialog.askopenfilename(
            filetypes=[("JSON-Dateien", "*.json")],
            initialdir=os.getcwd(),
            title="Definitionsdatei laden"
        )
        if datei:
            try:
                with open(datei, "r", encoding="utf-8") as f:
                    daten = json.load(f)
                gedcom_pfad = daten.get("gedcom_datei", "")
                haupttag = daten.get("haupttag", "")
                untertags = daten.get("untertags", {})
                jahrgang_flag = daten.get("jahrgang_flag", False)
                if gedcom_pfad:
                    self.dateipfad_var.set(gedcom_pfad)
                    self.dateipfad = gedcom_pfad
                    self.level1_tags = self.lese_level1_tags()
                    self.dropdown["values"] = self.level1_tags
                else:
                    messagebox.showwarning("Warnung", "Kein Pfad zur GEDCOM-Datei in der Definitionsdatei gefunden.")
                if haupttag:
                    self.selected_tag.set(haupttag)
                    self.on_tag_selected(None)
                    for struktur, var in self.checkbox_vars.items():
                        var.set(struktur in untertags)
                    for struktur, spaltenname in untertags.items():
                        if struktur in self.entry_fields:
                            self.entry_fields[struktur].delete(0, "end")
                            self.entry_fields[struktur].insert(0, spaltenname)
                else:
                    self.selected_tag.set("")
                    self.zeige_untertags([])
                self.jahrgang_flag.set(jahrgang_flag)
                if jahrgang_flag:
                    self.jahrgang_checkbox.select()
                else:
                    self.jahrgang_checkbox.deselect()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Definitionsdatei:\n{e}")

    def run(self):
        self.root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="GEDCOM-Explorer GUI/CLI")
    parser.add_argument('--konsole', metavar='DEFINITION.json', help='Starte im Konsolenmodus mit einer Definitionsdatei im JSON-Format')
    args = parser.parse_args()
    if args.konsole:
        json_pfad = args.konsole
        if not os.path.exists(json_pfad):
            print(f"Fehler: Definitionsdatei '{json_pfad}' wurde nicht gefunden.", file=sys.stderr)
            sys.exit(1)
        try:
            with open(json_pfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
            gedcom_pfad = daten.get("gedcom_datei", "")
            haupttag = daten.get("haupttag", "")
            untertags = daten.get("untertags", {})
            jahrgang_flag = daten.get("jahrgang_flag", False)
            if not gedcom_pfad or not os.path.exists(gedcom_pfad):
                print(f"Fehler: GEDCOM-Datei '{gedcom_pfad}' wurde nicht gefunden.", file=sys.stderr)
                sys.exit(1)
            csv_datei = gedcom_explorer(gedcom_pfad, haupttag, untertags, jahrgang_flag)
            print(f"CSV-Datei gespeichert unter: {csv_datei}")
        except Exception as e:
            print(f"Fehler bei der Verarbeitung: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        icon_path = os.path.join(base_path, "images", "prg_logo.ico")
        root = tk.Tk()
        root.iconbitmap(icon_path)
        app = GedTagGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
