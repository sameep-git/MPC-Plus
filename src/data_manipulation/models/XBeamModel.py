from src.data_manipulation.models.AbstractBeamModel import AbstractBeamModel
from datetime import datetime
from decimal import Decimal
import re

class XBeamModel(AbstractBeamModel):
    def __init__(self):
        super().__init__()
        self._relative_uniformity = Decimal('0.0')
        self._relative_output = Decimal('0.0')
        self._center_shift = Decimal('0.0')
    
    # Getters
    def get_relative_uniformity(self):
        return self._relative_uniformity
    
    def get_relative_output(self):
        return self._relative_output

    def get_center_shift(self):
        return self._center_shift

    # Setters
    def set_relative_uniformity(self, relative_uniformity):
        self._relative_uniformity = relative_uniformity
    
    def set_relative_output(self, relative_output):
        self._relative_output = relative_output

    def set_center_shift(self, center_shift):
        self._center_shift = center_shift
