from os import name
from .Extractor import Extractor
# From Uploader import Uploader
from ..models.EBeamModel import EBeamModel
from ..models.XBeamModel import XBeamModel
from ..models.Geo6xfffModel import Geo6xfffModel
# From Geo6xfff import Geo6xfff

class DataProcessor:
    """
    This class identifies the beam type from the input path,
    creates the appropriate model, and calls the `Extractor` to parse
    and extract the relevant beam data from `Results.csv`.
    """
    
    def __init__(self, path):
        """
        Initialize the DataProcessor with a file path.
        path (str): The base path to the beam data directory.
        The processor will look for Results.csv in this directory.
        """
        self.path = path + "\\Results.csv"
        self.ex = Extractor()
        #self.up = Uploader()
    
    def Run(self):
        """
        Run the data processing workflow.
    
        Initializes the appropriate beam model, configures it with path, type, 
        and date information, and then passes it to the extractor for processing.
        """
    
        # --- ELECTRON BEAMS ---
        if "6e" in self.path:
            print("6e Beam detected")
            beam6e = EBeamModel()
            beam6e.set_path(self.path)
            beam6e.set_type("6e")
            beam6e.set_date(beam6e._getDateFromPathName(self.path)); # Sets date based on date in the path name
            self.ex.testeModelExtraction(beam6e);
            # beam6e.upload();

        elif "9e" in self.path:
            print("9e Beam detected")
            beam9e = EBeamModel()
            beam9e.set_path(self.path)
            beam9e.set_type("9e")
            beam9e.set_date(beam9e._getDateFromPathName(self.path))  # Sets date based on date in the path name
            self.ex.eModelExtraction(beam9e)
            # beam9e.upload()

        elif "12e" in self.path:
            print("12e Beam detected")
            beam12e = EBeamModel()
            beam12e.set_path(self.path)
            beam12e.set_type("12e")
            beam12e.set_date(beam12e._getDateFromPathName(self.path)) # Sets date based on date in the path name
            self.ex.eModelExtraction(beam12e)
            # beam12e.upload()

        elif "16e" in self.path:
            print("16e Beam detected")
            beam16e = EBeamModel()
            beam16e.set_path(self.path)
            beam16e.set_type("16e")
            beam16e.set_date(beam16e._getDateFromPathName(self.path)) # Sets date based on date in the path name
            self.ex.eModelExtraction(beam16e)
            # beam16e.upload()

        # --- X-RAY BEAMS ---
        elif("10x" in self.path):
            print("10x Beam detected")
            beam10x = XBeamModel()
            beam10x.set_path(self.path)
            beam10x.set_type("10x")
            beam10x.set_date(beam10x._getDateFromPathName(self.path)); #Sets date based on date in the path name
            self.ex.xModelExtraction(beam10x);
            # beam6e.upload();
        
        elif("15x" in self.path):
            print("15x Beam detected")
            beam15x = XBeamModel()
            beam15x.set_path(self.path)
            beam15x.set_type("15x")
            beam15x.set_date(beam15x._getDateFromPathName(self.path)); #Sets date based on date in the path name
            self.ex.xModelExtraction(beam15x);
            # beam6e.upload();
        
        # --- GEO BEAMS ---
        elif("6x" in self.path):
            print("6xfff Beam detected")
            beam6xfff = Geo6xfffModel()
            beam6xfff.set_path(self.path)
            beam6xfff.set_type("15x")
            beam6xfff.set_date(beam6xfff._getDateFromPathName(self.path)); #Sets date based on date in the path name
            self.ex.testGeoModelExtraction(beam6xfff);
            # beam6e.upload();
        
        # --- UNKNOWN BEAM TYPE ---
        else:
            print("Unknown or unsupported beam type for path: {self.path}")
            print("Ensure the folder name includes one of the supported identifiers:")
            print("→ 6e, 9e, 12e, 16e, 10x, 15x, or 6x (6xfff)")
        
