from src.data_manipulation.models.AbstractBeamModel import AbstractBeamModel
from datetime import datetime
import re

class ImageModel(AbstractBeamModel):
    def __init__(self):
        super().__init__()

    # Getters
    def get_image(self):
        return self._image

    def get_ImageName(self):
        """
        Image Name Format:
        BeamType_MachineSN_Date
        """
        beam = self.get_type()
        sn = self.get_machine_SN()
        date_obj = self.get_date()
        date_str = date_obj.strftime("%Y%m%d")
        return f"{beam}_{sn}_{date_str}"

      
    # Setters
    def set_image(self, image):
        self._image = image
    