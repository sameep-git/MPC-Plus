from os import name
from Extractor import Extractor
#from Uploader import Uploader
from ..models import EBeamModel
#from XBeam import XBeam
#from Geo6xfff import Geo6xfff

class DataProcessor:

    def __init__(self, path):
        self.path = path
        self.ex = Extractor()
        self.up = Uploader()

    def Run(self):
        if(self.path.contains("6e")):
            beam6e = EBeam()
            beam6e.setPath(self.path)
            beam6e.setType("6e")
            beam6e.setDate(self._getDateFromPathName(self.path)); #Sets date based on date in the path name
            ex.extract(beam6e);
            #beam6e.upload();
        elif(self.path.contains("15x")):
            beam15x = XBeam()
            beam15x.setPath(self.path)
            beam15x.setType("15x")
            beam15x.setDate(); #Sets date based on date in the path name
        
