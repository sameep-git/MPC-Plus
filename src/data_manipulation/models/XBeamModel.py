from datetime import date
from decimal import Decimal
import math

class XBeamModel:
    
    def __init__(self):
        self._type = ""
        self._date = None
        self._relative_uniformity = Decimal('0.0')
        self._relative_out = Decimal('0.0')
        
        # Added for beam center shift
        self._baseline_iso_x = Decimal('0.0')
        self._baseline_iso_y = Decimal('0.0')
        self._iso_x = Decimal('0.0')
        self._iso_y = Decimal('0.0')
    
    # Getters
    def get_type(self):
        return self._type
    
    def get_date(self):
        return self._date
    
    def get_relative_uniformity(self):
        return self._relative_uniformity
    
    def get_relative_out(self):
        return self._relative_out
    
    def get_baseline_iso_x(self):
        return self._baseline_iso_x
    
    def get_baseline_iso_y(self):
        return self._baseline_iso_y
    
    def get_iso_x(self):
        return self._iso_x
    
    def get_iso_y(self):
        return self._iso_y

    # Placeholder for path parsing (if needed later)
    def _getDateFromPathName(self, path):
        # TODO: Implement date extraction logic from path
        pass
    
    # Setters
    def set_type(self, type_value):
        self._type = type_value
    
    def set_date(self, date_value):
        self._date = date_value
    
    def set_relative_uniformity(self, relative_uniformity):
        self._relative_uniformity = Decimal(str(relative_uniformity))
    
    def set_relative_out(self, relative_out):
        self._relative_out = Decimal(str(relative_out))
    
    def set_baseline_iso(self, x, y):
        """Set baseline isocenter coordinates."""
        self._baseline_iso_x = Decimal(str(x))
        self._baseline_iso_y = Decimal(str(y))
    
    def set_iso_center(self, x, y):
        """Set current isocenter coordinates."""
        self._iso_x = Decimal(str(x))
        self._iso_y = Decimal(str(y))
    
    
    # Calculation
    def beam_output_change(self):
        """
        Calculates beam output change percentage.
        Formula: (relative_output - 1) * 100
        """
        return (self._relative_out - Decimal('1.0')) * Decimal('100.0')
    
    def beam_uniformity_change(self):
        """
        Calculates beam uniformity change percentage.
        Formula: relative_uniformity * 100
        """
        return self._relative_uniformity * Decimal('100.0')
    
    def beam_center_shift(self):
        """
        Calculates beam center shift (mm).
        Formula: sqrt((X - Xb)^2 + (Y - Yb)^2)
        """
        dx = self._iso_x - self._baseline_iso_x
        dy = self._iso_y - self._baseline_iso_y
        shift = Decimal(math.sqrt(dx ** 2 + dy ** 2))
        return shift

