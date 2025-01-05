from tkinter import filedialog
from PIL import Image, ImageTk2

def process_image(image, faces, func, face_mode=False):
    """
    Wendet eine Funktion auf ein Bild oder auf erkannte Gesichtsbereiche an.

    Args:
        image: Ein PIL.Image-Objekt.
        faces: Eine Liste oder ein Array von Bounding-Box-Koordinaten (x, y, w, h).
        func: Eine Funktion, die auf das Bild oder Gesichtsbereiche angewandt wird.
        face_mode: Wenn True, wird die Funktion nur auf Gesichtsbereiche angewandt.

    Returns:
        Ein PIL.Image-Objekt nach der Verarbeitung.
    """
    if face_mode and faces is not None and len(faces) > 0:
        return apply_to_faces(image, faces, func)
    return func(image)


def apply_to_faces(image, faces, func):
    """
    Wendet eine Funktion auf erkannte Gesichtsbereiche eines Bildes an.

    Args:
        image: Ein PIL.Image-Objekt.
        faces: Eine Liste von Bounding-Box-Koordinaten (x, y, w, h) für Gesichter.
        func: Eine Funktion, die auf jedes Gesichtsbereich angewandt wird.

    Returns:
        Ein PIL.Image-Objekt mit verarbeiteten Gesichtsbereichen.
    """
    processed_image = image.copy()
    for (x, y, w, h) in faces:
        # Zuschneiden des Gesichtsbereichs
        face_region = image.crop((x, y, x + w, y + h))

        # Anwenden der Funktion auf den Gesichtsbereich
        processed_region = func(face_region)

        # Zurückkopieren des verarbeiteten Bereichs ins Bild
        processed_image.paste(processed_region, (x, y, x + w, y + h))

    return processed_image