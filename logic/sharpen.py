#############################
# Sharpen Image
# Author: Manuela Wittmann 
# Mat-Nr: 30524503
# Gruppe: B2-4
##############################

from PIL import ImageFilter

def sharpen(image):
    '''Schärft das gesamte Bild'''
    return image.filter(ImageFilter.UnsharpMask())