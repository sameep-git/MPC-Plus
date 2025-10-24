from datetime import date
from decimal import Decimal

class EBeamModel:
    
    def __init__(self):
        self._type = ""
        self._path = ""
        self._date = None
        self._relative_uniformity = Decimal('0.0')
        self._relative_output = Decimal('0.0')
    
    # Getters
    def get_type(self):
        return self._type
    
    def get_date(self):
        return self._date
    
    def get_relative_uniformity(self):
        return self._relative_uniformity
    
    def get_relative_output(self):
        return self._relative_output

    def get_path(self):
        return self._path
      
    def _getDateFromPathName(self, path):
        # TODO: Implement date extraction logic from path
        # This method should parse the path and extract the date
        pass
    
    # Setters
    def set_type(self, type_value):
        self._type = type_value
    
    def set_path(self, path):
        self._path = path

    def set_date(self, date):
        self._date = date
    
    def set_relative_uniformity(self, relative_uniformity):
        self._relative_uniformity = relative_uniformity
    
    def set_relative_output(self, relative_output):
        self._relative_output = relative_output

