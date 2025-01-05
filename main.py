
# -*- coding: utf-8 -*-
"""
Hauptanwendung für ein Bildbearbeitungsprogramm mit verschiedenen Funktionen:
- Grundlegende Bildmanipulation (drehen, spiegeln)
- Gesichtserkennung
- Steganographie (Verstecken von Daten in Bildern)
- Farbfilter und Effekte
- Bereichsbasierte Bildbearbeitung

@author: B2-4

Anpassung, dass Bildvorschau angezeigt werden kann Dez 12 20:54:00 2024
@ manuela

13.12.24 - Steganotool eingefügt @ Daniel
20.12.24 - Neues GUI Design @ Daniel
21.12.24 - generel-Klasse wieder entfernt. Globaler Filepicker und Vorschau in main
28.12.24 - Buttons neu angeordnet
            Farbschema: #F2F2F2, #BCDDE6, #4CE6D1, #BEEBC6, #C3D7EB, #CAE8E4
28.12.24 - Gesichtserkennung, drehen und spiegeln implementiert

Wichtige To-Do's (aus Joys Sicht):  1) Zurücksetzen (Meta-Daten sollen beim Zurücksetzen nicht verschwinden) und Speichern für alle Funktionen
                                    2) Funktionen sollen auf das bearbeitete Bild additiv greifen
                                    3) gitignore muss von allen genutzt werden
                                    4) Überflüssige Variablen oder Funktionen entfernen
                                    
29.12.2024 -    zurucksetzen und speichern in main implementiert
                pixelate, set_filter und selection in logic_handler implementiert
                es können mehrere Filter in der Bereichsauswahl angewendet werden. 
                main korrgiert, sodass kein Zugriff mehr auf Verpixeln_Bildbearbeitung für das Anzeigen und Resetten der Bilder notwendig ist. 
30.12.2024 -   Farbfilter hinzugefügt
31.12.2024 -   main Kommentiert @ Daniel

03.01.2025 -    Helligkeitsregler wird immer angezeigt
                Schwarz-Weiß und Sepia können ebenfalls auf einen ausgewählten Bereich angewendet werden. 
                Farbschema für Spalte 6 eingefügt
                Nicht benutzter Import (tkk) entfernt
                Redundanzen entfernt und Dokumentation vereinheitlicht. 
                @ Manuela
                
05.01.2025 -    Hier könnte Ihre Werbung stehen zu "Fachhoschule Südwestfalen\nProgrammierung für KI\nProjektgruppe B2-4" geändert. @ Manuela
06.01.2025 -    save_as korrigiert, und Finetuning @ Daniel
"""

# === main.py ===
import tkinter as tk
from tkinter import filedialog
from logic.steganotool import SteganographyTool 
from logic.logic_handler import LogicHandler
from PIL import Image, ImageTk


