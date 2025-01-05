#############################
# SelectionHandler
# Author: Manuela Wittmann 
# Mat-Nr: 30524503
# Gruppe: B2-4
# verwendete Hilfsmittel bei der
# Codeerstellung, Debugging und Kommentierung
# chatgpt und Copilot
##############################

class SelectionHandler:
    def __init__(self, canvas, update_info):
        '''
        Konstruktor für die Klasse SelectionHandler, die für die Verwaltung der Bereichsauswahl auf dem Canvas verantwortlich ist.
        
        :param canvas: Das Canvas-Objekt, auf dem die Auswahl angezeigt wird.
        :param update_info: Eine Funktion zur Aktualisierung von Informationen oder Benutzermeldungen.
        '''
        self.canvas = canvas  # Das Canvas, auf dem das Bild und die Auswahl angezeigt wird
        self.update_info = update_info  # Funktion zur Ausgabe von Infos
        self.start_x = None  # Start-X-Koordinate der Auswahl
        self.start_y = None  # Start-Y-Koordinate der Auswahl
        self.rect_id = None  # Die ID des Rechtecks, das die Auswahl repräsentiert
        self.selected_area = None  # Die Koordinaten des ausgewählten Bereichs
        self.image = None  # Das Bild, auf dem die Auswahl durchgeführt wird

    def set_image(self, image):
        '''
        Setzt das Bild, auf dem die Auswahl durchgeführt werden soll.
        
        :param image: Das Bild, das bearbeitet wird
        '''
        self.image = image  # Setzt das Bild für die Auswahl
        print(f"Bild gesetzt: {image}")  # Ausgabe des gesetzten Bildes

    def start_selection(self, event):
        '''
        Setzt den Startpunkt für die Auswahl. Ein Rechteck wird auf dem Canvas erstellt.
        
        :param event: Das Event-Objekt, das die Mausposition bei Auswahlbeginn enthält
        '''
        
        # Wenn bereits ein Rechteck existiert, wird dieser gelöscht
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None  # Löschen der Rechteck-ID
            
        # Startpunkte der Auswahl auf Basis der Mauskoordinaten setzen
        self.start_x = event.x
        self.start_y = event.y
        
        # Rechteck auf dem Canvas erstellen, das den Auswahlbereich anzeigt
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,  # Start- und Endkoordinaten des Rechtecks
            outline="red",  # Rechteckrahmenfarbe
            width=2  # Breite des Rahmens
        )
        
        # Ausgabe der Startkoordinaten des Rechtecks
        print(f"Startpunkt gesetzt: ({self.start_x}, {self.start_y}), rect_id: {self.rect_id}")

    def update_selection(self, event):
        '''
        Aktualisiert das Rechteck basierend auf der Mausbewegung, um die Auswahl zu visualisieren.
        
        :param event: Das Event-Objekt, das die aktuelle Mausposition enthält
        '''
        # Wenn das Rechteck existiert, aktualisiere dessen Koordinaten mit der aktuellen Mausposition
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)
            print(f"Rechteck aktualisiert: ({self.start_x}, {self.start_y}) bis ({event.x}, {event.y})")

    def end_selection(self, event=None):
        '''
        Beendet die Auswahl und speichert den ausgewählten Bereich. Das Rechteck wird finalisiert.
        
        :param event: Optional, das Event-Objekt, das den Mausabbruch enthält (normalerweise beim Loslassen der Maus)
        '''
        
        # Überprüfen, ob ein Bild und ein Rechteck existieren, bevor die Auswahl beendet wird
        if self.image and self.rect_id:
            # Holen der aktuellen Koordinaten des Rechtecks
            x1, y1, x2, y2 = self.canvas.coords(self.rect_id)
            print(f"Koordinaten des Rechtecks: ({x1}, {y1}) bis ({x2}, {y2})")
            
            # Umwandeln der Koordinaten zu Ganzzahlen
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Überprüfen, ob das Rechteck eine gültige Größe hat (nicht leer)
            if x1 != x2 and y1 != y2:
                self.selected_area = (x1, y1, x2, y2)  # Bereich für die Auswahl speichern
                print(f"Bereich erfolgreich gesetzt: {self.selected_area}")
            else:
                print("Ungültiger Bereich.")  # Wenn der Bereich ungültig ist (d.h., es wurde keine Fläche ausgewählt)
                self.selected_area = None
        else:
            # Wenn kein Rechteck existiert, Fehlermeldung ausgeben
            print(f"Kein Rechteck gefunden. rect_id: {self.rect_id}")

        return self.selected_area  # Gibt den gewählten Bereich oder None zurück
        
    def get_selected_area(self):
        '''
        Gibt den aktuell ausgewählten Bereich zurück, falls vorhanden.
        
        :return: Der ausgewählte Bereich (x1, y1, x2, y2) oder None, wenn kein Bereich ausgewählt wurde
        '''
        # Überprüfen, ob ein Bereich ausgewählt wurde
        if self.selected_area is None:
            print("Kein Bereich ausgewählt. Bitte wähle zuerst einen Bereich auf dem Bild aus.")  # Ausgabe, wenn kein Bereich ausgewählt wurde
        else: 
            print(f"Ausgewählter Bereich: {self.selected_area}")  # Ausgabe des ausgewählten Bereichs
        return self.selected_area  # Rückgabe des Bereichs oder None
