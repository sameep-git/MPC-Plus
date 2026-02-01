"""
Extract relative uniformity and relative output from e-beam Results.xml
"""

import os
import sys
import xml.etree.ElementTree as ET


def is_ebeam_folder(folder_path):
    """
    Check if folder is an e-beam folder
    
    Args:
        folder_path: Path to the folder to check
        
    Returns:
        bool: True if folder name contains e-beam indicators ('6e', '16e', or 'BeamCheckTemplate')
    """
    folder_name = os.path.basename(folder_path)
    # Check for e-beam indicators in folder name
    return '6e' in folder_name or '16e' in folder_name or 'BeamCheckTemplate' in folder_name


def extract_ebeam_values(folder_path):
    """
    Extract relative output and relative uniformity from e-beam Results.xml
    
    Args:
        folder_path: Path to the folder containing Results.xml
        
    Returns:
        tuple: (output_percentage, uniformity_percentage) or (None, None) if extraction fails
    """
    # Try to resolve path - if relative path doesn't exist, try relative to MPC-Plus
    if not os.path.exists(folder_path):
        # Try relative to MPC-Plus folder (common parent directory)
        # Navigate up from current script: ETL -> data_manipulation -> src -> MPC-Plus
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mpc_plus_dir = os.path.abspath(os.path.join(script_dir, '../../..'))
        
        # Try multiple possible locations
        possible_paths = [
            os.path.join(mpc_plus_dir, folder_path),  # Directly in MPC-Plus
            os.path.join(mpc_plus_dir, 'data', 'csv_data', folder_path)  # In data/csv_data subdirectory
        ]
        
        found_path = None
        for alt_path in possible_paths:
            if os.path.exists(alt_path):
                found_path = alt_path
                break
        
        if found_path:
            folder_path = found_path
        else:
            print(f"Error: Folder not found: {folder_path}")
            return None, None
    
    # Construct path to Results.xml file
    results_path = os.path.join(folder_path, "Results.xml")
    
    # Validate that Results.xml exists
    if not os.path.exists(results_path):
        print(f"Error: Results.xml not found in {folder_path}")
        return None, None
    
    # Validate that this is an e-beam folder
    if not is_ebeam_folder(folder_path):
        print(f"Error: Not an e-beam folder")
        return None, None
    
    # Parse the XML file
    tree = ET.parse(results_path)
    root = tree.getroot()
    
    # Initialize variables to store extracted values
    relative_output = None
    relative_uniformity = None
    
    # Find BeamProfileCheck element in the XML tree
    # XML namespaces are handled by checking the xsi:type attribute
    for elem in root.iter():
        # Check if this element is a BeamProfileCheck type
        if elem.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'BeamProfileCheck':
            # Iterate through child elements to find RelativeOutput and RelativeUniformity
            for child in elem:
                # Extract tag name by removing namespace prefix (everything before '}')
                tag = child.tag.split('}')[-1]
                if tag == 'RelativeOutput' and child.text:
                    relative_output = float(child.text.strip())
                elif tag == 'RelativeUniformity' and child.text:
                    relative_uniformity = float(child.text.strip())
            # Found the element, no need to continue searching
            break
    
    # Validate that both values were found
    if relative_output is None or relative_uniformity is None:
        return None, None
    
    # Convert relative values to percentages:
    # - RelativeOutput: subtract 1 and multiply by 100 (e.g., 1.02 -> 2.0%)
    # - RelativeUniformity: multiply by 100 (e.g., 0.015 -> 1.5%)
    output = (relative_output - 1) * 100
    uniformity = relative_uniformity * 100
    
    return output, uniformity


if __name__ == "__main__":
    # Command-line interface for testing the extractor
    if len(sys.argv) < 2:
        print("Usage: ebeam_extractor.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output, uniformity = extract_ebeam_values(folder_path)
    
    # Display results if extraction was successful
    if output is not None and uniformity is not None:
        print(f"Relative Output: {output:.2f}%")
        print(f"Relative Uniformity: {uniformity:.2f}%")
    else:
        print("Failed to extract values")
        sys.exit(1)
