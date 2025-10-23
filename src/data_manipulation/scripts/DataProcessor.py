from os import name
from data_manipulation.scripts.Extractor import Extractor
#from Uploader import Uploader
from data_manipulation.models.EBeamModel import EBeamModel
from data_manipulation.models.XBeamModel import XBeamModel
#from Geo6xfff import Geo6xfff

class DataProcessor:

    def __init__(self, path):
        self.path = path + "\\Results.xml"
        self.ex = Extractor()
        #self.up = Uploader()

    def Run(self):
        if("6e" in self.path):
            print("6e Beam detected")
            beam6e = EBeamModel()
            beam6e.set_path(self.path)
            beam6e.set_type("6e")
            beam6e.set_date(beam6e._getDateFromPathName(self.path)); #Sets date based on date in the path name
            self.ex.eModelExtraction(beam6e);
            #beam6e.upload();
        elif("15x" in self.path):
            print("15x Beam detected")
            beam15x = XBeamModel()
            beam15x.set_path(self.path)
            beam15x.set_type("6e")
            beam15x.set_date(beam15x._getDateFromPathName(self.path)); #Sets date based on date in the path name
            self.ex.xModelExtraction(beam15x);
            #beam6e.upload();
        
