from PIL import ImageOps  # Importiert das Modul ImageOps aus der Pillow-Bibliothek.

def schwarz_weiss(image):
    """
    Wendet einen Schwarz-Weiß-Filter auf ein Bild an.

    Parameter:
    image (PIL.Image.Image): Ein Bildobjekt, das in Graustufen umgewandelt werden soll.

    Rückgabewert:
    PIL.Image.Image: Ein neues Bild, das in Graustufen (Schwarz-Weiß) umgewandelt wurde.
    """
    # Verwendet die Funktion 'grayscale' aus dem ImageOps-Modul, um das Bild in Graustufen umzuwandeln.
    return ImageOps.grayscale(image)