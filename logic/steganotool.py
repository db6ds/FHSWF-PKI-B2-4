#############################
# Steganographie-Tool 
# Author: Daniel Stabenau
# Mat-Nr: 71300017
# Gruppe: B2-4
# verwendete Hilfsmittel bei der
# Codeerstellung und Debugging
# ollama, mixtral, claude.ai und chatgpt
##############################

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SteganographyTool:
    """
    Eine GUI-Anwendung zum Verstecken und Extrahieren von Daten in PNG-Bildern mittels LSB-Steganographie.
    
    Diese Klasse implementiert eine komplette Steganographie-Lösung mit folgenden Hauptfunktionen:
    - Verstecken von Text oder Dateien in PNG-Bildern
    - Extrahieren versteckter Daten aus präparierten Bildern
    - Analyse von Bildern auf versteckte Daten
    - Visualisierung der LSB-Verteilung und Differenzanalyse
    
    Die Steganographie erfolgt durch Manipulation der Least Significant Bits (LSB) der Bildpixel.
    """

    def __init__(self, root):
        """
        Initialisiert die Steganographie-Anwendung.
        
        Args:
            root: Das Hauptfenster der Tkinter-Anwendung
            
        Die Methode erstellt alle GUI-Elemente und initialisiert die grundlegenden Variablen
        für die Steganographie-Funktionalität.
        """
        # Grundlegende Fenster-Konfiguration
        self.main_root = root  # Speichere das Hauptfenster
        self.window = None     # Fenster für das Tool
        self.analyse_window = None # Analyse Fenster
        self.display_window = None
        self.canvas= None
        self.fig=None

    def ausfuehren(self, img_path):
        self.img_path = img_path # Pfad übergeben
        #print (img_path)

        # Wenn bereits ein Fenster offen ist, bringe es in den Vordergrund
        if self.window is not None and tk.Toplevel.winfo_exists(self.window):
            self.window.lift()
            self.window.focus_force()
            return
            
        # Erstelle neues Fenster
        self.window = tk.Toplevel(self.main_root)
        self.window.title("Steganographie Tool")
        self.window.geometry("1100x1000") # Festgelegte Fenstergröße
        self.window.resizable(False,False)# Fixe Fenstergröße
 

        # Variablen für die Dateiverwaltung
        self.current_file = None     # Pfad zum aktuell geladenen Bild
        self.secret_file = None      # Pfad zur zu versteckenden Datei
        self.available_bytes = 0     # Verfügbare Bytes für Steganographie
        
        # Steuerungsvariablen für die GUI
        self.input_method = tk.StringVar(value="text")  # Auswahl: Text oder Datei-Modus
        
        # GUI-Layout konfigurieren
        self._configure_grid()
        
        # GUI-Elemente erstellen
        self.create_file_selection_frame()  # Frame für Dateiauswahl
        self.create_info_frame()           # Frame für Bildinformationen
        self.create_content_frame()        # Frame für Texteingabe
        self.create_button_frame()         # Frame für Steuerungsbuttons
        self.create_selection_frame()      # Frame für Modusauswahl
        
        # Initialen GUI-Zustand setzen
        self.set_initial_state()

        # Überprüfe ob schon Datei im Main ausgewählt wurde
        if self.img_path:
            self.current_file = self.img_path
            self.get_file_info()

    def _configure_grid(self):
        """
        Konfiguriert das Grid-Layout des Hauptfensters.
        
        Legt die Größenverhältnisse und minimalen Größen der Spalten und Zeilen fest:
        - Spalte 0: Hauptbereich (weight=1, min=700px)
        - Spalte 1: Seitenbereich (min=400px)
        - Zeile 1: Hauptbereich (weight=1, min=400px)
        - Zeile 3: Unterer Bereich (weight=1)
        """
        self.window.grid_columnconfigure(0, weight=1, minsize=700)  # Hauptbereich
        self.window.grid_columnconfigure(1, weight=0, minsize=400)  # Seitenbereich
        self.window.grid_columnconfigure(2, weight=0)               # Zusätzlicher Bereich
        self.window.grid_rowconfigure(1, weight=1, minsize=400)    # Hauptbereich Höhe
        self.window.grid_rowconfigure(3, weight=1)                 # Unterer Bereich

    def set_initial_state(self):
        """
        Setzt den initialen Zustand aller GUI-Elemente.
        
        Deaktiviert alle Steuerelemente bis ein Bild geladen wird:
        - Info-Textfeld (read-only)
        - Texteingabefeld
        - Alle Steuerungsbuttons außer Bildauswahl
        - Radio-Buttons für Moduswahl
        """
        # Deaktiviere Informationsanzeige
        self.info_text.config(state=tk.DISABLED)
        
        # Deaktiviere Texteingabe
        self.text_input.config(state=tk.DISABLED)
        
        # Deaktiviere Steuerungsbuttons
        self.select_button.config(state=tk.DISABLED)
        self.encode_button.config(state=tk.DISABLED)
        self.decode_button.config(state=tk.DISABLED)
        
        # Deaktiviere Modusauswahl
        for radio in self.radio_buttons:
            radio.config(state=tk.DISABLED)

    def toggle_input_method(self):
        """
        Steuert die Aktivierung/Deaktivierung der GUI-Elemente basierend auf der gewählten Eingabemethode.
        
        Text-Modus:
        - Aktiviert Texteingabefeld
        - Deaktiviert Dateiauswahl-Button
        - Aktiviert Encode-Button
        
        Datei-Modus:
        - Deaktiviert Texteingabefeld
        - Aktiviert Dateiauswahl-Button
        - Encode-Button wird erst nach Dateiauswahl aktiviert
        """
        current_mode = self.input_method.get()
        
        if current_mode == "text":
            # Konfiguration für Text-Modus
            self.text_input.config(state=tk.NORMAL)      # Aktiviere Textfeld
            self.select_button.config(state=tk.DISABLED) # Deaktiviere Dateiauswahl
            self.encode_button.config(state=tk.NORMAL)   # Aktiviere Encoding
        else:
            # Konfiguration für Datei-Modus
            self.text_input.config(state=tk.DISABLED)    # Deaktiviere Textfeld
            self.select_button.config(state=tk.NORMAL)   # Aktiviere Dateiauswahl
            self.encode_button.config(state=tk.DISABLED) # Encode erst nach Dateiauswahl

    def create_file_selection_frame(self):
        """
        Erstellt den Frame für die primäre Bildauswahl der Anwendung.
        
        Dieser Frame enthält:
        - Einen Button zum Öffnen des Dateiauswahl-Dialogs für das Trägerbild
        
        Der Frame wird in der obersten Zeile des Hauptfensters platziert und
        erstreckt sich über zwei Spalten, um eine prominente Position zu gewährleisten.
        
        Technische Details:
        - Verwendet ttk.Frame für konsistentes Erscheinungsbild
        - Nutzt grid-Layout mit sticky="ew" für horizontale Ausdehnung
        - Button ruft open_file('normal') über Lambda-Funktion auf
        """
        # Erstelle einen ttk.Frame für konsistentes Design
        file_frame = ttk.Frame(self.window)
        
        # Positioniere den Frame im Grid-Layout
        # row=0: Oberste Zeile
        # columnspan=2: Erstreckt sich über zwei Spalten
        # padx/pady=5: Äußerer Abstand für besseres Layout
        # sticky="ew": Dehnt sich horizontal aus
        file_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Erstelle den Button zur Bildauswahl
        # Lambda-Funktion ermöglicht Übergabe des 'normal' Parameters an open_file
        self.file_Load_button = ttk.Button(
            file_frame,                          # Parent-Widget
            text="Bild auswählen",              # Button-Beschriftung
            command=lambda : self.open_file('normal')  # Callback-Funktion
        )


        # Positioniere den Button im Frame
        # side="left": Linksbündige Ausrichtung
        # padx=5: Horizontaler Abstand zu anderen Elementen
        self.file_Load_button.pack(side="left", padx=5)

    def create_info_frame(self):
        """
        Erstellt den Frame für die Bildvorschau und zugehörige Informationen.
        
        Dieser Frame besteht aus zwei Hauptkomponenten:
        1. Informations-Textfeld:
        - Zeigt Details zum geladenen Bild (Format, Größe, Kapazität)
        - Zeigt Ergebnisse der Steganographie-Analyse
        - Read-only Modus für Benutzer
        
        2. Bildvorschau-Bereich:
        - Zeigt eine skalierte Vorschau des geladenen Bildes
        - Platzhaltertext "IMG" wenn kein Bild geladen ist
        - Maximalgröße 380x380 Pixel
        
        Layout:
        - Informations-Textfeld links (Spalte 0)
        - Bildvorschau rechts (Spalte 1)
        - Beide in Zeile 1 des Hauptfensters
        """
        # Frame für Bildinformationen erstellen
        info_frame = ttk.Frame(self.window)
        # Positionierung: Zeile 1, Spalte 0, eine Spalte breit
        # sticky="ew" für horizontale Ausdehnung
        info_frame.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="ew")
        
        # Textfeld für Bildinformationen
        # height=12: Höhe in Textzeilen
        # width=1: Minimale Breite (wird durch sticky="ew" automatisch angepasst)
        self.info_text = tk.Text(info_frame, height=12, width=1)
        # fill="both", expand=True für vollständige Ausnutzung des verfügbaren Platzes
        self.info_text.pack(fill="both", expand=True)

        # Frame für Bildvorschau erstellen
        # borderwidth=1, relief="solid" erzeugt einen sichtbaren Rahmen
        self.img_frame = ttk.Frame(self.window, borderwidth=1, relief="solid")
        # Positionierung: Zeile 1, Spalte 1
        # sticky="nsew" für Ausdehnung in alle Richtungen
        self.img_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # Label für Bildvorschau/Platzhalter
        # Anfangs nur mit Text "IMG", wird später durch Bildvorschau ersetzt
        self.img_label = ttk.Label(self.img_frame, text="IMG")
        # Zentrierte Positionierung im Frame mittels place
        # relx/rely=0.5: Position bei 50% der Framegröße
        # anchor="center": Zentriert das Label an dieser Position
        self.img_label.place(relx=0.5, rely=0.5, anchor="center")

    def create_content_frame(self):
        """
        Erstellt den Frame für die Eingabe der zu versteckenden Daten.
        
        Dieser Frame enthält ein Textfeld für:
        - Direkte Texteingabe im Text-Modus
        - Anzeige extrahierter Daten beim Dekodieren
        
        Layout-Details:
        - Positioniert in Zeile 3, Spalte 0 des Hauptfensters
        - Nutzt die volle verfügbare Breite und Höhe
        - Scrollbares Textfeld mit fester Höhe von 25 Zeilen
        
        Eigenschaften:
        - Das Textfeld ist initial deaktiviert
        - Wird aktiviert/deaktiviert basierend auf dem gewählten Eingabemodus
        - Automatische Anpassung an die Framegröße
        
        Hinweis:
        Die ursprüngliche Implementierung enthielt auskommentierte Komponenten
        für einen separaten Datei-Input-Frame, der für zukünftige Erweiterungen 
        genutzt werden könnte.
        """
        # Hauptframe für den Content-Bereich
        content_frame = ttk.Frame(self.window)
        # Positionierung im Grid:
        # row=3: Unterer Bereich des Fensters
        # sticky="nsew": Ausdehnung in alle Richtungen
        content_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        
        # Frame für das Textfeld
        self.text_frame = ttk.Frame(content_frame)
        
        # Textfeld für Eingabe/Ausgabe
        self.text_input = tk.Text(
            self.text_frame,
            height=25,         # Höhe in Textzeilen
            width=40          # Breite in Zeichen
        )
        # Packen des Textfelds mit voller Ausnutzung des verfügbaren Platzes
        self.text_input.pack(fill="both", expand=True)
        
        # Packen des Text-Frames in den Content-Frame
        self.text_frame.pack(fill="both", expand=True)

    def create_button_frame(self):
        """
        Erstellt den Frame für die Steuerungsbuttons der Anwendung.
        
        Dieser Frame enthält vier Hauptbuttons:
        1. Analyse-Button:
        - Startet die LSB-Analyse des Bildes
        - Initial aktiviert
        - Zeigt Verteilungen und Statistiken
        
        2. Select-Button:
        - Öffnet Dateiauswahl für zu versteckende Dateien
        - Nur im Datei-Modus aktiv
        - Prüft automatisch Dateigrößenbeschränkungen
        
        3. Encode-Button:
        - Startet den Versteck-Prozess
        - Initial deaktiviert
        - Wird aktiviert wenn:
            * Im Text-Modus: Nach Bildauswahl
            * Im Datei-Modus: Nach erfolgreicher Dateiauswahl
        
        4. Decode-Button:
        - Extrahiert versteckte Daten
        - Wird aktiviert sobald ein Bild geladen ist
        - Erkennt automatisch den korrekten Ausgabemodus
        
        Layout:
        - Vertikal angeordnete Buttons
        - Positioniert in der rechten Spalte des Hauptfensters
        - Einheitliche Abstände zwischen den Buttons
        """
        # Erstelle den Frame für die Buttons
        button_frame = ttk.Frame(self.window)
        # Positionierung rechts oben im Hauptfenster
        # sticky="n": Am oberen Rand ausgerichtet
        button_frame.grid(row=3, column=1, padx=5, pady=5, sticky="n")

        # Analyse-Button
        # Ermöglicht detaillierte LSB-Analyse des Bildes
        self.analyse_button = ttk.Button(
            button_frame,
            text="Analyse",
            command=self.analyse_image,
            state=tk.NORMAL  # Initial aktiviert
        )
        self.analyse_button.pack(pady=2)  # Vertikaler Abstand 2 Pixel

        # Select-Button für Dateiauswahl
        # Wird für die Auswahl der zu versteckenden Datei verwendet
        self.select_button = ttk.Button(
            button_frame,
            text="Select",
            command=lambda: self.open_file('stegofile'),  # Öffnet Dateiauswahl im Stegofile-Modus
            state=tk.NORMAL  # Initial aktiviert
        )
        self.select_button.pack(pady=2)

        # Encode-Button zum Starten des Versteck-Prozesses
        self.encode_button = ttk.Button(
            button_frame,
            text="Encodieren",
            command=self.encode,  # Ruft die Encode-Methode auf
            state=tk.DISABLED    # Initial deaktiviert
        )
        self.encode_button.pack(pady=2)
        
        # Decode-Button zum Extrahieren versteckter Daten
        self.decode_button = ttk.Button(
            button_frame,
            text="Decodieren",
            command=self.decode,  # Ruft die Decode-Methode auf
            state=tk.DISABLED    # Initial deaktiviert
        )
        self.decode_button.pack(pady=2)

    def create_selection_frame(self):
        """
        Erstellt den Frame für die Auswahl des Betriebsmodus der Anwendung.
        
        Implementiert zwei Radio-Buttons für die Modi:
        1. Text-Modus:
        - Ermöglicht direkte Texteingabe im Textfeld
        - Aktiviert das Textfeld
        - Deaktiviert den Select-Button
        - Encode-Button direkt verfügbar
        
        2. Datei-Modus:
        - Ermöglicht das Verstecken von Dateien
        - Deaktiviert das Textfeld
        - Aktiviert den Select-Button für Dateiauswahl
        - Encode-Button erst nach Dateiauswahl verfügbar
        
        Layout:
        - Horizontal angeordnete Radio-Buttons
        - Mittig im Hauptfenster positioniert
        - Erstreckt sich über zwei Spalten
        
        Technische Details:
        - Nutzt tkinter StringVar für die Zustandsverwaltung
        - Initial auf "text" gesetzt
        - Buttons initial deaktiviert (werden nach Bildauswahl aktiviert)
        - Toggle-Funktion als Callback für Zustandsänderungen
        """
        # Erstelle Frame für die Modusauswahl
        selection_frame = ttk.Frame(self.window)
        # Positionierung: Zentral, über zwei Spalten
        # row=2: Zwischen Info- und Content-Frame
        # sticky="ew": Horizontale Ausdehnung
        selection_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Liste für Radio-Buttons (ermöglicht gemeinsame Zustandsverwaltung)
        self.radio_buttons = []
        
        # Radio-Button für Text-Modus
        text_radio = tk.Radiobutton(
            selection_frame,
            text="Text Mode",              # Beschriftung
            variable=self.input_method,    # Gemeinsame Variable
            value="text",                  # Wert bei Auswahl
            command=self.toggle_input_method  # Callback bei Änderung
        )
        # Positionierung links mit Abstand
        text_radio.pack(side=tk.LEFT, padx=5)
        # Zur Liste für gemeinsame Verwaltung hinzufügen
        self.radio_buttons.append(text_radio)

        # Radio-Button für Datei-Modus
        file_radio = tk.Radiobutton(
            selection_frame,
            text="File Mode",              # Beschriftung
            variable=self.input_method,    # Gemeinsame Variable
            value="file",                  # Wert bei Auswahl
            command=self.toggle_input_method  # Callback bei Änderung
        )
        # Positionierung links neben Text-Mode mit Abstand
        file_radio.pack(side=tk.LEFT, padx=5)
        # Zur Liste für gemeinsame Verwaltung hinzufügen
        self.radio_buttons.append(file_radio)



