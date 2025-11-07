from src.data_manipulation.models.AbstractBeamModel import AbstractBeamModel
from datetime import datetime
import re

class ImageModel(AbstractBeamModel):
    def __init__(self):
        super().__init__()

    # Getters
    def get_image(self):
        return self._image
      
    # Setters
    def set_image(self, image):
        self._image = image
    