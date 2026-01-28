"""
Example script demonstrating how to use xml_data_extractor
to extract data from XML files and populate beam models.
"""

import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.data_manipulation.ETL.xml_data_extractor import xml_data_extractor
from src.data_manipulation.models.EBeamModel import EBeamModel
from src.data_manipulation.models.XBeamModel import XBeamModel
from src.data_manipulation.models.Geo6xfffModel import Geo6xfffModel

def main():
    """
    Example usage of xml_data_extractor
    """
    # Example folder path - replace with your actual path
    folder_path = r"MPC-Plus\data\xml_only\NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    
    # Create extractor instance
    extractor = xml_data_extractor()
    
    # Example 1: Extract E-Beam data
    print("=" * 20)
    print("Example 1: E-Beam Model Extraction")
    print("=" * 20)
    ebeam_model = EBeamModel()
    ebeam_model.set_path(folder_path)
    extractor.extractTest(ebeam_model)
    print()
    
    # Example 2: Extract X-Beam data
    print("=" * 20)
    print("Example 2: X-Beam Model Extraction")
    print("=" * 20)
    xbeam_model = XBeamModel()
    xbeam_model.set_path(folder_path)
    extractor.extractTest(xbeam_model)
    print()
    
    # Example 3: Extract Geo Model data
    print("=" * 20)
    print("Example 3: Geo Model Extraction")
    print("=" * 20)
    geo_model = Geo6xfffModel()
    geo_model.set_path(folder_path)
    extractor.extractTest(geo_model)
    print()
    
    # Example 4: Extract without test (just populate model)
    print("=" * 20)
    print("Example 4: Extract without printing (silent)")
    print("=" * 20)
    ebeam_model2 = EBeamModel()
    ebeam_model2.set_path(folder_path)
    extractor.extract(ebeam_model2)
    print(f"Extracted Relative Output: {ebeam_model2.get_relative_output()}")
    print(f"Extracted Relative Uniformity: {ebeam_model2.get_relative_uniformity()}")

if __name__ == "__main__":
    main()
