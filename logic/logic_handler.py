from logic.gesichtserkennung import detect_faces, mark_faces
from PIL import Image, ImageTk
from logic.drehen import turn_image
from logic.spiegeln import mirror_image
from logic.pixelate import pixelate
from logic.sharpen import sharpen
from logic.schwarz_weiss import schwarz_weiss
from logic.sepia import sepia
from logic.aufhellen import aufhellen
from logic.abdunkeln import abdunkeln
from logic.selection import SelectionHandler
from logic.set_filter import FilterHandler

''' 
Eine Klasse zur Verwaltung der Logik für die Bildbearbeitung in einer GUI-Anwendung.
Diese Klasse steuert verschiedene Bearbeitungsfunktionen wie Gesichtserkennung, Filteranwendung, usw.
'''

class LogicHandler:
    def __init__(self, canvas, update_info):
        '''
        Initialisiert den LogicHandler.
        Args:
            canvas: Das Canvas-Widget der GUI, auf dem Bilder angezeigt werden.
            update_info: Eine Funktion, die Statusinformationen in der GUI aktualisiert.
        '''
        self.canvas = canvas
        self.image = None
        self.faces = None
        self.image_display = None
        self.update_info = update_info
        # Initialisierung der Hilfsklassen:
        self.selection_handler = SelectionHandler(canvas, self.update_info)
        self.filter_handler = FilterHandler(canvas, self.update_info, self.update_canvas, self.selection_handler)
        self.filter_applied = False
    
    def set_image(self, image):
        '''
        Setzt das Bild, das bearbeitet werden soll.

        Args:
            image: Ein PIL.Image-Objekt, das gesetzt und angezeigt werden soll.
        '''
        self.image = image
        self.selection_handler.set_image(image)
        self.filter_handler.set_image(image)
        self.update_canvas()

    def update_canvas(self):
        '''
        Aktualisiert die Anzeige im Canvas mit dem aktuellen Bild.
        Passt die Bildgröße an die Canvas-Dimensionen an.
        '''
        if self.image:
            canvas_width = self.canvas.winfo_width() or 600
            canvas_height = self.canvas.winfo_height() or 400
            self.image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.image_display = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_display)
            self.canvas.image = self.image_display

    def detect_faces(self):
        '''Führt die Gesichtserkennung durch und markiert erkannte Gesichter.'''
        try:
            if self.image:
                self.faces = detect_faces(self.image)
                self.image = mark_faces(self.image.copy(), self.faces)
                self.update_canvas()
        except Exception as e: 
            print(f"Fehler: {e}")       #Fehlermeldung im Terminal bei fehlgeschlagener Gesichtserkennung
            self.update_info("Es wurden keine Gesichter erkannt.")

    def turn_image(self):
        '''Dreht das gesamte Bild um 90 Grad im Uhrzeigersinn'''
        if self.image:
            self.image = turn_image(self.image)
            self.filter_applied = True
            self.update_canvas()

    def mirror_image(self):
        '''Spiegelt das Bild'''
        if self.image:
            self.image = mirror_image(self.image)
            self.filter_applied = True
            self.update_canvas()
            
    def pixelate(self):
        '''Verpixelt das Bild'''
        if self.image: 
            self.image = pixelate(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Das Bild ist nun verpixelt.")
            
    def sharpen(self):
        '''Schärft das Bild'''
        if self.image:
            self.image = sharpen(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Das Bild ist nun geschärft.")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")

    def schwarz_weiss(self):
        '''
        Wendet einen Schwarz-Weiß-Filter auf das Bild an, falls ein Bild geladen ist.
        Aktualisiert anschließend die Benutzeroberfläche und zeigt entsprechende Informationen an.
        '''
        if self.image:
            self.image = schwarz_weiss(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Das Bild ist nun in Schwarz-Weiß.")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")

    def sepia(self):
        '''
        Wendet einen Sepia-Filter auf das aktuell geladene Bild an.
        Aktualisiert anschließend die Benutzeroberfläche und zeigt entsprechende Informationen an.
        '''
        if self.image:
            self.image = sepia(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Das Bild hat nun einen Sepia-Ton.")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")

    def aufhellen(self):
        '''
        Erhöht die Helligkeit des aktuell geladenen Bildes um 50%.
        Aktualisiert anschließend  die Benutzeroberfläche und zeigt entsprechende Informationen an.
        '''
        if self.image:
            self.image= aufhellen(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Die Helligkeit wurde um 50% erhöht.")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")

            
    def abdunkeln(self):
        '''
        Erniedrigt die Helligkeit des aktuell geladenen Bildes um 50%.
        Aktualisiert anschließend  die Benutzeroberfläche und zeigt entsprechende Informationen an.
        '''
        if self.image:
            self.image = abdunkeln(self.image)
            self.filter_applied = True
            self.update_canvas()
            self.update_info("Die Helligkeit wurde um 50% verringert.")
        else:
            self.update_info("Es wurde noch kein Bild geladen.")
     
    def start_selection(self, event):
        '''Startet die Auswahl eines Bereichs'''
        self.selection_handler.start_selection(event)

    def update_selection(self, event):
        '''Aktualisiert die Auswahl eines Bereichs'''
        self.selection_handler.update_selection(event)

    def end_selection(self, event):
        '''Beendet die Auswahl eines Bereichs'''
        self.selection_handler.end_selection(event)
        self.update_info("Es wurde ein Bereich ausgewählt. Wähle nun einen Filter.")

    def set_filter(self, filter_name):
        '''Setzt den Filter, der auf den ausgewählten Bereich angewendet werden soll'''
        if self.image:
            if self.selection_handler.rect_id:
                # Wenn ein Auswahlbereich existiert, wird der Filter auf diesen Bereich angewendet
                if self.filter_applied:
                    self.update_info(f"Ein Filter oder eine Modifikation wurde bereits auf das gesamte Bild angewendet. Du kannst keinen Bereichsfilter mehr anwenden. Falls du einen Bereichsfilter mit einer Bildfilter oder -modifikation kombinieren möchtest, wende zuerst den Bereichsfilter an.")
                    
                    # Wenn ein Auswahlrechteck existiert, wird es gelöscht
                    self.canvas.delete(self.selection_handler.rect_id)
                    self.selection_handler.rect_id = None 
                else:
                    # Filter anwenden, wenn noch kein globaler Filter angewendet wurde
                    self.filter_handler.select_filter(filter_name)
                    self.update_canvas()
                    self.update_info(f"Filter '{filter_name}' wurde auf den ausgewählten Bereich angewendet.")
                    # Wenn ein Auswahlrechteck existiert, wird es gelöscht
                    if self.selection_handler.rect_id:
                        self.canvas.delete(self.selection_handler.rect_id)
                        self.selection_handler.rect_id = None
            else:
                # Wenn kein Auswahlbereich existiert, wird eine Fehlermeldung angezeigt
                self.update_info(f"Der Filter '{filter_name}' konnte nicht angewendet werden, da kein Bereich ausgewählt wurde.")
        else:
            # Wenn kein Bild geladen ist, wird eine Fehlermeldung angezeigt
            self.update_info(f"Der Filter '{filter_name}' konnte nicht angewendet werden, da kein Bild geladen ist.")
            
            # Wenn ein Auswahlrechteck existiert, wird es gelöscht
            if self.selection_handler.rect_id:
                self.canvas.delete(self.selection_handler.rect_id)
                self.selection_handler.rect_id = None
