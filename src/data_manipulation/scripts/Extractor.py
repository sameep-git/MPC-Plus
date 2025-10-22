import xml.etree.ElementTree as ET

class Extractor:
    
    def eModelExtraction(self, eBeam):
        """
        Extract data for E-beam model from XML file
        """
        try:
            # Get the path from the eBeam object
            path = eBeam.getPath()
            
            # Parse the XML file
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Find RelativeUniformity and RelativeOutput values
            relative_uniformity = None
            relative_output = None
            
            # Search for the tags in the XML
            for elem in root.iter():
                if elem.tag == 'RelativeUniformity':
                    relative_uniformity = elem.text
                elif elem.tag == 'RelativeOutput':
                    relative_output = elem.text
            
            # Set the values using the eBeam setters
            if relative_uniformity is not None:
                eBeam.set_relative_uniformity(relative_uniformity)
            
            if relative_output is not None:
                eBeam.set_relative_out(relative_output)
                
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
            path = eBeam.getPath()
            
            # Parse the XML file
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Find RelativeUniformity and RelativeOutput values
            relative_uniformity = None
            relative_output = None
            
            # Search for the tags in the XML
            for elem in root.iter():
                if elem.tag == 'RelativeUniformity':
                    relative_uniformity = elem.text
                elif elem.tag == 'RelativeOutput':
                    relative_output = elem.text
            
            # Print the values
            print(f"Relative Uniformity: {relative_uniformity}")
            print(f"Relative Output: {relative_output}")
                
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"XML file not found: {path}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    
    def xModelExtraction(self, xBeam):
        """
        Extract data for X-beam model
        """
        # TODO: Implement X-beam data extraction logic
        pass
    
    def geoModelExtraction(self, geoBeam):
        """
        Extract data for Geo6xfff model
        """
        # TODO: Implement Geo6xfff data extraction logic
        pass
