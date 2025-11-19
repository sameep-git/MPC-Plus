import os
from .data_extractor import data_extractor
from .image_extractor import image_extractor
from .Uploader import Uploader

from ..models.EBeamModel import EBeamModel
from ..models.XBeamModel import XBeamModel
from ..models.Geo6xfffModel import Geo6xfffModel
from ..models.ImageModel import ImageModel


class DataProcessor:
    """
    Identifies the beam type from the input path,
    creates the appropriate model, and uses extractors
    to process data and images.
    """

    def __init__(self, path: str):
        """
        Initialize the DataProcessor with the directory path containing beam data.
        """
        self.data_path = os.path.join(path, "Results.csv")
        self.image_path = os.path.join(path, "BeamProfileCheck.xim")

        self.data_ex = data_extractor()
        self.image_ex = image_extractor()
        
        # Database Uploader
        self.up = Uploader()
        # If ran as test, coded so that no database connection is made

    # -------------------------------------------------------------------------
    # Generic helper method for beams
    # -------------------------------------------------------------------------
    def _init_beam_model(self, model_class, beam_type):
        """
        Generic initializer for any beam model.
        Sets path, type, date, and machine SN automatically.
        """
        model = model_class()
        model.set_path(self.data_path)
        model.set_type(beam_type)
        model.set_date(model._getDateFromPathName(self.data_path))
        model.set_machine_SN(model._getSNFromPathName(self.data_path))
        model.set_baseline(model._getIsBaselineFromPathName(self.data_path))
        return model
    
    # -------------------------------------------------------------------------
    # Generic helper method for images
    # -------------------------------------------------------------------------
    def _init_beam_image(self, beam_type):
        """
        Initialize an ImageModel for a given beam type and extract the image data.

        Args:
            beam_type (str): The type of the beam (e.g., "6e", "10x", "6x").
        """
        image = ImageModel()
        image.set_path(self.image_path)
        image.set_type(beam_type)
        image.set_date(image._getDateFromPathName(self.image_path))
        image.set_machine_SN(image._getSNFromPathName(self.image_path))
        self.image_ex.get_image(image)
        # return image  # optional if you want to keep a reference to the image object


    # -------------------------------------------------------------------------
    # Internal beam dispatcher
    # -------------------------------------------------------------------------
    def _process_beam(self, is_test=False):
        """
        Shared logic for both Run() and RunTest().
        Detects the beam type, initializes the model, 
        and sends it to the correct extractor method.
        """

        beam_map = {
            "6e": (EBeamModel, "6e"),
            "9e": (EBeamModel, "9e"),
            "12e": (EBeamModel, "12e"),
            "16e": (EBeamModel, "16e"),
            "10x": (XBeamModel, "10x"),
            "15x": (XBeamModel, "15x"),
            "6x": (Geo6xfffModel, "6x"),
        }

        for key, (model_class, beam_type) in beam_map.items():
            if key in self.data_path:
                print(f"{beam_type.upper()} Beam detected")

                # Initialize the correct beam model (EBeam, XBeam, etc.)
                beam = self._init_beam_model(model_class, beam_type)

                if is_test:
                    print("Running test extraction...")
                    self.data_ex.extractTest(beam)
                else:
                    print("Running normal extraction...")
                    self.data_ex.extract(beam)
                    print("Uploading to SupaBase...")
                    # Set Up DataBase
                    # Connect to database
                    connection_params = {
                        'url': 'your-supabase-url',
                        'key': 'your-supabase-key'
                    }
                    self.up.connect(connection_params)
                    # self.up.upload(beam)
                    print("Uploading Complete")
                    self.up.close()

                

                # --- Image Extraction for all beam types ---
                print(f"Extracting image data for {beam_type} beam...")
                self._init_beam_image(beam_type)
                return

        # --- No beam type matched ---
        print(f"Unknown or unsupported beam type for path: {self.data_path}")
        print("Ensure the folder name includes one of the supported identifiers:")
        print("→ 6e, 9e, 12e, 16e, 10x, 15x, or 6x (6xfff)")

    # -------------------------------------------------------------------------
    # Public entrypoints
    # -------------------------------------------------------------------------
    def Run(self):
        """Run the normal data processing workflow."""
        self._process_beam(is_test=False)

    def RunTest(self):
        """Run the test data processing workflow."""
        self._process_beam(is_test=True)
