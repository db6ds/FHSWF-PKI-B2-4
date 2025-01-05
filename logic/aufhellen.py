from PIL import ImageEnhance # Importiert das Modul ImageEnhance aus der Pillow-Bibliothek.

def aufhellen(image):
    """
    Erhöht die Bildhelligkeit um 50%.

    Parameter:
    image (PIL.Image.Image): Ein Bildobjekt, das aufgehellt werden soll.

    Rückgabewert:
    PIL.Image.Image: Ein neues Bild mit um 50% erhöhter Helligkeit.
    """
    # Erzeugt ein Brightness-Enhancer-Objekt.
    # Dieses Objekt ermöglicht die Manipulation der Helligkeit des Bildes.
    enhancer = ImageEnhance.Brightness(image)
    # Erhöht die Helligkeit des Bildes um den Faktor 1,5.
    # Der Wert 1.5 bedeutet, dass die Helligkeit um 50% erhöht wird.
    # - Ein Faktor von 1.0 würde die Helligkeit unverändert lassen.
    return enhancer.enhance(1.5)  
