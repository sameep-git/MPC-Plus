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
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, Optional
import logging
import os
import json

# Set up logger for this module
logger = logging.getLogger(__name__)


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
    def upload_beam_data(self, table_name: str, data: Dict[str, Any], path: str = None) -> bool:
        """
        Upload beam data to the specified table.
        
        Args:
            table_name: Name of the database table
            data: Dictionary containing the data to upload
            path: Optional path to extract location from for machine creation
        
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
                logger.error("Supabase connection requires 'url' and 'key' parameters")
                return False
            
            self.client: Client = create_client(url, key)
            self.connected = True
            logger.info("Successfully connected to Supabase")
            return True
            
        except ImportError:
            logger.error("supabase-py library not installed. Install with: pip install supabase")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Supabase: {e}")
            self.connected = False
            return False

    def ensure_machine_exists(self, machine_id: str, path: str = None) -> bool:
        """
        Ensure a machine exists in the machines table before uploading beams.
        Creates the machine if it doesn't exist.
        
        Args:
            machine_id: The machine ID (serial number)
            path: Optional path to extract location from (e.g., "/Volumes/Lexar/MPC Data/Arlington/...")
        
        Returns:
            bool: True if machine exists or was created successfully, False otherwise
        """
        if not self.connected or not self.client:
            logger.error("Not connected to Supabase")
            return False
        
        try:
            # Check if machine exists
            response = self.client.table('machines').select('id').eq('id', machine_id).execute()
            
            if response.data and len(response.data) > 0:
                logger.debug(f"Machine {machine_id} already exists")
                return True
            
            # Machine doesn't exist, create it
            logger.info(f"Creating machine {machine_id}...")
            
            # Extract location from path if provided
            location = "Unknown"
            if path:
                # Try to extract location from path (e.g., "/Volumes/Lexar/MPC Data/Arlington/..." -> "Arlington")
                path_parts = path.split(os.sep)
                for part in path_parts:
                    if part in ["Arlington", "Weatherford"]:
                        location = part
                        break
            
            # Create machine with default values
            machine_data = {
                'id': machine_id,
                'name': f"Machine {machine_id}",
                'location': location,
                'type': 'NDS-WKS'  # Default type based on folder naming pattern
            }
            
            response = self.client.table('machines').insert(machine_data).execute()
            
            if response.data:
                logger.info(f"Created machine {machine_id} in location {location}")
                return True
            else:
                logger.warning(f"No data returned when creating machine {machine_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error ensuring machine exists: {e}", exc_info=True)
            return False

    def upload_beam_data(self, table_name: str, data: Dict[str, Any], path: str = None) -> bool:
        """
        Upload beam data to Supabase table.
        
        Args:
            table_name: Name of the Supabase table
            data: Dictionary containing the data to upload
            path: Optional path to extract location from for machine creation
        
        Returns:
            bool: True if upload successful, False otherwise
        """
        if not self.connected or not self.client:
            logger.error("Not connected to Supabase")
            return False
        
        try:
            # Ensure machine exists before uploading beam
            machine_id = data.get('machineId')
            if machine_id:
                if not self.ensure_machine_exists(machine_id, path):
                    logger.warning(f"Could not ensure machine {machine_id} exists, but continuing with upload attempt")
            
            # Convert Decimal to float for JSON serialization
            serialized_data = self._serialize_data(data)
            logger.debug(f"Uploading data to {table_name}: {serialized_data}")
            
            # Insert data into Supabase table
            response = self.client.table(table_name).insert(serialized_data).execute()
            
            if response.data:
                logger.info(f"Successfully uploaded data to {table_name}")
                return True
            else:
                logger.warning("No data returned from Supabase insert")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading data to Supabase: {e}", exc_info=True)
            return False

    def upload_geocheck_data(self, data: Dict[str, Any], path: str = None) -> Optional[str]:
        """
        Upload geometry check data to geochecks table.
        Note: MLC leaves and backlash should NOT be included here - they go to separate tables.
        
        Args:
            data: Dictionary containing the geocheck data to upload (geometry data only: jaws, couch, gantry, etc.)
            path: Optional path to extract location from for machine creation
        
        Returns:
            str: The geocheck_id if upload successful, None otherwise
        """
        if not self.connected or not self.client:
            logger.error("Not connected to Supabase")
            return None
        
        try:
            # Ensure machine exists before uploading geocheck
            machine_id = data.get('machine_id')
            if machine_id:
                if not self.ensure_machine_exists(machine_id, path):
                    logger.warning(f"Could not ensure machine {machine_id} exists, but continuing with upload attempt")
            
            # Remove MLC data if accidentally included (it goes to separate tables)
            data.pop('mlc_leaves_a', None)
            data.pop('mlc_leaves_b', None)
            data.pop('mlc_backlash_a', None)
            data.pop('mlc_backlash_b', None)
            
            # Convert Decimal to float for JSON serialization
            serialized_data = self._serialize_data(data)
            logger.debug(f"Uploading geocheck data: {serialized_data}")
            
            # Insert data into geochecks table
            response = self.client.table('geochecks').insert(serialized_data).execute()
            
            if response.data and len(response.data) > 0:
                geocheck_id = response.data[0].get('id')
                logger.info(f"Successfully uploaded geocheck data with id: {geocheck_id}")
                return geocheck_id
            else:
                logger.warning("No data returned from Supabase geocheck insert")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading geocheck data to Supabase: {e}", exc_info=True)
            return None

    def upload_mlc_leaves(self, geocheck_id: str, leaves_data: list, bank: str) -> bool:
        """
        Upload MLC leaves data to geocheck_mlc_leaves_a or geocheck_mlc_leaves_b table.
        
        Args:
            geocheck_id: The geocheck ID to associate leaves with
            leaves_data: List of dictionaries with 'leaf_number' and 'leaf_value'
            bank: Either 'a' or 'b' to determine which table to use
        
        Returns:
            bool: True if all leaves uploaded successfully, False otherwise
        """
        if not self.connected or not self.client:
            logger.error("Not connected to Supabase")
            return False
        
        if not geocheck_id or not leaves_data:
            return False
        
        table_name = f'geocheck_mlc_leaves_{bank.lower()}'
        
        try:
            # Prepare data with geocheck_id
            upload_data = []
            for leaf in leaves_data:
                leaf_record = {
                    'geocheck_id': geocheck_id,
                    'leaf_number': leaf.get('leaf_number'),
                    'leaf_value': float(leaf.get('leaf_value')) if leaf.get('leaf_value') is not None else None
                }
                upload_data.append(leaf_record)
            
            # Insert all leaves at once
            response = self.client.table(table_name).insert(upload_data).execute()
            
            if response.data:
                logger.info(f"Successfully uploaded {len(upload_data)} MLC leaves to {table_name}")
                return True
            else:
                logger.warning(f"No data returned from {table_name} insert")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading MLC leaves to {table_name}: {e}", exc_info=True)
            return False

    def upload_mlc_backlash(self, geocheck_id: str, backlash_data: list, bank: str) -> bool:
        """
        Upload MLC backlash data to geocheck_mlc_backlash_a or geocheck_mlc_backlash_b table.
        
        Args:
            geocheck_id: The geocheck ID to associate backlash with
            backlash_data: List of dictionaries with 'leaf_number' and 'backlash_value'
            bank: Either 'a' or 'b' to determine which table to use
        
        Returns:
            bool: True if all backlash data uploaded successfully, False otherwise
        """
        if not self.connected or not self.client:
            logger.error("Not connected to Supabase")
            return False
        
        if not geocheck_id or not backlash_data:
            return False
        
        table_name = f'geocheck_mlc_backlash_{bank.lower()}'
        
        try:
            # Prepare data with geocheck_id
            upload_data = []
            for backlash in backlash_data:
                backlash_record = {
                    'geocheck_id': geocheck_id,
                    'leaf_number': backlash.get('leaf_number'),
                    'backlash_value': float(backlash.get('backlash_value')) if backlash.get('backlash_value') is not None else None
                }
                upload_data.append(backlash_record)
            
            # Insert all backlash records at once
            response = self.client.table(table_name).insert(upload_data).execute()
            
            if response.data:
                logger.info(f"Successfully uploaded {len(upload_data)} MLC backlash records to {table_name}")
                return True
            else:
                logger.warning(f"No data returned from {table_name} insert")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading MLC backlash to {table_name}: {e}", exc_info=True)
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
            elif isinstance(value, (datetime, date)):
                # Convert both datetime and date objects to ISO format strings
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
        logger.info("Supabase connection closed")


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

    def close(self):
        """
        Close the database connection using the adapter.
        """
        if self.db_adapter:
            self.db_adapter.close()
        self.connected = False

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
            logger.error("Not connected to database. Call connect() first.")
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
            logger.error("Not connected to database. Call connect() first.")
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
        Upload data for E-beam model to the single beam table.
        Maps to schema: type, date, path, relUniformity, relOutput, centerShift, machineId, note
        """
        try:
            # Prepare data dictionary mapped to 'beams' table schema
            data = {
                'type': eBeam.get_type(),
                'date': eBeam.get_date(),
                'path': eBeam.get_path(),
                'relOutput': float(eBeam.get_relative_output()) if eBeam.get_relative_output() else None,
                'relUniformity': float(eBeam.get_relative_uniformity()) if eBeam.get_relative_uniformity() else None,
                'centerShift': None,  # E-beams don't have center shift
                'machineId': eBeam.get_machine_SN(),
                'note': f"Baseline: {eBeam.get_baseline()}" if eBeam.get_baseline() else None,
            }

            # Upload to database, passing path for machine creation
            table_name = 'beams'
            return self.db_adapter.upload_beam_data(table_name, data, path=eBeam.get_path())

        except Exception as e:
            logger.error(f"Error during E-beam upload: {e}", exc_info=True)
            return False


    # --- X-BEAM ---
    def xModelUpload(self, xBeam):
        """
        Upload data for X-beam model to the single beam table.
        Maps to schema: type, date, path, relUniformity, relOutput, centerShift, machineId, note
        """
        try:
            # Prepare data dictionary mapped to 'beams' table schema
            # Get values, handling Decimal('0.0') which is falsy but valid
            rel_output = xBeam.get_relative_output()
            rel_uniformity = xBeam.get_relative_uniformity()
            center_shift = xBeam.get_center_shift()
            
            data = {
                'type': xBeam.get_type(),
                'date': xBeam.get_date(),
                'path': xBeam.get_path(),
                'relOutput': float(rel_output) if rel_output is not None else None,
                'relUniformity': float(rel_uniformity) if rel_uniformity is not None else None,
                'centerShift': float(center_shift) if center_shift is not None else None,
                'machineId': xBeam.get_machine_SN(),
                'note': f"Baseline: {xBeam.get_baseline()}" if xBeam.get_baseline() else None,
            }

            # Upload to database, passing path for machine creation
            table_name = 'beams'
            return self.db_adapter.upload_beam_data(table_name, data, path=xBeam.get_path())

        except Exception as e:
            logger.error(f"Error during X-beam upload: {e}", exc_info=True)
            return False


    # --- GEO MODEL ---
    def geoModelUpload(self, geoModel):
        """
        Upload data for Geo6xfffModel to database.
        The 6x beam data (relative_output, relative_uniformity, center_shift) goes to 'beams' table as an X-beam.
        Geometry-specific data (jaws, couch, gantry, etc.) goes to 'geochecks' table.
        MLC leaves and backlash go to separate tables: geocheck_mlc_leaves_a/b and geocheck_mlc_backlash_a/b.
        """
        try:
            # Step 1: Extract and upload 6x beam data to 'beams' table (as an X-beam)
            rel_output = geoModel.get_relative_output()
            rel_uniformity = geoModel.get_relative_uniformity()
            center_shift = geoModel.get_center_shift()
            
            beam_data = {
                'type': geoModel.get_type(),  # "6x" - treated as an X-beam
                'date': geoModel.get_date(),
                'path': geoModel.get_path(),
                'relOutput': float(rel_output) if rel_output is not None else None,
                'relUniformity': float(rel_uniformity) if rel_uniformity is not None else None,
                'centerShift': float(center_shift) if center_shift is not None else None,
                'machineId': geoModel.get_machine_SN(),
                'note': f"Baseline: {geoModel.get_baseline()}, Geometry check data available" if geoModel.get_baseline() else "Geometry check data available",
            }

            # Upload 6x beam to beams table
            beam_result = self.db_adapter.upload_beam_data('beams', beam_data, path=geoModel.get_path())
            if not beam_result:
                logger.warning("Failed to upload 6x beam data, but continuing with geometry data upload")
            
            # Check if this is BeamCheckTemplate6xFFF - these should NOT go to geochecks
            path = geoModel.get_path()
            is_beamcheck_6xfff = "BeamCheckTemplate6xFFF" in path
            
            if is_beamcheck_6xfff:
                # BeamCheckTemplate6xFFF only goes to beams table, not geochecks
                logger.info("BeamCheckTemplate6xFFF detected - skipping geochecks upload (beam data only)")
                return beam_result
            
            # Step 2: Upload geometry data to 'geochecks' table (without MLC leaves/backlash)
            # ID will be auto-generated by upload_geocheck_data if not provided
            # Note: 'type' column doesn't exist in geochecks table - beam type is stored in beams table
            geocheck_data = {
                'path': geoModel.get_path(),
                'machine_id': geoModel.get_machine_SN(),
                'date': geoModel.get_date(),
                # IsoCenterGroup
                'iso_center_size': float(geoModel.get_IsoCenterSize()) if geoModel.get_IsoCenterSize() is not None else None,
                'iso_center_mv_offset': float(geoModel.get_IsoCenterMVOffset()) if geoModel.get_IsoCenterMVOffset() is not None else None,
                'iso_center_kv_offset': float(geoModel.get_IsoCenterKVOffset()) if geoModel.get_IsoCenterKVOffset() is not None else None,
                # BeamGroup (already in beams table, but also in geochecks for reference)
                'relative_output': float(rel_output) if rel_output is not None else None,
                'relative_uniformity': float(rel_uniformity) if rel_uniformity is not None else None,
                'center_shift': float(center_shift) if center_shift is not None else None,
                # CollimationGroup
                'collimation_rotation_offset': float(geoModel.get_CollimationRotationOffset()) if geoModel.get_CollimationRotationOffset() is not None else None,
                # GantryGroup
                'gantry_absolute': float(geoModel.get_GantryAbsolute()) if geoModel.get_GantryAbsolute() is not None else None,
                'gantry_relative': float(geoModel.get_GantryRelative()) if geoModel.get_GantryRelative() is not None else None,
                # EnhancedCouchGroup
                'couch_max_position_error': float(geoModel.get_CouchMaxPositionError()) if geoModel.get_CouchMaxPositionError() is not None else None,
                'couch_lat': float(geoModel.get_CouchLat()) if geoModel.get_CouchLat() is not None else None,
                'couch_lng': float(geoModel.get_CouchLng()) if geoModel.get_CouchLng() is not None else None,
                'couch_vrt': float(geoModel.get_CouchVrt()) if geoModel.get_CouchVrt() is not None else None,
                'couch_rtn_fine': float(geoModel.get_CouchRtnFine()) if geoModel.get_CouchRtnFine() is not None else None,
                'couch_rtn_large': float(geoModel.get_CouchRtnLarge()) if geoModel.get_CouchRtnLarge() is not None else None,
                'rotation_induced_couch_shift_full_range': float(geoModel.get_RotationInducedCouchShiftFullRange()) if geoModel.get_RotationInducedCouchShiftFullRange() is not None else None,
                # MLCGroup - Offsets (summary stats only, not individual leaves)
                'max_offset_a': float(geoModel.get_MaxOffsetA()) if geoModel.get_MaxOffsetA() is not None else None,
                'max_offset_b': float(geoModel.get_MaxOffsetB()) if geoModel.get_MaxOffsetB() is not None else None,
                'mean_offset_a': float(geoModel.get_MeanOffsetA()) if geoModel.get_MeanOffsetA() is not None else None,
                'mean_offset_b': float(geoModel.get_MeanOffsetB()) if geoModel.get_MeanOffsetB() is not None else None,
                # MLCBacklashGroup - Summary stats only (not individual leaves)
                'mlc_backlash_max_a': float(geoModel.get_MLCBacklashMaxA()) if geoModel.get_MLCBacklashMaxA() is not None else None,
                'mlc_backlash_max_b': float(geoModel.get_MLCBacklashMaxB()) if geoModel.get_MLCBacklashMaxB() is not None else None,
                'mlc_backlash_mean_a': float(geoModel.get_MLCBacklashMeanA()) if geoModel.get_MLCBacklashMeanA() is not None else None,
                'mlc_backlash_mean_b': float(geoModel.get_MLCBacklashMeanB()) if geoModel.get_MLCBacklashMeanB() is not None else None,
                # JawsGroup
                'jaw_x1': float(geoModel.get_JawX1()) if geoModel.get_JawX1() is not None else None,
                'jaw_x2': float(geoModel.get_JawX2()) if geoModel.get_JawX2() is not None else None,
                'jaw_y1': float(geoModel.get_JawY1()) if geoModel.get_JawY1() is not None else None,
                'jaw_y2': float(geoModel.get_JawY2()) if geoModel.get_JawY2() is not None else None,
                # JawsParallelismGroup
                'jaw_parallelism_x1': float(geoModel.get_JawParallelismX1()) if geoModel.get_JawParallelismX1() is not None else None,
                'jaw_parallelism_x2': float(geoModel.get_JawParallelismX2()) if geoModel.get_JawParallelismX2() is not None else None,
                'jaw_parallelism_y1': float(geoModel.get_JawParallelismY1()) if geoModel.get_JawParallelismY1() is not None else None,
                'jaw_parallelism_y2': float(geoModel.get_JawParallelismY2()) if geoModel.get_JawParallelismY2() is not None else None,
            }
            
            geocheck_id_result = self.db_adapter.upload_geocheck_data(geocheck_data, path=geoModel.get_path())
            if not geocheck_id_result:
                logger.error("Failed to upload geocheck data, cannot proceed with MLC data")
                return False
            
            # Step 3: Upload MLC leaves data to separate tables
            # Determine leaf range based on template type
            # GeometryCheckTemplate6xMVkVEnhancedCouch only has leaves 11-50
            if "GeometryCheckTemplate6xMVkVEnhancedCouch" in path:
                leaf_range = range(11, 51)  # Only leaves 11-50 for this template
            else:
                leaf_range = range(1, 61)  # Leaves 1-60 for other templates (e.g., BeamCheckTemplate6xFFF)
            
            leaves_a_data = []
            leaves_b_data = []
            for i in leaf_range:
                leaf_a_val = geoModel.get_MLCLeafA(i)
                leaf_b_val = geoModel.get_MLCLeafB(i)
                
                leaves_a_data.append({
                    'leaf_number': i,
                    'leaf_value': float(leaf_a_val) if leaf_a_val is not None else None
                })
                leaves_b_data.append({
                    'leaf_number': i,
                    'leaf_value': float(leaf_b_val) if leaf_b_val is not None else None
                })
            
            leaves_a_result = self.db_adapter.upload_mlc_leaves(geocheck_id_result, leaves_a_data, 'a')
            leaves_b_result = self.db_adapter.upload_mlc_leaves(geocheck_id_result, leaves_b_data, 'b')
            
            # Step 4: Upload MLC backlash data to separate tables
            # Use same leaf range as determined above
            backlash_a_data = []
            backlash_b_data = []
            for i in leaf_range:
                backlash_a_val = geoModel.get_MLCBacklashA(i)
                backlash_b_val = geoModel.get_MLCBacklashB(i)
                
                backlash_a_data.append({
                    'leaf_number': i,
                    'backlash_value': float(backlash_a_val) if backlash_a_val is not None else None
                })
                backlash_b_data.append({
                    'leaf_number': i,
                    'backlash_value': float(backlash_b_val) if backlash_b_val is not None else None
                })
            
            backlash_a_result = self.db_adapter.upload_mlc_backlash(geocheck_id_result, backlash_a_data, 'a')
            backlash_b_result = self.db_adapter.upload_mlc_backlash(geocheck_id_result, backlash_b_data, 'b')
            
            # Return True if all critical uploads succeeded
            # Beam upload is optional (we log warning but continue)
            # Geocheck, leaves, and backlash are all required
            overall_success = (geocheck_id_result is not None and 
                             leaves_a_result and leaves_b_result and 
                             backlash_a_result and backlash_b_result)
            
            if overall_success:
                logger.info("Successfully uploaded all geometry check data")
            else:
                logger.warning("Some geometry check data uploads may have failed")
            
            return overall_success

        except Exception as e:
            logger.error(f"Error during Geo model upload: {e}", exc_info=True)
            return False

    def uploadMLCLeaves(self, geoModel, table_name: str = 'mlc_leaves_data'):
        """
        Upload MLC leaf data separately (optional helper method).
        This can be called after geoModelUpload() if you want to store
        individual leaf data in a separate table.
        """
        try:
            leaves_data = []
            
            # Collect all MLC leaf A data (leaves 1-60)
            for i in range(1, 61):
                leaves_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'leaf_bank': 'A',
                    'leaf_index': i,
                    'leaf_value': geoModel.get_MLCLeafA(i),
                })
            
            # Collect all MLC leaf B data (leaves 1-60)
            for i in range(1, 61):
                leaves_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'leaf_bank': 'B',
                    'leaf_index': i,
                    'leaf_value': geoModel.get_MLCLeafB(i),
                })
            
            # Upload each leaf record
            success_count = 0
            for leaf_data in leaves_data:
                if self.db_adapter.upload_beam_data(table_name, leaf_data):
                    success_count += 1
            
            logger.info(f"Uploaded {success_count}/{len(leaves_data)} MLC leaf records")
            return success_count == len(leaves_data)

        except Exception as e:
            logger.error(f"Error uploading MLC leaves: {e}", exc_info=True)
            return False

    def uploadMLCBacklash(self, geoModel, table_name: str = 'mlc_backlash_data'):
        """
        Upload MLC backlash data separately (optional helper method).
        This can be called after geoModelUpload() if you want to store
        individual backlash data in a separate table.
        """
        try:
            backlash_data = []
            
            # Collect all MLC backlash A data (leaves 1-60)
            for i in range(1, 61):
                backlash_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'leaf_bank': 'A',
                    'leaf_index': i,
                    'backlash_value': geoModel.get_MLCBacklashA(i),
                })
            
            # Collect all MLC backlash B data (leaves 1-60)
            for i in range(1, 61):
                backlash_data.append({
                    'date': geoModel.get_date(),
                    'machine_sn': geoModel.get_machine_SN(),
                    'leaf_bank': 'B',
                    'leaf_index': i,
                    'backlash_value': geoModel.get_MLCBacklashB(i),
                })
            
            # Upload each backlash record
            success_count = 0
            for backlash_record in backlash_data:
                if self.db_adapter.upload_beam_data(table_name, backlash_record):
                    success_count += 1
            
            logger.info(f"Uploaded {success_count}/{len(backlash_data)} MLC backlash records")
            return success_count == len(backlash_data)

        except Exception as e:
            logger.error(f"Error uploading MLC backlash: {e}", exc_info=True)
            return False

    def close(self):
        """Close the database connection."""
        if self.db_adapter and hasattr(self.db_adapter, 'close'):
            self.db_adapter.close()


