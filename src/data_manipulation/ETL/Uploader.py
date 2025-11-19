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
                error_msg = "Error: Supabase connection requires 'url' and 'key' parameters"
                logger.error(error_msg)
                print(error_msg)
                return False
            
            self.client: Client = create_client(url, key)
            self.connected = True
            logger.info("Successfully connected to Supabase")
            print("Successfully connected to Supabase")
            return True
            
        except ImportError:
            error_msg = "Error: supabase-py library not installed. Install with: pip install supabase"
            logger.error(error_msg)
            print(error_msg)
            return False
        except Exception as e:
            error_msg = f"Error connecting to Supabase: {e}"
            logger.error(error_msg)
            print(error_msg)
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
            error_msg = "Error: Not connected to Supabase"
            logger.error(error_msg)
            print(error_msg)
            return False
        
        try:
            # Check if machine exists
            response = self.client.table('machines').select('id').eq('id', machine_id).execute()
            
            if response.data and len(response.data) > 0:
                logger.debug(f"Machine {machine_id} already exists")
                return True
            
            # Machine doesn't exist, create it
            logger.info(f"Machine {machine_id} not found, creating it...")
            
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
                logger.info(f"Successfully created machine {machine_id} in location {location}")
                print(f"Created machine {machine_id} in {location}")
                return True
            else:
                logger.warning(f"Warning: No data returned when creating machine {machine_id}")
                return False
                
        except Exception as e:
            error_msg = f"Error ensuring machine exists: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
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
            error_msg = "Error: Not connected to Supabase"
            logger.error(error_msg)
            print(error_msg)
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
                success_msg = f"Successfully uploaded data to {table_name}"
                logger.info(success_msg)
                logger.info(f"Uploaded record: {response.data}")
                print(success_msg)
                return True
            else:
                warning_msg = f"Warning: No data returned from Supabase insert"
                logger.warning(warning_msg)
                print(warning_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error uploading data to Supabase: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
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
            error_msg = "Error: Not connected to database. Call connect() first."
            logger.error(error_msg)
            print(error_msg)
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
            error_msg = "Error: Not connected to database. Call connect() first."
            logger.error(error_msg)
            print(error_msg)
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
            # Prepare data dictionary mapped to 'beams' table schema
            data = {
                'type': eBeam.get_type(),
                'date': eBeam.get_date().date() if hasattr(eBeam.get_date(), 'date') else eBeam.get_date(),
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
            error_msg = f"Error during E-beam upload: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
            return False


    # --- X-BEAM ---
    def xModelUpload(self, xBeam):
        """
        Upload data for X-beam model to database.
        """
        try:
            # Prepare data dictionary mapped to 'beams' table schema
            # Get values, handling Decimal('0.0') which is falsy but valid
            rel_output = xBeam.get_relative_output()
            rel_uniformity = xBeam.get_relative_uniformity()
            center_shift = xBeam.get_center_shift()
            
            data = {
                'type': xBeam.get_type(),
                'date': xBeam.get_date().date() if hasattr(xBeam.get_date(), 'date') else xBeam.get_date(),
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
            error_msg = f"Error during X-beam upload: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
            return False


    # --- GEO MODEL ---
    def geoModelUpload(self, geoModel):
        """
        Upload data for Geo6xfffModel to database.
        Note: The 'beams' table only stores basic beam data. 
        Additional geometry data could be stored in a separate table if needed.
        """
        try:
            # Prepare data dictionary mapped to 'beams' table schema
            # Note: The beams table doesn't have all geometry fields, so we store basic beam info
            # Get values, handling Decimal('0.0') which is falsy but valid
            rel_output = geoModel.get_relative_output()
            rel_uniformity = geoModel.get_relative_uniformity()
            center_shift = geoModel.get_center_shift()
            
            data = {
                'type': geoModel.get_type(),
                'date': geoModel.get_date().date() if hasattr(geoModel.get_date(), 'date') else geoModel.get_date(),
                'path': geoModel.get_path(),
                'relOutput': float(rel_output) if rel_output is not None else None,
                'relUniformity': float(rel_uniformity) if rel_uniformity is not None else None,
                'centerShift': float(center_shift) if center_shift is not None else None,
                'machineId': geoModel.get_machine_SN(),
                'note': f"Baseline: {geoModel.get_baseline()}, Geometry check data available" if geoModel.get_baseline() else "Geometry check data available",
            }

            # Upload to database, passing path for machine creation
            table_name = 'beams'
            result = self.db_adapter.upload_beam_data(table_name, data, path=geoModel.get_path())
            
            # Optionally upload MLC leaf data to separate tables
            # This could be done in a separate method or as part of this method
            # For now, we'll skip individual leaf data to keep the main record simple
            
            return result

        except Exception as e:
            error_msg = f"Error during Geo model upload: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)
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


