from abc import ABC
from datetime import datetime
from decimal import Decimal
import re

class AbstractBeamModel(ABC):
    def __init__(self):
        self._type = ""
        self._path = ""
        self._date = None
        self._machine_SN = None

    # --- Getters ---
    def get_type(self):
        return self._type

    def get_date(self):
        return self._date

    def get_path(self):
        return self._path

    def get_machine_SN(self):
        return self._machine_SN

    # --- Setters ---
    def set_type(self, type_value):
        self._type = type_value

    def set_path(self, path):
        self._path = path

    def set_date(self, date):
        self._date = date

    def set_machine_SN(self, SN):
        self._machine_SN = SN

    # --- Concrete utility methods shared by subclasses ---
    def _getDateFromPathName(self, path: str) -> datetime:
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

    def _getSNFromPathName(self, path: str) -> str:
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