###############
    def open_file(self, mode):
        """
        Öffnet einen Dateiauswahldialog und verarbeitet die ausgewählte Datei.
        
        Die Methode unterstützt zwei Modi:
        1. 'normal':
        - Auswahl des Trägerbildes (PNG)
        - Aktiviert die GUI-Elemente nach erfolgreicher Auswahl
        - Startet automatisch die Bildanalyse
        
        2. 'stegofile':
        - Auswahl der zu versteckenden Datei
        - Prüft die Dateigröße gegen verfügbaren Speicherplatz
        - Aktiviert den Encode-Button bei erfolgreicher Auswahl
        
        Args:
            mode (str): Auswahlmodus ('normal' oder 'stegofile')
        
        Fehlerbehandlung:
        - Prüft Dateigröße bei 'stegofile'
        - Zeigt Fehlermeldung bei zu großen Dateien
        - Bricht bei ungültiger Auswahl ab
        """
        # Bildauswahl-Modus
        if mode == 'normal':
            # Definiere erlaubte Dateitypen
            filetypes = [
                ("PNG Dateien", "*.png"),  # Primär PNG-Dateien
                ("Alle Dateien", "*.*")    # Optional alle Dateien
            ]
            
            # Öffne Dateiauswahl-Dialog für Bilder
            filename = filedialog.askopenfilename(
                title="Bild auswählen",
                filetypes=filetypes
            )
            
            # Wenn eine Datei ausgewählt wurde
            if filename:
                self.current_file = filename  # Speichere Dateipfad
                self.get_file_info()         # Analysiere Bildinformationen
                
        # Modus für zu versteckende Datei
        elif mode == 'stegofile':
            # Öffne Dateiauswahl-Dialog ohne Typeinschränkung
            filename = filedialog.askopenfilename(
                title="Datei zum Verstecken auswählen"
            )
            
            # Wenn eine Datei ausgewählt wurde
            if filename:
                # Prüfe Dateigröße
                file_size = os.path.getsize(filename)
                
                # Vergleiche mit verfügbarem Speicherplatz
                if file_size > self.available_bytes:
                    # Zeige Fehlermeldung bei zu großer Datei
                    messagebox.showerror(
                        "Fehler",
                        f"Datei zu groß! Maximal möglich: {self.available_bytes} Bytes"
                    )
                    return
                        
                # Speichere Dateipfad bei erfolgreicher Prüfung
                self.secret_file = filename
                
                # Aktiviere Encode-Button für den Start des Versteckprozesses
                self.encode_button.config(state=tk.NORMAL)

    def get_file_info(self, img_path=None):
        """
        Analysiert das ausgewählte Bild und zeigt relevante Informationen an.
        
        Die Methode führt folgende Aufgaben aus:
        1. Bildanalyse:
        - Prüft Bildformat und warnt bei Nicht-PNG-Formaten
        - Berechnet Dateigröße in MB
        - Ermittelt Bildabmessungen und Farbkanäle
        - Berechnet verfügbaren Speicherplatz für Steganographie
        
        2. Steganographie-Prüfung:
        - Sucht nach Anzeichen versteckter Daten
        - Berechnet LSB-Statistiken
        - Gibt Hinweise auf mögliche versteckte Inhalte
        
        3. GUI-Aktualisierung:
        - Zeigt alle Informationen im Info-Textfeld
        - Erstellt eine Bildvorschau (maximal 380x380 Pixel)
        - Aktiviert relevante Steuerelemente
        
        Fehlerbehandlung:
        - Prüft ob eine Datei ausgewählt wurde
        - Fängt mögliche Fehler bei der Bildverarbeitung ab
        - Zeigt Fehlermeldungen in einem Dialogfenster an
        """
        # Prüfe ob eine Datei ausgewählt wurde
        if img_path:
            self.current_file =img_path

        if not self.current_file:
            return

        try:
            # Aktiviere info_text für das Schreiben
            if not img_path:
                self.info_text.config(state=tk.NORMAL)
            
            # Öffne und analysiere das Bild
            with Image.open(self.current_file) as img:
                # Warnung bei Nicht-PNG-Formaten
                #if img.format != 'PNG':
                #    messagebox.showwarning(
                #        "Warnung",
                #        "Für beste Ergebnisse bitte PNG-Dateien verwenden!"
                #    )
                
                # Berechne Dateigröße in MB
                file_size = os.path.getsize(self.current_file) / (1024 * 1024)
                
                # Ermittle Bildabmessungen
                width, height = img.size
                
                # Bestimme Anzahl und Art der Farbkanäle
                channels = len(img.getbands())
                strChannels = "RGBA" if channels == 4 else "RGB"
                
                # Berechne verfügbaren Speicherplatz für Steganographie
                # Ein Bit pro Farbkanal pro Pixel
                self.available_bytes = (width * height * channels) // 8

                # Suche nach Anzeichen versteckter Daten
                hidden = ""
                results = self.check_steganography(self.current_file)
                
                # Wenn Auffälligkeiten gefunden wurden
                if (results.get('details')):
                    hidden = (
                        "\n" + results.get('details')[0] + 
                        "\nMittelwert LSBs: " + 
                        str(np.round(results.get('details')[1], 2)) + 
                        "\nEvtl. versteckte Daten enthalten"
                    )

                # Erstelle formatierten Informationstext
                info_text = (
                    f"Dateiname : {os.path.basename(self.current_file)}\n"
                    f"Dateityp  : {img.format}\n"
                    f"Bildgröße : {width}x{height}\n"
                    f"Farbkanäle: {channels}, {strChannels}\n"
                    f"Dateigröße: {file_size:.2f} MB\n"
                    f"Verfügbar : {self.available_bytes//1024} kBytes\n"
                    f"{hidden}"
                )
                # Aktualisiere Info-Textfeld
                if not img_path:
                    self.info_text.delete(1.0, tk.END)    # Lösche alten Inhalt
                    self.info_text.insert(tk.END, info_text)  # Füge neue Infos ein
                
                    # Erstelle Bildvorschau
                    max_size = (380, 380)  # Maximale Vorschaugröße
                    img.thumbnail(max_size, Image.LANCZOS)  # Skaliere Bild
                    self.preview_image = ImageTk.PhotoImage(img)  # Erstelle Tkinter-Bildobjekt
                    self.img_label.config(
                        image=self.preview_image,  # Setze Vorschaubild
                        text=""                    # Entferne Platzhaltertext
                    )
                
                    # Aktiviere GUI-Elemente
                    self.decode_button.config(state=tk.NORMAL)  # Aktiviere Decode-Button
                    for radio in self.radio_buttons:            # Aktiviere Modusauswahl
                        radio.config(state=tk.NORMAL)
                    
                    # Aktualisiere Button-Zustände basierend auf Eingabemodus
                    self.toggle_input_method()
                
                    # Deaktiviere info_text (read-only)
                    self.info_text.config(state=tk.DISABLED)
                    
        except Exception as e:
            # Fehlerbehandlung
            messagebox.showerror(
                "Fehler", 
                f"Fehler beim Analysieren der Datei: {str(e)}"
            )
            if not img_path:
                self.info_text.config(state=tk.DISABLED)

        return info_text
    

    def check_steganography(self, image):
        """
        Analysiert ein PNG-Bild auf mögliche versteckte Daten mittels LSB-Analyse.
        
        Die Methode untersucht die Least Significant Bits (LSBs) des Bildes auf
        statistische Auffälligkeiten, die auf versteckte Daten hinweisen könnten.
        
        Analyseschritte:
        1. Extraktion der LSBs aller Pixel
        2. Berechnung des Mittelwerts der LSB-Verteilung
        3. Vergleich mit erwarteter Normalverteilung
        - Erwartungswert bei zufälligen LSBs: ~0.5
        - Auffällig bei Werten < 0.49 oder > 0.51
        
        Args:
            image: Pfad zum PNG-Bild
        
        Returns:
            dict: Dictionary mit Analyseergebnissen:
                {
                    "lsb_anomalies": bool,  # True wenn Auffälligkeiten gefunden
                    "details": list         # Details zu gefundenen Auffälligkeiten
                }
        
        Fehlerbehandlung:
            Bei Fehlern wird ein Dictionary mit Fehlermeldung zurückgegeben
        """
        try:
            # Bild öffnen und in NumPy-Array konvertieren
            img = Image.open(image)
            img_array = np.array(img)
            
            # Initialisiere Ergebnis-Dictionary
            results = {
                "lsb_anomalies": False,  # Flag für gefundene Auffälligkeiten
                "details": []            # Liste für Detailinformationen
            }
            
            # LSB-Analyse durchführen
            # Extrahiere LSBs mittels Bitwise-AND mit 1
            lsb_data = img_array & 1
            
            # Berechne Mittelwert der LSB-Verteilung
            mean_lsb = np.mean(lsb_data)
            print(mean_lsb)  # Debug-Ausgabe
            
            # Prüfe auf ungewöhnliche LSB-Verteilung
            # Bei normalen Bildern sollte der Mittelwert nahe 0.5 liegen
            lsb_unusual = mean_lsb < 0.49 or mean_lsb > 0.51
            
            # Wenn Auffälligkeiten gefunden wurden
            if lsb_unusual:
                results["lsb_anomalies"] = True
                # Füge Detailinformationen hinzu
                results["details"].append("Ungewöhnliche LSB-Verteilung gefunden")
                results["details"].append(mean_lsb)
                    
            return results
                
        except Exception as e:
            # Bei Fehlern wird ein Dictionary mit Fehlermeldung zurückgegeben
            return {
                "error": f"Fehler bei der Analyse: {str(e)}"
            }

    def encode(self):
        """
        Versteckt Daten in einem Bild mittels LSB-Steganographie.
        
        Der Prozess läuft in mehreren Schritten ab:
        1. Datenvorbereitung:
        - Prüfung des gewählten Modus (Text/Datei)
        - Extraktion der zu versteckenden Daten
        - Größenvalidierung
        
        2. Datenverarbeitung:
        - Hinzufügen eines 4-Byte-Headers mit der Datengröße
        - Konvertierung der Daten in Bits
        - Modifikation der Pixel-LSBs
        
        3. Speicherung:
        - Speichern des modifizierten Bildes als PNG
        - Anzeige des Vergleichs zwischen Original und modifiziertem Bild
        
        Fehlerbehandlung:
        - Prüft Bildauswahl und Datengröße
        - Validiert Pixelwerte
        - Debug-Ausgaben bei Fehlern
        """
        
        # Prüfe ob ein Bild ausgewählt wurde
        if not self.current_file:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst ein Bild aus!")
            return
                
        # Hole die zu versteckenden Daten
        if self.input_method.get() == "text":
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Fehler", "Bitte geben Sie einen Text ein!")
                return
            data = text.encode()
        else:
            if not self.secret_file:
                messagebox.showerror("Fehler", "Bitte wählen Sie eine Datei zum Verstecken aus!")
                return
            with open(self.secret_file, 'rb') as f:
                data = f.read()

        # Prüfe Datengröße
        if len(data) > self.available_bytes:
            messagebox.showerror(
                "Fehler",
                f"Daten zu groß! Maximal möglich: {self.available_bytes} Bytes"
            )
            return
                
        try:
            print(f"Datengröße: {len(data)} Bytes")

            print (self.current_file)
            with Image.open(self.current_file) as img:
                original_pixels = np.array(img, dtype=np.uint8)
                pixels = original_pixels.copy()
            

            # Füge die Größe der Daten am Anfang hinzu
            data_size = len(data)
            full_data = data_size.to_bytes(4, 'big') + data
            

            # Konvertiere Daten in Binärstring
            binary_data = ''.join(format(byte, '08b') for byte in full_data)
            binary_array = np.array([int(bit) for bit in binary_data], dtype=np.uint8)
            
    
            # Überprüfe ob genügend Platz vorhanden ist
            if len(binary_array) > pixels.size:
                messagebox.showerror("Fehler", "Nicht genügend Platz im Bild!")
                return
            

            # Erstelle eine flache Kopie des Arrays und konvertiere zu uint8
            flat_pixels = pixels.ravel().astype(np.uint8)

 
            # Modifiziere nur LSB 
            #flat_pixels[:len(binary_array)] = (flat_pixels[:len(binary_array)] & ~1) | binary_array
            flat_pixels[:len(binary_array)] = (flat_pixels[:len(binary_array)] & 254) | binary_array


            # Reshape zurück zur originalen Form
            modified_pixels = flat_pixels.reshape(pixels.shape)

            # Speichere das neue Bild
            output_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Dateien", "*.png")]
            )
                
            if output_path:
                Image.fromarray(modified_pixels).save(output_path, 'PNG')
                messagebox.showinfo("Erfolg", "Daten wurden erfolgreich versteckt!")

            # Öffne Diff Fenster / Zeige die Bilder an
            self.display_images(original_pixels, modified_pixels)

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Encodieren: {str(e)}")

    def decode(self):
        """
        Extrahiert versteckte Daten aus einem Bild mittels LSB-Steganographie.
        
        Funktionsablauf:
        1. Bildverarbeitung:
        - Lädt das Bild und konvertiert es in ein NumPy-Array
        - Extrahiert die LSBs aller Pixel
        
        2. Datenextraktion:
        - Liest die ersten 32 Bits zur Bestimmung der Datengröße
        - Extrahiert die entsprechende Menge an Datenbits
        - Konvertiert die Bits zurück in Bytes
        
        3. Datenausgabe (abhängig vom gewählten Modus):
        Text-Modus:
        - Versucht die Bytes als Text zu dekodieren
        - Zeigt Text im Textfeld an
        
        Datei-Modus:
        - Speichert die Bytes in eine vom Benutzer gewählte Datei
        
        Fehlerbehandlung:
        - Prüft ob ein Bild geladen ist
        - Validiert die extrahierte Datengröße
        - Behandelt Fehler bei der Textdekodierung
        - Fängt allgemeine Fehler ab
        
        Hinweis:
        Die extrahierten Daten müssen im gleichen Format vorliegen,
        in dem sie versteckt wurden (Text oder Binärdatei).
        """
        # Prüfe ob ein Bild geladen ist
        if not self.current_file:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst ein Bild aus!")
            return
                
        try:
            # Bild öffnen und in NumPy-Array konvertieren
            img = Image.open(self.current_file)
            pixels = np.array(img)

            # Array für effizientere Verarbeitung eindimensional machen
            flat_pixels = pixels.ravel()
            
            # Extrahiere die ersten 32 Bits für die Größeninformation
            # Wandle die LSBs in String-Bits um
            size_bits = (flat_pixels[:32] & 1).astype(str)
            # Konvertiere Bit-String in Integer
            data_size = int(''.join(size_bits), 2)
            
            # Validiere die extrahierte Größe
            available_bytes = (flat_pixels.size - 32) // 8  # Verfügbare Bytes nach Header
            if data_size > available_bytes:
                return None  # Ungültige Größe
                
            # Berechne benötigte Anzahl an Bits
            bits_needed = data_size * 8
            
            # Extrahiere die Datenbits (nach den 32 Größenbits)
            data_bits = (flat_pixels[32:32+bits_needed] & 1).astype(str)
            binary_data = ''.join(data_bits)
            
            # Konvertiere Binärdaten zurück in Bytes
            # Verarbeite jeweils 8 Bits als ein Byte
            data_bytes = bytes(
                int(binary_data[i:i+8], 2)
                for i in range(0, len(binary_data), 8)
            )
                
            # Datenausgabe je nach gewähltem Modus
            if self.input_method.get() == "text":
                try:
                    # Versuche Bytes als Text zu dekodieren
                    decoded_text = data_bytes.decode()
                    # Aktualisiere Textfeld
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(tk.END, decoded_text)
                    messagebox.showinfo("Erfolg", "Text wurde erfolgreich extrahiert!")
                except:
                    messagebox.showerror("Fehler", "Enthaltene Daten sind kein Text!")
            else:
                # Datei-Modus: Speichere Bytes in Datei
                output_path = filedialog.asksaveasfilename(
                    title="Datei speichern unter"
                )
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(data_bytes)
                    messagebox.showinfo("Erfolg", "Datei wurde erfolgreich extrahiert!")
                        
        except Exception as e:
            # Allgemeine Fehlerbehandlung
            messagebox.showerror("Fehler", f"Fehler beim Decodieren: {str(e)}")
            
    def display_images(self, original_pixels, encoded_pixels):
        """
        Erstellt ein Vergleichsfenster zur Visualisierung der Steganographie-Effekte.
        
        Zeigt drei Bilder nebeneinander:
        1. Originalbild:
        - Unmodifiziertes Ausgangsbild
        
        2. Encodiertes Bild:
        - Bild mit versteckten Daten
        - Änderungen für das menschliche Auge meist nicht sichtbar
        
        3. Differenzbild:
        - Visualisiert die Unterschiede zwischen Original und kodiertem Bild
        - Verwendet Heatmap zur Hervorhebung der Änderungen
        - Enthält Colorbar zur Intensitätsanzeige
        
        Args:
            original_pixels (numpy.ndarray): Pixel-Array des Originalbildes
            encoded_pixels (numpy.ndarray): Pixel-Array des encodierten Bildes
        
        Technische Details:
        - Nutzt Matplotlib für die Visualisierung
        - Erstellt ein neues Toplevel-Fenster für die Anzeige
        - Normalisiert die Differenzwerte für bessere Sichtbarkeit
        """
        # Prüfe ob bereits ein Fenster existiert
        if self.display_window is None or not tk.Toplevel.winfo_exists(self.display_window):
            # Erstelle neues Fenster
            self.display_window = tk.Toplevel(self.display_window)
            self.display_window.title("Bildvergleich")
            #self.display_window.attributes("-zoomed", True)  # Maximiere Fenster

            # Schließen-Button hinzufügen
            close_button = tk.Button(
                self.display_window, 
                text="Schließen", 
                command=self.display_window.destroy
            )
            close_button.pack(pady=20)

            # Frame für die Bildanzeige
            self.image_frame = tk.Frame(self.display_window)
            self.image_frame.pack(
                side=tk.RIGHT,
                padx=10, 
                fill=tk.BOTH, 
                expand=True
            )
            
            # Canvas für Matplotlib erstellen
            self.fig = Figure(figsize=(12, 4))  # Breites Format für 3 Bilder
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.image_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Lösche eventuell vorhandene alte Plots
            self.fig.clear()
            
            # Subplot 1: Originalbild
            ax1 = self.fig.add_subplot(131)  # 1 Zeile, 3 Spalten, Position 1
            ax1.imshow(original_pixels)
            ax1.set_title('Original')
            ax1.axis('off')  # Keine Achsen anzeigen
            
            # Subplot 2: Encodiertes Bild
            ax2 = self.fig.add_subplot(132)  # 1 Zeile, 3 Spalten, Position 2
            ax2.imshow(encoded_pixels)
            ax2.set_title('Encodiert')
            ax2.axis('off')
            
            # Subplot 3: Differenzbild
            # Berechne absolute Differenz und konvertiere zu float für Normalisierung
            diff = np.abs(encoded_pixels.astype(np.float32) - 
                        original_pixels.astype(np.float32))
            
            # Normalisiere Differenz für bessere Sichtbarkeit
            if diff.max() > 0:
                # Skaliere auf Bereich 0-255
                diff = diff / diff.max() * 255
                    
            # Bei RGB-Bildern: Konvertiere zu Grauwert für Differenzanzeige
            if len(diff.shape) == 3:
                diff = np.mean(diff, axis=2)
                    
            # Erstelle Differenz-Plot
            ax3 = self.fig.add_subplot(133)  # 1 Zeile, 3 Spalten, Position 3
            # Verwende 'hot' Colormap für intuitive Darstellung der Änderungen
            diff_plot = ax3.imshow(diff, cmap='hot')
            ax3.set_title('Differenz')
            ax3.axis('off')
            
            # Füge Colorbar für Differenzplot hinzu
            # Zeigt die Intensität der Änderungen an
            self.fig.colorbar(diff_plot, ax=ax3)
            
            # Optimiere Layout
            self.fig.tight_layout()
            
            # Aktualisiere Canvas
            self.canvas.draw()



        if not self.current_file:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst ein Bild aus!")
            return

        if self.display_window is None or not tk.Toplevel.winfo_exists(self.display_window):
            self.display_window = tk.Toplevel(self.root)
            self.display_window.title("Analyse")
            #self.window.attributes("-zoomed", True)

            # Schließen Button
            close_button = tk.Button(self.window, text="Schließen", command=self.display_window.destroy)
            close_button.pack(pady=20)

            # Frame für Bildanzeige
            self.image_frame = tk.Frame(self.display_window)
            self.image_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
            # Canvas für Matplotlib
            self.fig = Figure(figsize=(12, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.image_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Clear previous plots
            self.fig.clear()

            # Bild öffnen und in Graustufen konvertieren
            img = Image.open(self.current_file)
            if img.mode != 'L':  # Falls nicht bereits Graustufen
                img = img.convert('L')
            
            img_array = np.array(img)

            # Erzeuge gleichgroße LSB-Normalverteilung
            rnd_array = np.random.randint(0,255, (img_array.shape))


            # LSB extrahieren
            lsb_data = img_array & 1
            
            # Plot erstellen
            ax1 = self.fig.add_subplot(131)
            #ax1.figure(figsize=(15, 12))
            
            # LSB-Normalverteilung
            ax1.imshow(rnd_array, cmap='gray')
            #ax1.imshow(img_array, cmap='gray')
            ax1.set_title('Typische LSB-Normalverteilung')
            ax1.axis('off')
            
            # LSB Visualisierung
            ax2 = self.fig.add_subplot(132)
            #if len(img_array.shape) == 3:
            #    lsb_display = np.stack([lsb_data[:,:,0], lsb_data[:,:,1], lsb_data[:,:,2]], axis=-1)
            #else:
            #    lsb_display = lsb_data
            #ax2.imshow(lsb_display, cmap='binary')
            ax2.imshow(lsb_data, cmap='binary')
            ax2.set_title('LSB-Visualisierung')
            ax2.axis('off')
            
            # LSB-Verteilung als Barplot / #Histogramm
            no_zeros = np.count_nonzero(lsb_data==0)
            no_ones =  np.count_nonzero(lsb_data==1)
            no_total = lsb_data.size
            x = [0,1]
            y = [(no_zeros/no_total),(no_ones/no_total)]
            ax3 = self.fig.add_subplot(133)
            #ax3.hist(lsb_data.flatten(), bins=2)
            ax3.set (xticks = x)
            ax3.bar(x,y, width=0.5)
            ax3.set_title('LSB-Verteilung')
            ax3.set_xlabel('LSB-Wert (0 oder 1)')
            ax3.set_ylabel('Häufigkeit')



            
            #Layout anpassen
            self.fig.tight_layout()
            self.canvas.draw()       

    def analyse_image(self, image=None):
        """
        Führt eine detaillierte LSB-Analyse des Bildes durch und visualisiert die Ergebnisse.
        
        Die Analyse umfasst drei Hauptkomponenten:
        1. LSB-Normalverteilung:
        - Zeigt eine zufällige Verteilung als Referenz
        - Repräsentiert das erwartete Muster bei unmodifizierten Bildern
        
        2. LSB-Visualisierung:
        - Extrahiert und zeigt die Least Significant Bits
        - Ermöglicht visuelle Erkennung von Mustern
        - Auffällige Muster können auf versteckte Daten hinweisen
        
        3. LSB-Verteilungsanalyse:
        - Zeigt die statistische Verteilung der LSB-Werte (0 und 1)
        - Berechnet relative Häufigkeiten
        - Bei unmodifizierten Bildern sollte die Verteilung nahe 50/50 sein
        
        Die Visualisierung erfolgt in einem separaten Fenster mit drei Subplot-Bereichen.
        
        Fehlerbehandlung:
        - Prüft ob ein Bild geladen ist
        - Konvertiert Farb- zu Graustufenbildern für die Analyse
        """
        if image:
            self.current_file = image
            if self.analyse_window and tk.Toplevel.winfo_exists(self.analyse_window):
                self.canvas.get_tk_widget().destroy()
                self.fig.clear()
                self.analyse_window.destroy()
                self.analyse_window = None

        # Prüfe ob ein Bild geladen ist
        if not self.current_file:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst ein Bild aus!")
            return

        # Erstelle neues Fenster falls noch keins existiert
        if self.analyse_window is None or not tk.Toplevel.winfo_exists(self.analyse_window):
            # Initialisiere Analysefenster
            self.analyse_window = tk.Toplevel(self.main_root)
            self.analyse_window.title("Analyse")
            #self.window.attributes("-zoomed", True)

            # Schließen-Button hinzufügen
            close_button = tk.Button(
                self.analyse_window, 
                text="Schließen", 
                command=self.analyse_window.destroy
            )
            close_button.pack(pady=20)

            # Frame für die Visualisierung
            self.image_frame = tk.Frame(self.analyse_window)
            self.image_frame.pack(
                side=tk.RIGHT, 
                padx=10, 
                fill=tk.BOTH, 
                expand=True
            )
            
            # Matplotlib Figure und Canvas erstellen
            self.fig = Figure(figsize=(12, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.image_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Lösche eventuell vorhandene alte Plots
            self.fig.clear()

            # Bild laden und zu Graustufen konvertieren
            img = Image.open(self.current_file)
            if img.mode != 'L':  # Falls nicht bereits Graustufen
                img = img.convert('L')
            
            img_array = np.array(img)

            # Erzeuge Referenz-Normalverteilung
            # Zufallswerte im gleichen Format wie das Originalbild
            rnd_array = np.random.randint(0, 255, (img_array.shape))

            # Extrahiere LSBs des Originalbildes
            lsb_data = img_array & 1
            
            # Plot 1: LSB-Normalverteilung (Referenz)
            ax1 = self.fig.add_subplot(131)
            ax1.imshow(rnd_array, cmap='gray')
            ax1.set_title('Typische LSB-Normalverteilung')
            ax1.axis('off')
            
            # Plot 2: LSB-Visualisierung des Originalbildes
            ax2 = self.fig.add_subplot(132)
            ax2.imshow(lsb_data, cmap='binary')
            ax2.set_title('LSB-Visualisierung')
            ax2.axis('off')
            
            # Plot 3: LSB-Verteilungsanalyse als Balkendiagramm
            # Berechne relative Häufigkeiten
            no_zeros = np.count_nonzero(lsb_data==0)  # Anzahl der 0en
            no_ones = np.count_nonzero(lsb_data==1)   # Anzahl der 1en
            no_total = lsb_data.size                   # Gesamtanzahl Pixel
            
            # Erstelle Daten für Balkendiagramm
            x = [0, 1]  # X-Achse: LSB-Werte
            # Y-Achse: Relative Häufigkeiten
            y = [(no_zeros/no_total), (no_ones/no_total)]
            
            # Plot Balkendiagramm
            ax3 = self.fig.add_subplot(133)
            ax3.set(xticks=x)  # Setze X-Achsen-Beschriftung
            ax3.bar(x, y, width=0.5)  # Erstelle Balken
            ax3.set_title('LSB-Verteilung')
            ax3.set_xlabel('LSB-Wert (0 oder 1)')
            ax3.set_ylabel('Häufigkeit')

            # Optimiere Layout
            self.fig.tight_layout()
            
            # Aktualisiere Canvas
            self.canvas.draw()



if __name__ == "__main__":
    print ("Standalonefunktion deaktiviert. Bitte die Hauptapp starten!")
#    root = tk.Tk()
#    app = SteganographyTool(root)
#   root.mainloop()
