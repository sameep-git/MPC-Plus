import xml.etree.ElementTree as ET
from decimal import Decimal
import math

class Extractor:
    
    def eModelExtraction(self, eBeam):
        """
        Extract data for E-beam model from XML file
        """
        try:
            # Get the path from the eBeam object
            path = eBeam.get_path()
            
            # Parse the XML file
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Find RelativeUniformity and RelativeOutput values
            relative_uniformity = None
            relative_output = None
            
            # Search for the tags in the XML
            for elem in root.iter():
                # Strip namespace if present
                elem.tag = elem.tag.split('}')[-1]  # This gives 'RelativeUniformity' or 'RelativeOutput'
                if elem.tag == 'RelativeUniformity':
                    #eBeam.set_relative_uniformity = elem.text
                    try:
                        eBeam.set_relative_uniformity(Decimal(elem.text) * 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        eBeam.set_relative_uniformity(-1)
                elif elem.tag == 'RelativeOutput':
                    #eBeam.set_relative_output = elem.text
                    try:
                        eBeam.set_relative_output((Decimal(elem.text) -1)* 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        eBeam.set_relative_output(-1)
            
                
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"XML file not found: {path}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    def testeModelExtraction(self, eBeam):
        """
        Test method to print relative uniformity and relative output values
        """
        try:
            # Get the path from the eBeam object
            path = eBeam.get_path()
            
            # Parse the XML file
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Find RelativeUniformity and RelativeOutput values
            relative_uniformity = None
            relative_output = None
            
            # Search for the tags in the XML
            for elem in root.iter():
                # Strip namespace if present
                elem.tag = elem.tag.split('}')[-1]  # This gives 'RelativeUniformity' or 'RelativeOutput'
                if elem.tag == 'RelativeUniformity':
                    #eBeam.set_relative_uniformity = elem.text
                    try:
                        eBeam.set_relative_uniformity(Decimal(elem.text) * 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        eBeam.set_relative_uniformity(-1)
                elif elem.tag == 'RelativeOutput':
                    #eBeam.set_relative_output = elem.text
                    try:
                        eBeam.set_relative_output((Decimal(elem.text) - 1)* 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        eBeam.set_relative_output(-1)
            
            # print("Root tag:", root.tag)
            # for elem in root.iter():
            #     print("Found tag:", elem.tag)
            
            # Print the values
            print(f"Relative Uniformity: {eBeam.get_relative_uniformity()}")
            print(f"Relative Output: {eBeam.get_relative_output()}")
                
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"XML file not found: {path}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    
    def xModelExtraction(self, xBeam):
        """
        Extract data for X-beam model from XML file
        """
        try:
            # Get the path from the eBeam object
            path = xBeam.get_path()
            
            # Parse the XML file
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Local variables for calculations
            relative_output = Decimal(-1)
            baseline_x = baseline_y = Decimal(-1)
            center_x = center_y = Decimal(-1)
            iso_x = iso_y = Decimal(-1)
                
            # Search for the tags in the XML
            for elem in root.iter():
                # Strip namespace if present
                elem.tag = elem.tag.split('}')[-1]  # This gives 'RelativeUniformity' or 'RelativeOutput'
                if elem.tag == 'RelativeUniformity':
                    #xBeam.set_relative_uniformity = elem.text
                    try:
                        xBeam.set_relative_uniformity(Decimal(elem.text) * 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        xBeam.set_relative_uniformity(-1)
                elif elem.tag == 'RelativeOutput':
                    #xBeam.set_relative_output = elem.text
                    try:
                        xBeam.set_relative_output((Decimal(elem.text) -1)* 100)
                    except (ValueError, TypeError, decimal.InvalidOperation):
                        xBeam.set_relative_output(-1)
                    # Extract X/Y values from BaselineIsoCenter, IsoCenter

                # Extract X/Y values from BaselineIsoCenter, IsoCenter
                elif elem.tag in ['BaselineIsoCenter', 'IsoCenter']:
                    x_val = y_val = Decimal(-1)
                    for child in elem:  # iterate over X and Y
                        child_tag = child.tag.split('}')[-1]
                        try:
                            if child_tag == 'X':
                                x_val = Decimal(child.text)
                            elif child_tag == 'Y':
                                y_val = Decimal(child.text)
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            x_val = y_val = Decimal(-1)

                    # Store locally for calculations
                    if elem.tag == 'BaselineIsoCenter':
                        baseline_x, baseline_y = x_val, y_val
                    elif elem.tag == 'IsoCenter':
                        iso_x, iso_y = x_val, y_val

            #Calculations for Beam Center Shift
            deltaX = iso_x - baseline_x
            deltaY = iso_y - baseline_y
            #Euclidean Distance (cm)
            shift = (deltaX**2 + deltaY**2).sqrt()
            #Convert to cm
            xBeam.set_center_shift(shift * 10)

                
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"XML file not found: {path}")
        except Exception as e:
            print(f"Error during extraction: {e}")


        
    
    def geoModelExtraction(self, geoBeam):
        """
        Extract data for Geo6xfff model
        """
        # TODO: Implement Geo6xfff data extraction logic
        pass
