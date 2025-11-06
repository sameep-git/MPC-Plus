from datetime import datetime
from decimal import Decimal
import re

class XBeamModel:
    
    def __init__(self):
        self._type = ""
        self._date = None
        self._path = ""
        self._machine_SN = None
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
    
    def get_machine_SN(self):
        return self._machine_SN

    
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
    
    def set_machine_SN(self, SN):
        self._machine_SN = SN

    def _getDateFromPathName(self, path):
        """
        Extracts a datetime from the given path.
        Example:
            '...NDS-WKS-SN6543-2025-09-19-07-41-49-0008-GeometryCheckTemplate6xMVkVEnhancedCouch'
            → datetime(2025, 9, 19, 7, 41, 49)
        Raises:
            ValueError: if no valid date pattern is found in the path.
        """
        match = re.search(r'(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})', path)
        if not match:
            raise ValueError(f"Could not extract date from path: {path}")
        
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")

    def _getSNFromPathName(self, path):
        """
        Extracts a serial number from the given path.
        Example:
            '...NDS-WKS-SN6543-2025-09-19-07-41-49-0008-GeometryCheckTemplate6xMVkVEnhancedCouch'
            → '6543'
        Raises:
            ValueError: if no valid serial number pattern is found in the path.
        """
        match = re.search(r'SN(\d{4})', path)
        if not match:
            raise ValueError(f"Could not extract serial number from path: {path}")
        return match.group(1)
    

    
    


