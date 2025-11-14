"""
Supabase Uploader Module
------------------------
This module handles uploading beam quality assurance data to Supabase database.

The Uploader class connects to Supabase and provides methods to upload:
    - Electron beam data (EBeamModel) to beam-specific tables
    - X-ray beam data (XBeamModel) to beam-specific tables
    - Geometry check data (Geo6xfffModel) to the 6x geometry table

Each of the 7 beam types (6e, 9e, 12e, 16e, 10x, 15x, 6x) has its own table
in the Supabase database to maintain data integrity and optimize queries.
"""

from supabase import create_client, Client
from datetime import datetime
from decimal import Decimal
import json


class Uploader:
    """
    Handles uploading beam QA data to Supabase database.
    
    Connects to Supabase using provided credentials and uploads data from
    model instances (EBeamModel, XBeamModel, Geo6xfffModel) to their respective
    tables based on beam type.
    """
    
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initialize the Uploader with Supabase connection credentials.
        
        
        Raises:
            Exception: If connection to Supabase fails
        """
        try:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            print(f"✓ Successfully connected to Supabase")
        except Exception as e:
            print(f"✗ Failed to connect to Supabase: {e}")
            raise
    
    def _convert_decimal_to_float(self, value):
        """
        Convert Decimal values to float for JSON serialization.
        
        Args:
            value: The value to convert (Decimal, datetime, or other)
            
        Returns:
            Converted value suitable for JSON serialization
        """
        if isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        return value
    
    def EBeamUploader(self, ebeam_model):
        """
        Upload electron beam data to the appropriate Supabase table.
        
        Takes an EBeamModel instance and uploads all data to the table
        corresponding to the beam type (6e, 9e, 12e, or 16e).
        
        Args:
            ebeam_model: Instance of EBeamModel with populated data
            
        Returns:
            dict: Response from Supabase API containing inserted record
            
        Raises:
            ValueError: If beam type is not recognized
            Exception: If upload to Supabase fails
        """
        try:
            # Get beam type to determine table name
            beam_type = ebeam_model.get_type()
            
            # Validate beam type
            valid_ebeam_types = ['6e', '9e', '12e', '16e']
            if beam_type not in valid_ebeam_types:
                raise ValueError(f"Invalid E-beam type: {beam_type}. Must be one of {valid_ebeam_types}")
            
            # Determine table name based on beam type
            table_name = f"beam_{beam_type}"  # e.g., "beam_6e", "beam_9e"
            
            # Extract all data using getters
            data = {
                'beam_type': beam_type,
                'measurement_date': self._convert_decimal_to_float(ebeam_model.get_date()),
                'file_path': ebeam_model.get_path(),
                'relative_uniformity': self._convert_decimal_to_float(ebeam_model.get_relative_uniformity()),
                'relative_output': self._convert_decimal_to_float(ebeam_model.get_relative_output()),
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Upload to Supabase
            print(f"Uploading E-beam ({beam_type}) data to table '{table_name}'...")
            response = self.supabase.table(table_name).insert(data).execute()
            
            print(f"✓ Successfully uploaded E-beam ({beam_type}) data")
            return response
            
        except ValueError as ve:
            print(f"✗ Validation Error: {ve}")
            raise
        except Exception as e:
            print(f"✗ Error uploading E-beam data: {e}")
            raise
    
    def XBeamUploader(self, xbeam_model):
        """
        Upload X-ray beam data to the appropriate Supabase table.
        
        Takes an XBeamModel instance and uploads all data to the table
        corresponding to the beam type (10x or 15x).
        
        Args:
            xbeam_model: Instance of XBeamModel with populated data
            
        Returns:
            dict: Response from Supabase API containing inserted record
            
        Raises:
            ValueError: If beam type is not recognized
            Exception: If upload to Supabase fails
        """
        try:
            # Get beam type to determine table name
            beam_type = xbeam_model.get_type()
            
            # Validate beam type
            valid_xbeam_types = ['10x', '15x']
            if beam_type not in valid_xbeam_types:
                raise ValueError(f"Invalid X-beam type: {beam_type}. Must be one of {valid_xbeam_types}")
            
            # Determine table name based on beam type
            table_name = f"beam_{beam_type}"  # e.g., "beam_10x", "beam_15x"
            
            # Extract all data using getters
            data = {
                'beam_type': beam_type,
                'measurement_date': self._convert_decimal_to_float(xbeam_model.get_date()),
                'file_path': xbeam_model.get_path(),
                'relative_uniformity': self._convert_decimal_to_float(xbeam_model.get_relative_uniformity()),
                'relative_output': self._convert_decimal_to_float(xbeam_model.get_relative_output()),
                'center_shift': self._convert_decimal_to_float(xbeam_model.get_center_shift()),
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Upload to Supabase
            print(f"Uploading X-beam ({beam_type}) data to table '{table_name}'...")
            response = self.supabase.table(table_name).insert(data).execute()
            
            print(f"✓ Successfully uploaded X-beam ({beam_type}) data")
            return response
            
        except ValueError as ve:
            print(f"✗ Validation Error: {ve}")
            raise
        except Exception as e:
            print(f"✗ Error uploading X-beam data: {e}")
            raise
    
    def GeoBeamUploader(self, geo_model):
        """
        Upload geometry check beam data to the Supabase 6x geometry table.
        
        Takes a Geo6xfffModel instance and uploads all comprehensive geometry
        check data including isocenter, beam, gantry, couch, MLC leaves,
        and jaw measurements.
        
        Args:
            geo_model: Instance of Geo6xfffModel with populated data
            
        Returns:
            dict: Response from Supabase API containing inserted record
            
        Raises:
            Exception: If upload to Supabase fails
        """
        try:
            # Table name for geometry checks
            table_name = "beam_6x"
            
            # Get beam type
            beam_type = geo_model.get_type()
            
            # ---- Extract IsoCenterGroup data ----
            isocenter_data = {
                'isocenter_size': self._convert_decimal_to_float(geo_model.get_IsoCenterSize()),
                'isocenter_mv_offset': self._convert_decimal_to_float(geo_model.get_IsoCenterMVOffset()),
                'isocenter_kv_offset': self._convert_decimal_to_float(geo_model.get_IsoCenterKVOffset()),
            }
            
            # ---- Extract BeamGroup data ----
            beam_data = {
                'relative_output': self._convert_decimal_to_float(geo_model.get_relative_output()),
                'relative_uniformity': self._convert_decimal_to_float(geo_model.get_relative_uniformity()),
                'center_shift': self._convert_decimal_to_float(geo_model.get_center_shift()),
            }
            
            # ---- Extract CollimationGroup data ----
            collimation_data = {
                'collimation_rotation_offset': self._convert_decimal_to_float(geo_model.get_CollimationRotationOffset()),
            }
            
            # ---- Extract GantryGroup data ----
            gantry_data = {
                'gantry_absolute': self._convert_decimal_to_float(geo_model.get_GantryAbsolute()),
                'gantry_relative': self._convert_decimal_to_float(geo_model.get_GantryRelative()),
            }
            
            # ---- Extract EnhancedCouchGroup data ----
            couch_data = {
                'couch_max_position_error': self._convert_decimal_to_float(geo_model.get_CouchMaxPositionError()),
                'couch_lat': self._convert_decimal_to_float(geo_model.get_CouchLat()),
                'couch_lng': self._convert_decimal_to_float(geo_model.get_CouchLng()),
                'couch_vrt': self._convert_decimal_to_float(geo_model.get_CouchVrt()),
                'couch_rtn_fine': self._convert_decimal_to_float(geo_model.get_CouchRtnFine()),
                'couch_rtn_large': self._convert_decimal_to_float(geo_model.get_CouchRtnLarge()),
                'rotation_induced_couch_shift_full_range': self._convert_decimal_to_float(
                    geo_model.get_RotationInducedCouchShiftFullRange()
                ),
            }
            
            # ---- Extract MLC Leaves data (A and B banks, leaves 11-50) ----
            mlc_leaves_a = {}
            mlc_leaves_b = {}
            for i in range(11, 51):
                mlc_leaves_a[f"leaf_{i}"] = self._convert_decimal_to_float(geo_model.get_MLCLeafA(i))
                mlc_leaves_b[f"leaf_{i}"] = self._convert_decimal_to_float(geo_model.get_MLCLeafB(i))
            
            # ---- Extract MLC Offsets ----
            mlc_offset_data = {
                'mlc_max_offset_a': self._convert_decimal_to_float(geo_model.get_MaxOffsetA()),
                'mlc_max_offset_b': self._convert_decimal_to_float(geo_model.get_MaxOffsetB()),
                'mlc_mean_offset_a': self._convert_decimal_to_float(geo_model.get_MeanOffsetA()),
                'mlc_mean_offset_b': self._convert_decimal_to_float(geo_model.get_MeanOffsetB()),
            }
            
            # ---- Extract MLC Backlash data (A and B banks, leaves 11-50) ----
            mlc_backlash_a = {}
            mlc_backlash_b = {}
            for i in range(11, 51):
                mlc_backlash_a[f"leaf_{i}"] = self._convert_decimal_to_float(geo_model.get_MLCBacklashA(i))
                mlc_backlash_b[f"leaf_{i}"] = self._convert_decimal_to_float(geo_model.get_MLCBacklashB(i))
            
            mlc_backlash_data = {
                'mlc_backlash_max_a': self._convert_decimal_to_float(geo_model.get_MLCBacklashMaxA()),
                'mlc_backlash_max_b': self._convert_decimal_to_float(geo_model.get_MLCBacklashMaxB()),
                'mlc_backlash_mean_a': self._convert_decimal_to_float(geo_model.get_MLCBacklashMeanA()),
                'mlc_backlash_mean_b': self._convert_decimal_to_float(geo_model.get_MLCBacklashMeanB()),
            }
            
            # ---- Extract Jaws data ----
            jaws_data = {
                'jaw_x1': self._convert_decimal_to_float(geo_model.get_JawX1()),
                'jaw_x2': self._convert_decimal_to_float(geo_model.get_JawX2()),
                'jaw_y1': self._convert_decimal_to_float(geo_model.get_JawY1()),
                'jaw_y2': self._convert_decimal_to_float(geo_model.get_JawY2()),
            }
            
            # ---- Extract Jaw Parallelism data ----
            jaw_parallelism_data = {
                'jaw_parallelism_x1': self._convert_decimal_to_float(geo_model.get_JawParallelismX1()),
                'jaw_parallelism_x2': self._convert_decimal_to_float(geo_model.get_JawParallelismX2()),
                'jaw_parallelism_y1': self._convert_decimal_to_float(geo_model.get_JawParallelismY1()),
                'jaw_parallelism_y2': self._convert_decimal_to_float(geo_model.get_JawParallelismY2()),
            }
            
            # ---- Combine all data into single record ----
            data = {
                'beam_type': beam_type,
                'measurement_date': self._convert_decimal_to_float(geo_model.get_date()),
                'file_path': geo_model.get_path(),
                
                # IsoCenterGroup
                **isocenter_data,
                
                # BeamGroup
                **beam_data,
                
                # CollimationGroup
                **collimation_data,
                
                # GantryGroup
                **gantry_data,
                
                # EnhancedCouchGroup
                **couch_data,
                
                # MLC Leaves (stored as JSONB in database)
                'mlc_leaves_a': json.dumps(mlc_leaves_a),
                'mlc_leaves_b': json.dumps(mlc_leaves_b),
                
                # MLC Offsets
                **mlc_offset_data,
                
                # MLC Backlash (stored as JSONB in database)
                'mlc_backlash_a': json.dumps(mlc_backlash_a),
                'mlc_backlash_b': json.dumps(mlc_backlash_b),
                **mlc_backlash_data,
                
                # Jaws
                **jaws_data,
                
                # Jaw Parallelism
                **jaw_parallelism_data,
                
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Upload to Supabase
            print(f"Uploading Geometry check (6x) data to table '{table_name}'...")
            print(f"  → Uploading {len(data)} total fields")
            print(f"  → Including 40 MLC leaves per bank (A & B)")
            print(f"  → Including 40 MLC backlash values per bank (A & B)")
            
            response = self.supabase.table(table_name).insert(data).execute()
            
            print(f"✓ Successfully uploaded Geometry check (6x) data")
            return response
            
        except Exception as e:
            print(f"✗ Error uploading Geometry check data: {e}")
            raise


# ---- Example Usage ----
if __name__ == "__main__":
    """
    Example usage of the Uploader class.
    
    This demonstrates how to:
    1. Initialize the Uploader with Supabase credentials
    2. Create and populate model instances
    3. Upload data to Supabase
    """
    
    
    SUPABASE_URL = "https://your-project.supabase.co"
    SUPABASE_KEY = "your-anon-or-service-key"
    
    # Initialize uploader
    uploader = Uploader(SUPABASE_URL, SUPABASE_KEY)
    
    # Example 1: Upload E-beam data
    from ..models.EBeamModel import EBeamModel
    
    ebeam = EBeamModel()
    ebeam.set_type("6e")
    ebeam.set_date(datetime.now())
    ebeam.set_path("/path/to/beam/data")
    ebeam.set_relative_uniformity(Decimal("0.21"))
    ebeam.set_relative_output(Decimal("0.05"))
    
    # uploader.EBeamUploader(ebeam)
    
    # Example 2: Upload X-beam data
    from ..models.XBeamModel import XBeamModel
    
    xbeam = XBeamModel()
    xbeam.set_type("15x")
    xbeam.set_date(datetime.now())
    xbeam.set_path("/path/to/beam/data")
    xbeam.set_relative_uniformity(Decimal("0.22"))
    xbeam.set_relative_output(Decimal("-0.82"))
    xbeam.set_center_shift(Decimal("0.11"))
    
    # uploader.XBeamUploader(xbeam)
    
    # Example 3: Upload Geometry check data
    from ..models.Geo6xfffModel import Geo6xfffModel
    
    geo = Geo6xfffModel()
    geo.set_type("6x")
    geo.set_date(datetime.now())
    geo.set_path("/path/to/beam/data")
    # ... set all other geometry parameters ...
    
    # uploader.GeoBeamUploader(geo)
    
    print("\nUpload examples completed!")

