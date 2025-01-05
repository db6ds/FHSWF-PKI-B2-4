from PIL import ImageEnhance   
"""
    Verringert die Helligkeit eines Bildes um 50%.

    Parameter:
    image (PIL.Image.Image): Ein Bildobjekt, das  abgedunkelt werden soll.

    Rückgabewert:
    PIL.Image.Image: Ein neues Bild, bei dem die Helligkeit um 50% reduziert wurde.
    """
def abdunkeln(image):
    enhancer = ImageEnhance.Brightness(image)

    # Verringert die Helligkeit des Bildes um den Faktor 0.5.
    # Der Faktor 0.5 bedeutet, dass die Helligkeit um 50% reduziert wird.
    return enhancer.enhance(0.5)  