class MainApplication:
    def __init__(self, root):
        ''''
        Initialisiert die Hauptanwendung und erstellt das GUI.
        
        Args:
            root: Das Hauptfenster der Tkinter-Anwendung
        '''
        # Grundlegende Fenster-Konfiguration
        self.root = root
        self.root.title("Bildverarbeitung und Bildanalyse")
        self.root.geometry("1820x1320")
        
        # Speichert den Pfad zum aktuell geladenen Bild
        self.img_path = None
                
        # Erstelle eine Bildansicht im Fenster
        self.panel = tk.Label(self.root, text="Fachhochschule Südwestfalen - Programmierung für KI - Projektgruppe B2-4",image = None) 
        self.panel.configure(fg='#333333', font= ("Helvetica", 15))#, "bold"))
        self.panel.pack()
        
        # Erstelle Bildansichten und InfoFeld im Frame
        pic_frame = tk.Frame(self.root)
        pic_frame.pack(side="top", pady=20)

        # Bearbeitungsbereich
        self.lbl_canvas = tk.Label(pic_frame, text="Bearbeitung", image=None)
        self.lbl_canvas.config(font=("Helvetica", 11, "bold"))
        self.lbl_canvas.grid(row=0, column=1)
        
        # Canvas für die Bildbearbeitung
        self.canvas = tk.Canvas(pic_frame, width=800, height=500, bg="white")
        self.canvas.grid(sticky="ew", row=1, column=1)

        # Informationsbereich
        self.info = tk.Text(pic_frame, height=10, width=25)
        self.info.grid(sticky="ew", row=2, column=0)

        # Vorschaubereich für das Originalbild
        self.lbl_vorschau = tk.Label(pic_frame, text="Original", image=None)
        self.lbl_vorschau.config(font=("Helvetica", 11, "bold"))
        self.lbl_vorschau.grid(row=0, column=0)
        
        # Canvas für die Originalbildanzeige
        self.can_vorschau = tk.Canvas(pic_frame, width=800, height=500, bg="white")
        self.can_vorschau.grid(sticky="ew", row=1, column=0)

        # Initialer Info-Text
        self.info.delete(1.0, tk.END)
        self.update_info("Bitte ein Bild laden")

        # Erstelle Instanzen der Funktionsklassen
        self.stegano_tool = SteganographyTool(self.root)  # Geändert DS
        self.logic = LogicHandler(self.canvas, update_info = self.update_info)
        
        # Button Frame erstellen  
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=20)

        # Datei Funktionen
        self.lbl_Datei = tk.Label(button_frame, text="Datei",image = None) 
        self.lbl_Datei.config(font=("Helvetica", 11, "bold"))
        self.lbl_Datei.grid(row=0, column=0)

        self.btn_select = tk.Button(button_frame, text="Auswählen", command= self.set_file)
        self.btn_select.grid(row=1, column=0, padx=10, pady=5)        

        self.btn_save = tk.Button(button_frame, text="Speichern", command=self.save_as)
        self.btn_save.grid(row=2, column=0, padx=10, pady=5)  
        
        self.btn_restore = tk.Button(button_frame, text="Zurücksetzen", command=self.reset)
        self.btn_restore.grid(row=3, column=0, padx=10, pady=5)
                   
        self.lbl_Analyse = tk.Label(button_frame, text="Bildmodifikation",image = None) 
        self.lbl_Analyse.config(font=("Helvetica", 11, "bold"))
        self.lbl_Analyse.grid(row=0, column=1)

        self.btn_face = tk.Button(button_frame, text="Gesichter\nerkennen", command=self.logic.detect_faces)
        self.btn_face.grid(row=1, column=1, padx=10, pady=5)
        self.btn_turn = tk.Button(button_frame, text="drehen", command=self.logic.turn_image)
        self.btn_turn.grid(row=2, column=1, padx=10, pady=5)      
        self.btn_mirror = tk.Button(button_frame, text="spiegeln", command=self.logic.mirror_image)
        self.btn_mirror.grid(row=3, column=1, padx=10, pady=5)

        # Steganographie
        self.lbl_Stego = tk.Label(button_frame, text="Steganographie",image = None) 
        self.lbl_Stego.config(font=("Helvetica", 11, "bold"))
        self.lbl_Stego.grid(row=0, column=2)

        self.btn_analyse = tk.Button(button_frame, text="LSB\nAnalyse", command=lambda: self.stegano_tool.analyse_image(self.img_path))  
        self.btn_analyse.grid(row=1, column=2, padx=10, pady=5)
        self.btn_encode = tk.Button(button_frame, text="Daten\nverstecken", command=lambda: self.stegano_tool.ausfuehren(self.img_path))  
        self.btn_encode.grid(row=2, column=2, padx=10, pady=5)
        self.btn_decode = tk.Button(button_frame, text="Daten\ndecodieren", command=lambda: self.stegano_tool.ausfuehren(self.img_path))  
        self.btn_decode.grid(row=3, column=2, padx=10, pady=5)
        
        # Farbfilter
        self.lbl_Modify = tk.Label(button_frame, text="Komplettes Bild",image = None) 
        self.lbl_Modify.config(font=("Helvetica", 11, "bold"))
        self.lbl_Modify.grid(row=0, column=3, columnspan=2)
        
        self.btn_bw = tk.Button(button_frame, text="Schwarz-Weiß", command=self.logic.schwarz_weiss)
        self.btn_bw.grid(row=1, column=3, padx=10, pady=5)
        
        self.btn_sepia = tk.Button(button_frame, text="Sepia", command=self.logic.sepia)
        self.btn_sepia.grid(row=2, column=3, padx=10, pady=5)

        self.btn_brightness = tk.Button(button_frame, text="Aufhellen", command=self.logic.aufhellen)
        self.btn_brightness.grid(row=3, column=3, padx=10, pady=5)

        self.btn_verpixeln_gesamt = tk.Button(button_frame, text="Verpixeln", command=self.logic.pixelate)
        self.btn_verpixeln_gesamt.grid(row=1, column=4, padx=10, pady=5) 

        self.btn_tbd2 = tk.Button(button_frame, text="Schärfen", command=self.logic.sharpen)
        self.btn_tbd2.grid(row=2, column=4, padx=10, pady=5)

        self.btn_darken = tk.Button(button_frame, text="Abdunkeln", command=self.logic.abdunkeln)
        self.btn_darken.grid(row=3, column=4, padx=10, pady=5)

        # Filter kann erst nach Bereichsauswahl angewendet werden
        self.lbl_Modify = tk.Label(button_frame, text="Auswahl",image = None) 
        self.lbl_Modify.config(font=("Helvetica", 11, "bold"))
        self.lbl_Modify.grid(row=0, column=5, columnspan=2)
        self.btn_verpixeln = tk.Button(button_frame, text="Verpixeln", command=lambda: self.logic.set_filter("Verpixeln"))
        self.btn_verpixeln.grid(row=1, column=5, padx=10, pady=5) 
        self.btn_sharpen = tk.Button(button_frame, text="Schärfen", command=lambda: self.logic.set_filter("Schärfen"))
        self.btn_sharpen.grid(row=2, column=5, padx=10, pady=5)    
        self.btn_black_white = tk.Button(button_frame, text="Schwarz-Weiß", command=lambda: self.logic.set_filter("Schwarz-Weiß"))
        self.btn_black_white.grid(row=1, column=6, padx=10, pady=5)    
        self.btn_sepia = tk.Button(button_frame, text="Sepia", command=lambda: self.logic.set_filter("Sepia"))
        self.btn_sepia.grid(row=2, column=6, padx=10, pady=5)        

        # Formatierung der Buttons
        self.format_Buttons(button_frame)

        # Ereignisse für Freihandverpixeln
        self.canvas.bind("<ButtonPress-1>", self.logic.start_selection)
        self.canvas.bind("<B1-Motion>", self.logic.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.logic.end_selection)

    def format_Buttons(self, button_frame):
        '''
        Formatiert alle Buttons im Button-Frame einheitlich
        
        Args:
            button_frame: Der Frame, der die zu formatierenden Buttons enthält
        '''
        for button in button_frame.winfo_children():
            if isinstance(button, tk.Button):
                button.configure( height = 2, width = 13)
                grid_info = button.grid_info()
                #row = grid_info['row']
                column = grid_info['column']
                ## Farben festlegen
                match column:
                    case 0:
                        button.configure(bg='#F2F2F2')
                    case 1:
                        button.configure(bg='#BCDEE6')
                    case 2:
                        button.configure(bg='#C3D7EB')
                    case 3 | 4:
                        button.configure(bg='#BEEBC6')
                    case 5 | 6:
                        button.configure(bg='#CAE8E4')
                    
    def vorschau(self, selected_path):
        '''
        Erstellt eine skalierte Vorschau des ausgewählten Bildes
        
        Args:
            selected_path: Pfad zum ausgewählten Bild
        '''
        # Bild laden und für Canvas-Größe skalieren
        canvas_width = int(self.can_vorschau.__getitem__('width'))
        canvas_height = int(self.can_vorschau.__getitem__('height'))
        img = Image.open(selected_path)
        img.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        image_display = ImageTk.PhotoImage(img)

        # Bild im Vorschau Canvas anzeigen
        self.can_vorschau.create_image(0, 0, anchor=tk.NW, image=image_display)
        self.can_vorschau.image = image_display  # Referenz zum Canvas hinzufügen
    
        # Bild im Bearbeitungs-Canvas anzeigen
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_display)
        self.canvas.image = image_display  # Referenz zum Canvas hinzufügen

    def set_file(self, filetypes=None):
        '''Setzt den globalen Pfad zur Datei und zeigt die Bildinformationen an. Es werden die erlaubten Bildtypen definiert'''
        
        match filetypes:
            case None:
                filetypes=[("Bild Dateien", "*.png *.jpg *.jpeg *.bmp")]
            case 'PNG':
                filetypes = [("PNG Dateien", "*.png")]  # Primär PNG-Dateien
            case 'all':
                filetypes = [("Alle Dateien",  "*.*")]   # Optional alle Dateien

        self.img_path = filedialog.askopenfilename(title="Bild auswählen", filetypes=filetypes)

        if self.img_path:
            # Bild-Informationen anzeigen
            self.info_text = self.stegano_tool.get_file_info(self.img_path)
            self.info.delete(1.0, tk.END)
            self.update_info(self.info_text)
            self.vorschau(self.img_path)
            img = Image.open(self.img_path)
            self.logic.set_image(img)
 
    def update_info(self, message):
        '''
        Aktualisiert das Info-Textfeld mit einer neuen Nachricht
        
        Args:
            message: Die anzuzeigende Nachricht
        '''
        self.info.config(state="normal")
        self.info.delete(1.0, tk.END)
        self.info.insert(tk.END, message)
        self.info.config(state="disabled")
        print(f'Ausgewählte Datei: {self.img_path}')

    def reset(self):
        '''Setzt das Bild auf das Original zurück.'''
        if self.can_vorschau.image:
            self.canvas.image = self.can_vorschau.image  # Auf das Originalbild zurücksetzen
            self.logic.set_image(Image.open(self.img_path))
            self.update_info(f"Das Bild wurde auf das Original zurückgesetzt.\n{self.info_text}")
            self.logic.filter_applied = False
        else:
            self.update_info("Es wurde noch keine Datei geöffnet.")
   
            

    def save_as(self):
        '''Speichert das aktuelle Bild.'''
        if hasattr(self.logic, 'image') and self.logic.image: 
            try: 
                # Dialog zur Auswahl des Speicherpfades
                speicherpfad = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[
                        ("PNG files", "*.png"),
                        ("JPEG files", "*.jpg;*.jpeg"),
                        ("BMP files", "*.bmp"),
                        ("All files", "*.*")
                    ]
                )
                if speicherpfad:
                    # Verwende das PIL Image aus dem LogicHandler zum Speichern
                    self.logic.image.save(speicherpfad)
                    self.update_info("Das Bild wurde gespeichert.")
            except Exception as e:
                self.update_info(f"Fehler beim Speichern der Datei: {str(e)}")
                print(f"Fehler beim Speichern der Datei: {e}")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")            
    

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

