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
import json
#---temp---
import os

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
            
            # url = connection_params.get('url')
            # key = connection_params.get('key')
            # print("SUPABASE_URL =", os.getenv("SUPABASE_URL"))
            # print("SUPABASE_URL:", url)

            # connection_params = {
            #     "url": os.getenv("SUPABASE_URL"),
            #     "key": os.getenv("SUPABASE_KEY"),
            # }
            url = connection_params.get('url')
            key = connection_params.get('key')
            # print("SUPABASE_URL =", os.getenv("SUPABASE_URL"))
            # print("SUPABASE_URL:", url)


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

    def _upload_baseline_metrics(self, model, check_type: str):
        """
        Upload baseline data as individual metric records to the baseline table.
        Creates one record per metric (relUniformity, relOutput, centerShift if applicable).
        
        Args:
            model: The beam model (EBeam, XBeam, or GeoModel)
            check_type: "beam" for EBeam/XBeam, "geometry" for GeoModel
        
        Returns:
            bool: True if all metrics uploaded successfully, False otherwise
        """
        try:
            machine_id = model.get_machine_SN()
            beam_variant = model.get_type()  # e.g., "6e", "15x", "6x"
            date = model.get_date()
            
            # List of metrics to upload
            metrics = []
            
            # Add relUniformity
            rel_uniformity = model.get_relative_uniformity()
            if rel_uniformity is not None:
                metrics.append({
                    'machine_id': machine_id,
                    'check_type': check_type,
                    'beam_variant': beam_variant,
                    'metric_type': 'relUniformity',
                    'date': date,
                    'value': rel_uniformity
                })
            
            # Add relOutput
            rel_output = model.get_relative_output()
            if rel_output is not None:
                metrics.append({
                    'machine_id': machine_id,
                    'check_type': check_type,
                    'beam_variant': beam_variant,
                    'metric_type': 'relOutput',
                    'date': date,
                    'value': rel_output
                })
            
            # Add centerShift (only for XBeam and GeoModel, not EBeam)
            if hasattr(model, 'get_center_shift'):
                center_shift = model.get_center_shift()
                if center_shift is not None:
                    metrics.append({
                        'machine_id': machine_id,
                        'check_type': check_type,
                        'beam_variant': beam_variant,
                        'metric_type': 'centerShift',
                        'date': date,
                        'value': center_shift
                    })
            
            # Upload each metric record
            success_count = 0
            for metric_data in metrics:
                if self.db_adapter.upload_beam_data('baselines', metric_data):
                    success_count += 1
                else:
                    print(f"Failed to upload baseline metric: {metric_data['metric_type']}")
            
            print(f"Uploaded {success_count}/{len(metrics)} baseline metric records")
            return success_count == len(metrics) and len(metrics) > 0
            
        except Exception as e:
            print(f"Error uploading baseline metrics: {e}")
            return False

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
        Upload data for E-beam model to the single beam table or baseline table.
        Maps to schema: type, date, path, relUniformity, relOutput, centerShift, machineId, note
        
        For baselines: Uploads individual metric records to baseline table.
        For regular beams: Uploads single record to beam table.
        """
        try:
            # Check if this is a baseline
            if eBeam.get_baseline():
                # Upload to baseline table as individual metric records
                return self._upload_baseline_metrics(eBeam, check_type='beam')
            else:
                # Prepare data dictionary using model getters, matching the beam table schema
                data = {
                    'type': eBeam.get_type(),
                    'date': eBeam.get_date(),
                    'path': eBeam.get_path(),
                    'relUniformity': eBeam.get_relative_uniformity(),
                    'relOutput': eBeam.get_relative_output(),
                    'centerShift': None,  # E-beams don't have centerShift
                    'machineId': eBeam.get_machine_SN(),
                    'note': None  # Add note if available in the model
                }
                return self.db_adapter.upload_beam_data('beam', data)

        except Exception as e:
            print(f"Error during E-beam upload: {e}")
            return False


    # --- X-BEAM ---
    def xModelUpload(self, xBeam):
        """
        Upload data for X-beam model to the single beam table or baseline table.
        Maps to schema: type, date, path, relUniformity, relOutput, centerShift, machineId, note
        
        For baselines: Uploads individual metric records to baseline table.
        For regular beams: Uploads single record to beam table.
        """
        try:
            # Check if this is a baseline
            if xBeam.get_baseline():
                # Upload to baseline table as individual metric records
                return self._upload_baseline_metrics(xBeam, check_type='beam')
            else:
                # Prepare data dictionary using model getters, matching the beam table schema
                data = {
                    'type': xBeam.get_type(),
                    'date': xBeam.get_date(),
                    'path': xBeam.get_path(),
                    'relUniformity': xBeam.get_relative_uniformity(),
                    'relOutput': xBeam.get_relative_output(),
                    'centerShift': xBeam.get_center_shift(),
                    'machineId': xBeam.get_machine_SN(),
                    'note': None  # Add note if available in the model
                }
                return self.db_adapter.upload_beam_data('beam', data)

        except Exception as e:
            print(f"Error during X-beam upload: {e}")
            return False


    # --- GEO MODEL ---
    def geoModelUpload(self, geoModel):
        """
        Upload data for Geo6xfffModel to the single beam table or baseline table.
        Maps to schema: type, date, path, relUniformity, relOutput, centerShift, machineId, note
        
        For baselines: Uploads individual metric records to baseline table.
        For regular beams: Uploads single record to beam table.
        
        Note: Geometry models have additional data (isocenter, gantry, couch, MLC, jaws) 
        that is not stored in the basic beam table. The full extraction code is 
        commented out below for easy re-enabling when geometry tables are created.
        """
        try:
            # Check if this is a baseline
            if geoModel.get_baseline():
                # Upload to baseline table as individual metric records
                return self._upload_baseline_metrics(geoModel, check_type='geometry')
            else:
                # Prepare basic beam data matching the beam table schema
                data = {
                    'type': geoModel.get_type(),
                    'date': geoModel.get_date(),
                    'path': geoModel.get_path(),
                    'relUniformity': geoModel.get_relative_uniformity(),
                    'relOutput': geoModel.get_relative_output(),
                    'centerShift': geoModel.get_center_shift(),
                    'machineId': geoModel.get_machine_SN(),
                    'note': None  # Add note if available in the model
                }
                result = self.db_adapter.upload_beam_data('beam', data)
            
            # ========================================================================
            # COMMENTED OUT: Full geometry data extraction
            # Uncomment when geometry_data table is created
            # ========================================================================
            
            # # ---- Extract IsoCenterGroup data ----
            # isocenter_data = {
            #     'beam_id': result_id,  # Foreign key to beam table
            #     'isoCenterSize': geoModel.get_IsoCenterSize(),
            #     'isoCenterMVOffset': geoModel.get_IsoCenterMVOffset(),
            #     'isoCenterKVOffset': geoModel.get_IsoCenterKVOffset(),
            # }
            # 
            # # ---- Extract CollimationGroup data ----
            # collimation_data = {
            #     'beam_id': result_id,
            #     'collimationRotationOffset': geoModel.get_CollimationRotationOffset(),
            # }
            # 
            # # ---- Extract GantryGroup data ----
            # gantry_data = {
            #     'beam_id': result_id,
            #     'gantryAbsolute': geoModel.get_GantryAbsolute(),
            #     'gantryRelative': geoModel.get_GantryRelative(),
            # }
            # 
            # # ---- Extract EnhancedCouchGroup data ----
            # couch_data = {
            #     'beam_id': result_id,
            #     'couchMaxPositionError': geoModel.get_CouchMaxPositionError(),
            #     'couchLat': geoModel.get_CouchLat(),
            #     'couchLng': geoModel.get_CouchLng(),
            #     'couchVrt': geoModel.get_CouchVrt(),
            #     'couchRtnFine': geoModel.get_CouchRtnFine(),
            #     'couchRtnLarge': geoModel.get_CouchRtnLarge(),
            #     'rotationInducedCouchShiftFullRange': geoModel.get_RotationInducedCouchShiftFullRange(),
            # }
            # 
            # # ---- Extract MLC Leaves data (A and B banks, leaves 11-50) ----
            # mlc_leaves_a = {}
            # mlc_leaves_b = {}
            # for i in range(11, 51):
            #     mlc_leaves_a[f"leaf_{i}"] = geoModel.get_MLCLeafA(i)
            #     mlc_leaves_b[f"leaf_{i}"] = geoModel.get_MLCLeafB(i)
            # 
            # # ---- Extract MLC Offsets ----
            # mlc_offset_data = {
            #     'beam_id': result_id,
            #     'mlcMaxOffsetA': geoModel.get_MaxOffsetA(),
            #     'mlcMaxOffsetB': geoModel.get_MaxOffsetB(),
            #     'mlcMeanOffsetA': geoModel.get_MeanOffsetA(),
            #     'mlcMeanOffsetB': geoModel.get_MeanOffsetB(),
            #     'mlcLeavesA': json.dumps(mlc_leaves_a),  # Store as JSONB
            #     'mlcLeavesB': json.dumps(mlc_leaves_b),  # Store as JSONB
            # }
            # 
            # # ---- Extract MLC Backlash data (A and B banks, leaves 11-50) ----
            # mlc_backlash_a = {}
            # mlc_backlash_b = {}
            # for i in range(11, 51):
            #     mlc_backlash_a[f"leaf_{i}"] = geoModel.get_MLCBacklashA(i)
            #     mlc_backlash_b[f"leaf_{i}"] = geoModel.get_MLCBacklashB(i)
            # 
            # mlc_backlash_data = {
            #     'beam_id': result_id,
            #     'mlcBacklashMaxA': geoModel.get_MLCBacklashMaxA(),
            #     'mlcBacklashMaxB': geoModel.get_MLCBacklashMaxB(),
            #     'mlcBacklashMeanA': geoModel.get_MLCBacklashMeanA(),
            #     'mlcBacklashMeanB': geoModel.get_MLCBacklashMeanB(),
            #     'mlcBacklashA': json.dumps(mlc_backlash_a),  # Store as JSONB
            #     'mlcBacklashB': json.dumps(mlc_backlash_b),  # Store as JSONB
            # }
            # 
            # # ---- Extract Jaws data ----
            # jaws_data = {
            #     'beam_id': result_id,
            #     'jawX1': geoModel.get_JawX1(),
            #     'jawX2': geoModel.get_JawX2(),
            #     'jawY1': geoModel.get_JawY1(),
            #     'jawY2': geoModel.get_JawY2(),
            # }
            # 
            # # ---- Extract Jaw Parallelism data ----
            # jaw_parallelism_data = {
            #     'beam_id': result_id,
            #     'jawParallelismX1': geoModel.get_JawParallelismX1(),
            #     'jawParallelismX2': geoModel.get_JawParallelismX2(),
            #     'jawParallelismY1': geoModel.get_JawParallelismY1(),
            #     'jawParallelismY2': geoModel.get_JawParallelismY2(),
            # }
            # 
            # # ---- Upload to geometry tables ----
            # # Uncomment and adjust table names when geometry tables are created
            # # self.db_adapter.upload_beam_data('geometry_isocenter', isocenter_data)
            # # self.db_adapter.upload_beam_data('geometry_collimation', collimation_data)
            # # self.db_adapter.upload_beam_data('geometry_gantry', gantry_data)
            # # self.db_adapter.upload_beam_data('geometry_couch', couch_data)
            # # self.db_adapter.upload_beam_data('geometry_mlc', mlc_offset_data)
            # # self.db_adapter.upload_beam_data('geometry_mlc_backlash', mlc_backlash_data)
            # # self.db_adapter.upload_beam_data('geometry_jaws', jaws_data)
            # # self.db_adapter.upload_beam_data('geometry_jaw_parallelism', jaw_parallelism_data)
            
            # ========================================================================
            # END OF COMMENTED GEOMETRY DATA
            # ========================================================================
            
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
        self.db_adapter.close()
        self.connected = False
