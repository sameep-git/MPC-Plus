"""
Extract relative uniformity, relative output, and center shift from x-beam Results.xml
"""

import os
import sys
import xml.etree.ElementTree as ET
import math


def is_xbeam_folder(folder_path):
    """Check if folder is an x-beam folder"""
    folder_name = os.path.basename(folder_path)
    return '15x' in folder_name or '6x' in folder_name or 'BeamCheckTemplate' in folder_name


def extract_xbeam_values(folder_path):
    """Extract relative output, relative uniformity, and center shift from Results.xml"""
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
            return None, None, None
    
    results_path = os.path.join(folder_path, "Results.xml")
    
    if not os.path.exists(results_path):
        print(f"Error: Results.xml not found in {folder_path}")
        return None, None, None
    
    if not is_xbeam_folder(folder_path):
        print(f"Error: Not an x-beam folder")
        return None, None, None
    
    tree = ET.parse(results_path)
    root = tree.getroot()
    
    relative_output = None
    relative_uniformity = None
    center_shift = None
    
    # Find BeamProfileCheck element for relative output and relative uniformity
    for elem in root.iter():
        if elem.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'BeamProfileCheck':
            for child in elem:
                tag = child.tag.split('}')[-1]
                if tag == 'RelativeOutput' and child.text:
                    relative_output = float(child.text.strip())
                elif tag == 'RelativeUniformity' and child.text:
                    relative_uniformity = float(child.text.strip())
            break
    
    # Find JawEdgeCheck element for IsoCenter and BaselineIsoCenter
    iso_x = None
    iso_y = None
    baseline_iso_x = None
    baseline_iso_y = None
    
    for elem in root.iter():
        if elem.get('{http://www.w3.org/2001/XMLSchema-instance}type') == 'JawEdgeCheck':
            for child in elem:
                tag = child.tag.split('}')[-1]
                if tag == 'IsoCenter':
                    for coord in child:
                        coord_tag = coord.tag.split('}')[-1]
                        if coord_tag == 'X' and coord.text:
                            iso_x = float(coord.text.strip())
                        elif coord_tag == 'Y' and coord.text:
                            iso_y = float(coord.text.strip())
                elif tag == 'BaselineIsoCenter':
                    for coord in child:
                        coord_tag = coord.tag.split('}')[-1]
                        if coord_tag == 'X' and coord.text:
                            baseline_iso_x = float(coord.text.strip())
                        elif coord_tag == 'Y' and coord.text:
                            baseline_iso_y = float(coord.text.strip())
            break
    
    # Calculate center shift using formula: √(X – X₀)² + (Y – Y₀)² × 10
    if iso_x is not None and iso_y is not None and baseline_iso_x is not None and baseline_iso_y is not None:
        dx = iso_x - baseline_iso_x
        dy = iso_y - baseline_iso_y
        center_shift = math.sqrt(dx * dx + dy * dy) * 10
    
    if relative_output is None or relative_uniformity is None:
        return None, None, None
    
    # Calculate: (relative_output - 1) × 100 and relative_uniformity × 100
    output = (relative_output - 1) * 100
    uniformity = relative_uniformity * 100
    
    return output, uniformity, center_shift


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: xbeam_extractor.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output, uniformity, center_shift = extract_xbeam_values(folder_path)
    
    if output is not None and uniformity is not None:
        print(f"Relative Output: {output:.2f}%")
        print(f"Relative Uniformity: {uniformity:.2f}%")
        if center_shift is not None:
            print(f"Center Shift: {center_shift:.6f} mm")
        else:
            print("Center Shift: Not found")
    else:
        print("Failed to extract values")
        sys.exit(1)
