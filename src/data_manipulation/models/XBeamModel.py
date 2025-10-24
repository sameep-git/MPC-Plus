from datetime import date
from decimal import Decimal
import math

class XBeamModel:
    
    def __init__(self):
        self._type = ""
        self._date = None
        self._path = ""
        self._relative_uniformity = Decimal('0.0')
        self._relative_output = Decimal('0.0')
        
        # Added for beam center shift
        self._center_shift = Decimal('0.0')
    
    # Getters
    def get_type(self):
        return self._type
    
    def get_date(self):
        return self._date

    def get_path(self):
        return self._path
    
    def get_relative_uniformity(self):
        return self._relative_uniformity
    
    def get_relative_output(self):
        return self._relative_output

    def get_center_shift(self):
        return self._center_shift


    # Placeholder for path parsing (if needed later)
    def _getDateFromPathName(self, path):
        # TODO: Implement date extraction logic from path
        pass
    
    # Setters
    def set_type(self, type_value):
        self._type = type_value

    def set_path(self, path):
        self._path = path
    
    def set_date(self, date_value):
        self._date = date_value
    
    def set_relative_uniformity(self, relative_uniformity):
        self._relative_uniformity = relative_uniformity
    
    def set_relative_output(self, relative_output):
        self._relative_output = relative_output

    def set_center_shift(self, center_shift):
        self._center_shift = center_shift
    

    
    


