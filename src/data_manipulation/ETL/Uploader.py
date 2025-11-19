"""
Uploader Module
----------------
This module defines the `Uploader` class, responsible for uploading beam data
from model objects to a database. It follows the Program-to-an-Interface principle,
allowing easy switching between different database management systems.

The module includes:
    - DatabaseAdapter: Abstract interface for database operations
    - SupabaseAdapter: Concrete implementation for Supabase DBMS
    - Uploader: Main class that uses model getters to upload data

Supported beam models:
    - Electron beams: `EBeamModel`
    - X-ray beams: `XBeamModel`
    - Geometric beams: `Geo6xfffModel`
"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional


class DatabaseAdapter(ABC):
    """
    Abstract interface for database operations.
    Implementations should provide concrete methods for connecting and uploading data.
    """

    @abstractmethod
    def connect(self, connection_params: Dict[str, Any]) -> bool:
        """
        Establish connection to the database.
        
        Args:
            connection_params: Dictionary containing connection parameters
                              (e.g., url, key, etc.)
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    def upload_beam_data(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        Upload beam data to the specified table.
        
        Args:
            table_name: Name of the database table
            data: Dictionary containing the data to upload
        
        Returns:
            bool: True if upload successful, False otherwise
        """
        pass

    @abstractmethod
    def close(self):
        """Close the database connection."""
        pass


class SupabaseAdapter(DatabaseAdapter):
    """
    Concrete implementation of DatabaseAdapter for Supabase DBMS.
    Uses the supabase-py library to interact with Supabase.
    """

    def __init__(self):
        self.client = None
        self.connected = False

    def connect(self, connection_params: Dict[str, Any]) -> bool:
        """
        Establish connection to Supabase.
        
        Args:
            connection_params: Dictionary with 'url' and 'key' keys
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            from supabase import create_client, Client
            
            url = connection_params.get('url')
            key = connection_params.get('key')
            
            if not url or not key:
                print("Error: Supabase connection requires 'url' and 'key' parameters")
                return False
            
            self.client: Client = create_client(url, key)
            self.connected = True
            print("Successfully connected to Supabase")
            return True
            
        except ImportError:
            print("Error: supabase-py library not installed. Install with: pip install supabase")
            return False
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
            self.connected = False
            return False

    def upload_beam_data(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        Upload beam data to Supabase table.
        
        Args:
            table_name: Name of the Supabase table
            data: Dictionary containing the data to upload
        
        Returns:
            bool: True if upload successful, False otherwise
        """
        if not self.connected or not self.client:
            print("Error: Not connected to Supabase")
            return False
        
        try:
            # Convert Decimal to float for JSON serialization
            serialized_data = self._serialize_data(data)
            
            # Insert data into Supabase table
            response = self.client.table(table_name).insert(serialized_data).execute()
            
            if response.data:
                print(f"Successfully uploaded data to {table_name}")
                return True
            else:
                print(f"Warning: No data returned from Supabase insert")
                return False
                
        except Exception as e:
            print(f"Error uploading data to Supabase: {e}")
            return False

    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert data types to JSON-serializable formats.
        
        Args:
            data: Dictionary with potentially non-serializable values
        
        Returns:
            Dictionary with serialized values
        """
        serialized = {}
        for key, value in data.items():
            if isinstance(value, Decimal):
                serialized[key] = float(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif value is None:
                serialized[key] = None
            else:
                serialized[key] = value
        return serialized

    def close(self):
        """Close the Supabase connection."""
        self.client = None
        self.connected = False
        print("Supabase connection closed")


class Uploader:
    """
    Handles data upload from model objects to a database.
    Each method corresponds to a specific model type and uses model getters
    to retrieve data for upload.
    """

    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        """
        Initialize the Uploader with a database adapter.
        
        Args:
            db_adapter: Database adapter instance. If None, defaults to SupabaseAdapter
        """
        if db_adapter is None:
            self.db_adapter = SupabaseAdapter()
        else:
            self.db_adapter = db_adapter
        
        self.connected = False

    def connect(self, connection_params: Dict[str, Any]) -> bool:
        """
        Connect to the database using the adapter.
        
        Args:
            connection_params: Dictionary containing connection parameters
        """
        self.connected = self.db_adapter.connect(connection_params)
        return self.connected

    def upload(self, model):
        """
        Automatically calls the correct upload method
        based on the type of model object passed in.

        Supported models:
            - EBeamModel
            - XBeamModel
            - Geo6xfffModel
        """
        if not self.connected:
            print("Error: Not connected to database. Call connect() first.")
            return False

        model_type = type(model).__name__.lower()

        if "ebeam" in model_type:
            return self.eModelUpload(model)
        elif "xbeam" in model_type:
            return self.xModelUpload(model)
        elif "geo" in model_type:
            return self.geoModelUpload(model)
        else:
            raise TypeError(f"Unsupported model type: {type(model).__name__}")

    def uploadTest(self, model):
        """
        Automatically calls the correct upload method
        based on the type of model object passed in, with test output.

        Supported models:
            - EBeamModel
            - XBeamModel
            - Geo6xfffModel
        """
        if not self.connected:
            print("Error: Not connected to database. Call connect() first.")
            return False

        model_type = type(model).__name__.lower()

        if "ebeam" in model_type:
            return self.testeModelUpload(model)
        elif "xbeam" in model_type:
            return self.testxModelUpload(model)
        elif "geo" in model_type:
            return self.testGeoModelUpload(model)
        else:
            raise TypeError(f"Unsupported model type: {type(model).__name__}")

    # --- E-BEAM ---
    def eModelUpload(self, eBeam):
        """
        Upload data for E-beam model to database.
        """
        try:
            # Prepare data dictionary using model getters
            data = {
                'date': eBeam.get_date(),
                'machine_sn': eBeam.get_machine_SN(),
                'beam_type': eBeam.get_type(),
                'is_baseline': eBeam.get_baseline(),
                'relative_output': eBeam.get_relative_output(),
                'relative_uniformity': eBeam.get_relative_uniformity(),
            }

            # Upload to database
            table_name = 'ebeam_data'  # Adjust table name as needed
            return self.db_adapter.upload_beam_data(table_name, data)

        except Exception as e:
            print(f"Error during E-beam upload: {e}")
            return False


    # --- X-BEAM ---
    def xModelUpload(self, xBeam):
        """
        Upload data for X-beam model to database.
        """
        try:
            # Prepare data dictionary using model getters
            data = {
                'date': xBeam.get_date(),
                'machine_sn': xBeam.get_machine_SN(),
                'beam_type': xBeam.get_type(),
                'is_baseline': xBeam.get_baseline(),
                'relative_output': xBeam.get_relative_output(),
                'relative_uniformity': xBeam.get_relative_uniformity(),
                'center_shift': xBeam.get_center_shift(),
            }

            # Upload to database
            table_name = 'xbeam_data'  # Adjust table name as needed
            return self.db_adapter.upload_beam_data(table_name, data)

        except Exception as e:
            print(f"Error during X-beam upload: {e}")
            return False


    # --- GEO MODEL ---
    def geoModelUpload(self, geoModel):
        """
        Upload data for Geo6xfffModel to database.
        """
        try:
            # Prepare data dictionary using model getters
            data = {
                'date': geoModel.get_date(),
                'machine_sn': geoModel.get_machine_SN(),
                'beam_type': geoModel.get_type(),
                'is_baseline': geoModel.get_baseline(),
                
                # IsoCenterGroup
                'iso_center_size': geoModel.get_IsoCenterSize(),
                'iso_center_mv_offset': geoModel.get_IsoCenterMVOffset(),
                'iso_center_kv_offset': geoModel.get_IsoCenterKVOffset(),
                
                # BeamGroup
                'relative_output': geoModel.get_relative_output(),
                'relative_uniformity': geoModel.get_relative_uniformity(),
                'center_shift': geoModel.get_center_shift(),
                
                # CollimationGroup
                'collimation_rotation_offset': geoModel.get_CollimationRotationOffset(),
                
                # GantryGroup
                'gantry_absolute': geoModel.get_GantryAbsolute(),
                'gantry_relative': geoModel.get_GantryRelative(),
                
                # EnhancedCouchGroup
                'couch_max_position_error': geoModel.get_CouchMaxPositionError(),
                'couch_lat': geoModel.get_CouchLat(),
                'couch_lng': geoModel.get_CouchLng(),
                'couch_vrt': geoModel.get_CouchVrt(),
                'couch_rtn_fine': geoModel.get_CouchRtnFine(),
                'couch_rtn_large': geoModel.get_CouchRtnLarge(),
                'rotation_induced_couch_shift_full_range': geoModel.get_RotationInducedCouchShiftFullRange(),
                
                # MLC Offsets
                'max_offset_a': geoModel.get_MaxOffsetA(),
                'max_offset_b': geoModel.get_MaxOffsetB(),
                'mean_offset_a': geoModel.get_MeanOffsetA(),
                'mean_offset_b': geoModel.get_MeanOffsetB(),
                
                # MLC Backlash
                'mlc_backlash_max_a': geoModel.get_MLCBacklashMaxA(),
                'mlc_backlash_max_b': geoModel.get_MLCBacklashMaxB(),
                'mlc_backlash_mean_a': geoModel.get_MLCBacklashMeanA(),
                'mlc_backlash_mean_b': geoModel.get_MLCBacklashMeanB(),
                
                # Jaws Group
                'jaw_x1': geoModel.get_JawX1(),
                'jaw_x2': geoModel.get_JawX2(),
                'jaw_y1': geoModel.get_JawY1(),
                'jaw_y2': geoModel.get_JawY2(),
                
                # Jaw Parallelism
                'jaw_parallelism_x1': geoModel.get_JawParallelismX1(),
                'jaw_parallelism_x2': geoModel.get_JawParallelismX2(),
                'jaw_parallelism_y1': geoModel.get_JawParallelismY1(),
                'jaw_parallelism_y2': geoModel.get_JawParallelismY2(),
            }

            # Upload to database
            table_name = 'geo6xfff_data'  # Adjust table name as needed
            result = self.db_adapter.upload_beam_data(table_name, data)
            
            # Optionally upload MLC leaf data to separate tables
            # This could be done in a separate method or as part of this method
            # For now, we'll skip individual leaf data to keep the main record simple
            
            return result

        except Exception as e:
            print(f"Error during Geo model upload: {e}")
            return False

    def uploadMLCLeaves(self, geoModel, table_name: str = 'mlc_leaves_data'):
        """
        Upload MLC leaf data separately (optional helper method).
        This can be called after geoModelUpload() if you want to store
        individual leaf data in a separate table.
        """
        try:
            leaves_data = []
            
            # Collect all MLC leaf A data
            for i in range(11, 51):
                leaves_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'beam_type': geoModel.get_type(),
                    'leaf_bank': 'A',
                    'leaf_index': i,
                    'leaf_value': geoModel.get_MLCLeafA(i),
                })
            
            # Collect all MLC leaf B data
            for i in range(11, 51):
                leaves_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'beam_type': geoModel.get_type(),
                    'leaf_bank': 'B',
                    'leaf_index': i,
                    'leaf_value': geoModel.get_MLCLeafB(i),
                })
            
            # Upload each leaf record
            success_count = 0
            for leaf_data in leaves_data:
                if self.db_adapter.upload_beam_data(table_name, leaf_data):
                    success_count += 1
            
            print(f"Uploaded {success_count}/{len(leaves_data)} MLC leaf records")
            return success_count == len(leaves_data)

        except Exception as e:
            print(f"Error uploading MLC leaves: {e}")
            return False

    def uploadMLCBacklash(self, geoModel, table_name: str = 'mlc_backlash_data'):
        """
        Upload MLC backlash data separately (optional helper method).
        This can be called after geoModelUpload() if you want to store
        individual backlash data in a separate table.
        """
        try:
            backlash_data = []
            
            # Collect all MLC backlash A data
            for i in range(11, 51):
                backlash_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'beam_type': geoModel.get_type(),
                    'leaf_bank': 'A',
                    'leaf_index': i,
                    'backlash_value': geoModel.get_MLCBacklashA(i),
                })
            
            # Collect all MLC backlash B data
            for i in range(11, 51):
                backlash_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'beam_type': geoModel.get_type(),
                    'leaf_bank': 'B',
                    'leaf_index': i,
                    'backlash_value': geoModel.get_MLCBacklashB(i),
                })
            
            # Upload each backlash record
            success_count = 0
            for backlash_record in backlash_data:
                if self.db_adapter.upload_beam_data(table_name, backlash_record):
                    success_count += 1
            
            
            print(f"Uploaded {success_count}/{len(backlash_data)} MLC backlash records")
            return success_count == len(backlash_data)

        except Exception as e:
            print(f"Error uploading MLC backlash: {e}")
            return False

    def close(self):
        """Close the database connection."""
        if self.db_adapter and hasattr(self.db_adapter, 'close'):
            self.db_adapter.close()


