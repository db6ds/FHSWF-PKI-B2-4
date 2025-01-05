#############################
# Pixelate Image
# Author: Manuela Wittmann 
# Mat-Nr: 30524503
# Gruppe: B2-4
##############################


from PIL import ImageFilter

def pixelate(image):
    '''Verpixelt das gesamte Bild.'''
    return image.filter(ImageFilter.BoxBlur(5))