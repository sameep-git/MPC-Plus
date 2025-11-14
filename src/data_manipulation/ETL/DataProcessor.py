from os import name
from .data_extractor import data_extractor
from .image_extractor import image_extractor
from .Uploader import Uploader
from ..models.EBeamModel import EBeamModel
from ..models.XBeamModel import XBeamModel
from ..models.Geo6xfffModel import Geo6xfffModel
from ..models.ImageModel import ImageModel 

import os

class DataProcessor:
    """
    This class identifies the beam type from the input path,
    creates the appropriate model, and calls the `data_extractor` to parse
    and extract the relevant beam data from `Results.csv`.
    """
    
    def __init__(self, path, supabase_url=None, supabase_key=None):
        """
        Initialize the DataProcessor with a file path.
        
        Args:
            path (str): The base path to the beam data directory.
                       The processor will look for Results.csv in this directory.
            supabase_url (str, optional): Supabase project URL for uploading data
            supabase_key (str, optional): Supabase API key for uploading data
        """
        # self.data_path = path + "\\Results.csv"
        self.data_path = os.path.join(path, "Results.csv")
        self.data_ex = data_extractor()
        self.image_path = os.path.join(path, "BeamProfileCheck.xim")
        self.image_ex = image_extractor()
        
        # Initialize uploader if credentials provided
        if supabase_url and supabase_key:
            self.uploader = Uploader(supabase_url, supabase_key)
        else:
            self.uploader = None
    
    def Run(self):
        """
        Run the data processing workflow.
    
        Initializes the appropriate beam model, configures it with path, type, 
        and date information, and then passes it to the data_extractor for processing.
        """
    
        # --- ELECTRON BEAMS ---
        if "6e" in self.data_path:
            print("6e Beam detected")
            ## Retrieve beam data from the data_extractor
            beam6e = EBeamModel()
            beam6e.set_path(self.data_path)
            beam6e.set_type("6e")
            beam6e.set_date(beam6e._getDateFromPathName(self.data_path)); # Sets date based on date in the path name
            self.data_ex.testeModelExtraction(beam6e);
            # beam6e.upload();

        elif "9e" in self.data_path:
            print("9e Beam detected")
            beam9e = EBeamModel()
            beam9e.set_path(self.data_path)
            beam9e.set_type("9e")
            beam9e.set_date(beam9e._getDateFromPathName(self.data_path))  # Sets date based on date in the path name
            self.data_ex.eModelExtraction(beam9e)
            # beam9e.upload()

        elif "12e" in self.data_path:
            print("12e Beam detected")
            beam12e = EBeamModel()
            beam12e.set_path(self.data_path)
            beam12e.set_type("12e")
            beam12e.set_date(beam12e._getDateFromPathName(self.data_path)) # Sets date based on date in the path name
            self.data_ex.eModelExtraction(beam12e)
            # beam12e.upload()

        elif "16e" in self.data_path:
            print("16e Beam detected")
            beam16e = EBeamModel()
            beam16e.set_path(self.data_path)
            beam16e.set_type("16e")
            beam16e.set_date(beam16e._getDateFromPathName(self.data_path)) # Sets date based on date in the path name
            self.data_ex.eModelExtraction(beam16e)
            # beam16e.upload()

        # --- X-RAY BEAMS ---
        elif("10x" in self.data_path):
            print("10x Beam detected")
            beam10x = XBeamModel()
            beam10x.set_path(self.data_path)
            beam10x.set_type("10x")
            beam10x.set_date(beam10x._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.xModelExtraction(beam10x);
            # beam6e.upload();
        
        elif("15x" in self.data_path):
            print("15x Beam detected")
            beam15x = XBeamModel()
            beam15x.set_path(self.data_path)
            beam15x.set_type("15x")
            beam15x.set_date(beam15x._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.xModelExtraction(beam15x);
            # beam6e.upload();
        
        # --- GEO BEAMS ---
        elif("6x" in self.data_path):
            print("6xfff Beam detected")
            beam6xfff = Geo6xfffModel()
            beam6xfff.set_path(self.data_path)
            beam6xfff.set_type("15x")
            beam6xfff.set_date(beam6xfff._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.testGeoModelExtraction(beam6xfff);
            # beam6e.upload();
        
        # --- UNKNOWN BEAM TYPE ---
        else:
            print("Unknown or unsupported beam type for path: {self.data_path}")
            print("Ensure the folder name includes one of the supported identifiers:")
            print("→ 6e, 9e, 12e, 16e, 10x, 15x, or 6x (6xfff)")


    def RunTest(self):
        """
        Run the data processing workflow.
    
        Initializes the appropriate beam model, configures it with path, type, 
        and date information, and then passes it to the data_extractor for processing.
        """
    
        # --- ELECTRON BEAMS ---
        if "6e" in self.data_path:
            print("6e Beam detected")
            beam6e = EBeamModel()
            beam6e.set_path(self.data_path)
            beam6e.set_type("6e")
            beam6e.set_date(beam6e._getDateFromPathName(self.data_path)); # Sets date based on date in the path name
            self.data_ex.testeModelExtraction(beam6e);
            ## Retrieve image data from the image_extractor
            print("Retrieving image data from the image_extractor")
            image = ImageModel()
            image.set_path(self.image_path)
            image.set_type("6e")
            image.set_date(image._getDateFromPathName(self.image_path))
            self.image_ex.get_image(image)
            # beam6e.upload();

        elif "9e" in self.data_path:
            print("9e Beam detected")
            beam9e = EBeamModel()
            beam9e.set_path(self.data_path)
            beam9e.set_type("9e")
            beam9e.set_date(beam9e._getDateFromPathName(self.data_path))  # Sets date based on date in the path name
            self.data_ex.testeModelExtraction(beam9e)
            # beam9e.upload()

        elif "12e" in self.data_path:
            print("12e Beam detected")
            beam12e = EBeamModel()
            beam12e.set_path(self.data_path)
            beam12e.set_type("12e")
            beam12e.set_date(beam12e._getDateFromPathName(self.data_path)) # Sets date based on date in the path name
            self.data_ex.testeModelExtraction(beam12e)
            # beam12e.upload()

        elif "16e" in self.data_path:
            print("16e Beam detected")
            beam16e = EBeamModel()
            beam16e.set_path(self.data_path)
            beam16e.set_type("16e")
            beam16e.set_date(beam16e._getDateFromPathName(self.data_path)) # Sets date based on date in the path name
            self.data_ex.eModelExtraction(beam16e)
            # beam16e.upload()

        # --- X-RAY BEAMS ---
        elif("10x" in self.data_path):
            print("10x Beam detected")
            beam10x = XBeamModel()
            beam10x.set_path(self.data_path)
            beam10x.set_type("10x")
            beam10x.set_date(beam10x._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.testxModelExtraction(beam10x);
            # beam6e.upload();
        
        elif("15x" in self.data_path):
            print("15x Beam detected")
            beam15x = XBeamModel()
            beam15x.set_path(self.data_path)
            beam15x.set_type("15x")
            beam15x.set_date(beam15x._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.testxModelExtraction(beam15x);
            # beam6e.upload();
        
        # --- GEO BEAMS ---
        elif("6x" in self.data_path):
            print("6xfff Beam detected")
            beam6xfff = Geo6xfffModel()
            beam6xfff.set_path(self.data_path)
            beam6xfff.set_type("15x")
            beam6xfff.set_date(beam6xfff._getDateFromPathName(self.data_path)); #Sets date based on date in the path name
            self.data_ex.testGeoModelExtraction(beam6xfff);
            # beam6e.upload();
        
        # --- UNKNOWN BEAM TYPE ---
        else:
            print("Unknown or unsupported beam type for path: {self.data_path}")
            print("Ensure the folder name includes one of the supported identifiers:")
            print("→ 6e, 9e, 12e, 16e, 10x, 15x, or 6x (6xfff)")
        
