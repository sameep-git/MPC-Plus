"""
Image Extractor Module
----------------
This module defines the `image_extractor` class, responsible create an 
image object from the given image path.

Supported Image Types:
    - BeamProfileCheck.xim
"""

#import pylinac as pl
from pylinac.core.image import XIM

class image_extractor:

    def get_image(self, image):
        #xim_img = XIM("path/to/image.xim")
        tempImage = XIM(image.get_path())
        image.set_image(tempImage)
        # Image properties are stored but not printed to avoid verbose output