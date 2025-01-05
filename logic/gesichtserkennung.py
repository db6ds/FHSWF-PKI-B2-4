import cv2
from PIL import ImageDraw
import numpy as np

def detect_faces(image):
    """
    Erkennt Gesichter im Bild und gibt die bearbeiteten Koordinaten zurück.
    Args:
        image (PIL.Image.Image): Das Eingabebild im PIL-Format.

    Returns:
        list: Eine Liste von Rechtecken (x, y, Breite, Höhe) für jedes erkannte Gesicht.

    Raises:
        Exception: Wenn keine Gesichter im Bild erkannt werden.

    Beschreibung:
    Diese Funktion verwendet das Haar-Cascade-Modell von OpenCV, um Gesichter in einem Bild zu erkennen.
    Die Gesichtserkennung wird auf einer Graustufenversion des Bildes durchgeführt, um die Effizienz zu verbessern.
    """

    #Konvertiere PIL-Image in ein OpenCV-kompatibles Format (NumPy-Array mit BGR-Farbkanälen)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    #Lade das vortrainierte Haar-Cascade-Modell für Gesichtserkennung
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    #Konvertiere in Graustufen (für bessere Erkennung)
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    #Führe die Gesichtserkennung durch
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    #Exception, wenn keine Gesichter erkannt werden. Ausgabe im Terminal
    if len(faces) == 0:
        raise Exception("Keine Gesichter erkannt")

    # Rückgabe der erkannten Gesichter als Liste von Koordinaten.
    return faces


def mark_faces(image, faces):
    """
    Markiert erkannte Gesichter im Bild durch das Zeichnen von Rechtecken.

    Args:
        image (PIL.Image.Image): Das Bild, auf dem die Gesichter markiert werden sollen.
        faces (list): Eine Liste von Koordinaten der erkannten Gesichter.
                      Jedes Gesicht wird durch ein Rechteck repräsentiert:
                      (x, y, Breite, Höhe).

    Returns:
        PIL.Image.Image: Das Bild mit Rechtecken um die erkannten Gesichter.

    Beschreibung:
    Diese Funktion verwendet die `ImageDraw`-Klasse von PIL, um auf das Bild zu zeichnen.
    Sie zeichnet für jedes erkannte Gesicht ein Rechteck um die Koordinaten, die in der `faces`-Liste angegeben sind.
    """

    draw = ImageDraw.Draw(image)

    #Zeichne Rechtecke um jedes erkannte Gesicht
    for (x, y, w, h) in faces:
        draw.rectangle([x, y, x+w, y+h], outline="red", width=3)

    return image