#############################
# SelectionHandler
# Author: Manuela Wittmann 
# Mat-Nr: 30524503
# Gruppe: B2-4
# verwendete Hilfsmittel bei der
# Codeerstellung, Debugging und Kommentierung
# chatgpt und Copilot
##############################

from logic.sharpen import sharpen
from logic.pixelate import pixelate
from logic.schwarz_weiss import schwarz_weiss
from logic.sepia import sepia

class FilterHandler:
    def __init__(self, canvas, update_info, update_canvas, selection_handler):
        '''
        Konstruktor für den FilterHandler, der die Filterlogik und die Canvas-Interaktionen verwaltet.

        :param canvas: Das Canvas-Objekt, auf dem das Bild angezeigt wird.
        :param update_info: Eine Funktion zur Aktualisierung von Informationen oder Benutzermeldungen.
        :param update_canvas: Eine Funktion zur Aktualisierung der Canvas, um das bearbeitete Bild darzustellen.
        :param selection_handler: Der Handler für die Auswahl eines Bildbereichs.
        '''
        self.canvas = canvas
        self.update_info = update_info
        self.update_canvas = update_canvas
        self.selection_handler = selection_handler
        self.selected_area = None
        self.rect_id = None
        self.image = None
        
    def set_image(self, image):
        '''Setzt das Bild, das bearbeitet werden soll.'''
        self.image = image

    def select_filter(self, filter_name):
        '''
        Wendet den ausgewählten Filter auf den markierten Bereich des Bildes an.
        
        :param filter_name: Der Name des Filters, der angewendet werden soll. ("Verpixeln", "Schärfen", "Schwarz-Weiß", "Sepia")
        :return: Das bearbeitete Bild nach der Anwendung des Filters
        '''
        # Hole den aktuell ausgewählten Bereich vom Selection Handler
        self.selected_area = self.selection_handler.get_selected_area()
        print(f"Überprüfe Filterauswahl: Bereich = {self.selected_area}, Bild = {self.image}") 
        
        if self.selected_area and self.image:
            print(f"Ausgewählter Bereich: {self.selected_area}") 
            # Extrahiere die Koordinaten des ausgewählten Bereichs
            x1, y1, x2, y2 = self.selected_area
            # Schneide den Bereich aus dem Bild heraus
            cropped_area = self.image.crop((x1, y1, x2, y2))

            # Filter anwenden
            if filter_name == "Verpixeln":
                filtered_area = pixelate(cropped_area)
            elif filter_name == "Schärfen":
                filtered_area = sharpen(cropped_area)
            elif filter_name == "Schwarz-Weiß":
                filtered_area = schwarz_weiss(cropped_area)
            elif filter_name == "Sepia":
                filtered_area = sepia(cropped_area)
            else:
                self.update_info("Unbekannter Filter.")
                return self.image  # Rückgabe des Originalbildes bei unbekanntem Filter

            # Das gefilterte Bild zurück in das Originalbild einfügen
            self.image.paste(filtered_area, (x1, y1, x2, y2))

            # Aktualisiere die Canvas-Anzeige, um das bearbeitete Bild zu zeigen
            self.update_canvas()

            # Lösche das Rechteck, das den ausgewählten Bereich auf dem Canvas markiert
            if self.rect_id:
                self.canvas.delete(self.rect_id)
                self.rect_id = None

            # Rückmeldung, dass der Filter erfolgreich angewendet wurde
            self.update_info(f"Filter '{filter_name}' angewendet.")            

        else:
            # Falls kein Bereich ausgewählt wurde oder kein Bild vorhanden ist, gib eine Fehlermeldung aus
            self.update_info("Kein Bereich ausgewählt oder kein Bild geladen.")
            
            
            

