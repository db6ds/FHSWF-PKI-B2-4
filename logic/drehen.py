from PIL import Image

'''
Dreht ein gegebenes Bild um 90 Grad im Uhrzeigersinn.

    Args:
        image (PIL.Image.Image): Das Bild, das gedreht werden soll.

    Returns:
        PIL.Image.Image: PIL.Image-Objekt, das das gedrehte Bild enthält.

    Beschreibung:
    - Die Methode `rotate` von PIL wird verwendet, um das Bild zu drehen.
    - Der Winkel von -90 Grad sorgt dafür, dass die Drehung im Uhrzeigersinn erfolgt.
      (Positive Winkel würden das Bild gegen den Uhrzeigersinn drehen.)
    - Das Argument `expand=True` stellt sicher, dass die gesamte gedrehte Bildfläche
      sichtbar bleibt. Ohne dieses Argument würde das Bild auf die ursprünglichen
      Dimensionen zugeschnitten, was Teile des Bildes abschneiden könnte.
'''

def turn_image(image):
    return image.rotate(-90, expand=True)