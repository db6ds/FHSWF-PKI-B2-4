def sepia(image):
    """
    Wendet einen Sepia-Filter auf ein Bild an.

    Sepia ist ein Filter, der dem Bild eine warme, braune Tönung verleiht, die an alte Fotografien erinnert.

    Parameter:
    image (PIL.Image.Image): Ein Bildobjekt, auf das der Sepia-Filter angewendet werden soll.

    Rückgabewert:
    PIL.Image.Image: Ein neues Bild mit angewendetem Sepia-Filter.
    """

    # Definiert eine innere Funktion zur Berechnung der Sepia-Farbwerte eines Pixels.
    # Die Funktion nimmt die RGB-Werte eines Pixels (r, g, b) als Eingabe
    # und berechnet die neuen Farbwerte basierend auf der Sepia-Formel.
    def sepia_pixel(r, g, b):
        """
        Berechnet die Sepia-Farbwerte für einen Pixel.

        Parameter:
        r (int): Rotwert des Pixels (0–255).
        g (int): Grünwert des Pixels (0–255).
        b (int): Blauwert des Pixels (0–255).

        Rückgabewert:
        tuple: Die neuen Sepia-RGB-Werte (r, g, b), begrenzt auf 255.
        """
        # Sepia-Berechnung für die drei Farbkanäle:
        # tr, tg und tb sind die transformierten Farbwerte.
        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
        
        # Stellt sicher, dass die Farbwerte nicht größer als 255 sind.
        return min(255, tr), min(255, tg), min(255, tb)

    # Konvertiert das Bild in den "RGB"-Modus, falls es nicht bereits in diesem Modus ist.
    # Der RGB-Modus wird benötigt, um die Farbwerte (r, g, b) für jeden Pixel zu verarbeiten.
    sepia_image = image.convert("RGB")
    
    # Wendet die Sepia-Funktion auf jeden Pixel des Bildes an:
    # - sepia_image.getdata() liefert eine Liste aller Pixel im Bild (als (r, g, b)-Tupel).
    # - Für jedes Pixel wird die Funktion `sepia_pixel` aufgerufen, um die neuen Farbwerte zu berechnen.
    sepia_data = [sepia_pixel(r, g, b) for r, g, b in sepia_image.getdata()]
    
    # Aktualisiert die Pixel des Bildes mit den neuen Sepia-Farbwerten.
    sepia_image.putdata(sepia_data)
    
    # Gibt das Bild mit dem angewendeten Sepia-Filter zurück.
    return sepia_image
