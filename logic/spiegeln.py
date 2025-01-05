from PIL import Image

'''
Spiegelt ein Bild horizontal (von links nach rechts).

Args:
    image (PIL.Image.Image): Das Bild, das gespiegelt werden soll.

Returns:
    PIL.Image.Image: Das horizontal gespiegelte Bild.

Beschreibung:
Diese Funktion verwendet die Methode `transpose` aus der PIL-Bibliothek, 
um das Bild horizontal zu spiegeln. Die Pixel werden dabei so vertauscht, 
dass die linke Seite des Bildes zur rechten Seite wird und umgekehrt.
'''

def mirror_image(image):
    # Verwende die Transpose-Option FLIP_LEFT_RIGHT, um das Bild horizontal zu spiegeln.
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)