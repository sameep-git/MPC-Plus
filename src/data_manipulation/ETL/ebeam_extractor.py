"""
Extract relative uniformity and relative output from e-beam Results.xml
"""

import os
import sys
import xml.etree.ElementTree as ET


def is_ebeam_folder(folder_path):
    """Check if folder is an e-beam folder"""
    folder_name = os.path.basename(folder_path)
    return '6e' in folder_name or '16e' in folder_name or 'BeamCheckTemplate' in folder_name


def extract_ebeam_values(folder_path):
    """Extract relative output and relative uniformity from Results.xml"""
    # Try to resolve path - if relative path doesn't exist, try relative to MPC-Plus
    if not os.path.exists(folder_path):
        # Try relative to MPC-Plus folder (common parent directory)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mpc_plus_dir = os.path.abspath(os.path.join(script_dir, '../../..'))
        alt_path = os.path.join(mpc_plus_dir, folder_path)
        if os.path.exists(alt_path):
            folder_path = alt_path
        else:
            print(f"Error: Folder not found: {folder_path}")
            return None, None
    
    results_path = os.path.join(folder_path, "Results.xml")
    
    if not os.path.exists(results_path):
        print(f"Error: Results.xml not found in {folder_path}")
        return None, None
    
    if not is_ebeam_folder(folder_path):
        print(f"Error: Not an e-beam folder")
        return None, None
    
    tree = ET.parse(results_path)
    root = tree.getroot()
    
    relative_output = None
    relative_uniformity = None
    
    # Find BeamProfileCheck element
    for elem in root.iter():
        if elem.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'BeamProfileCheck':
            for child in elem:
                tag = child.tag.split('}')[-1]
                if tag == 'RelativeOutput' and child.text:
                    relative_output = float(child.text.strip())
                elif tag == 'RelativeUniformity' and child.text:
                    relative_uniformity = float(child.text.strip())
            break
    
    if relative_output is None or relative_uniformity is None:
        return None, None
    
    # Calculate: (relative_output - 1) × 100 and relative_uniformity × 100
    output = (relative_output - 1) * 100
    uniformity = relative_uniformity * 100
    
    return output, uniformity


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ebeam_extractor.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output, uniformity = extract_ebeam_values(folder_path)
    
    if output is not None and uniformity is not None:
        print(f"Relative Output: {output:.2f}%")
        print(f"Relative Uniformity: {uniformity:.2f}%")
    else:
        print("Failed to extract values")
        sys.exit(1)
