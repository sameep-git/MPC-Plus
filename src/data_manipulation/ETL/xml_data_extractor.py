"""
Results.xml:
    - BeamProfileCheck (i:type="BeamProfileCheck"):
        * RelativeOutput -> set_relative_output()
        * RelativeUniformity -> set_relative_uniformity()
        * BeamCenterShift -> set_center_shift() (X-Beam and Geo only)
    
    - CouchReference:
        * CouchLat -> set_CouchLat() (Geo only)
        * CouchLng -> set_CouchLng() (Geo only)
        * CouchVrt -> set_CouchVrt() (Geo only)
        * CouchRtn -> set_CouchRtnFine() or set_CouchRtnLarge() (Geo only)

SetBeam-*.xml (e.g., SetBeam-6e.xml, SetBeam-6x.xml):
    - ControlPoints -> Cp[WorkObjectID="Linac"]:
        * GantryRtn -> set_GantryAbsolute() (Geo only)
        * CollRtn -> set_CollimationRotationOffset() (Geo only)
        * X1 -> set_JawX1() (Geo only)
        * X2 -> set_JawX2() (Geo only)
        * Y1 -> set_JawY1() (Geo only)
        * Y2 -> set_JawY2() (Geo only)
        * Mlc -> A (60 space-separated values) -> set_MLCLeafA(index, value) (Geo only)
        * Mlc -> B (60 space-separated values) -> set_MLCLeafB(index, value) (Geo only)

NOTES:
    - Many Geo model fields (IsoCenterSize, MLC offsets, backlash, jaw parallelism, etc.)
      are not currently present in the XML files
"""

import os
import logging
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

# Set up logger for this module
logger = logging.getLogger(__name__)

class xml_data_extractor:
    """
    Handles data extraction from XML files for various beam models.
    Each method corresponds to a specific model type and maps XML elements
    to model attributes via setter methods.
    """

    def extract(self, model):
        """
        Automatically calls the correct extraction method
        based on the type of model object passed in.

        Supported models:
            - EBeamModel
            - XBeamModel
            - Geo6xfffModel
        """
        model_type = type(model).__name__.lower()

        if "ebeam" in model_type:
            return self.eModelExtraction(model)
        elif "xbeam" in model_type:
            return self.xModelExtraction(model)
        elif "geo" in model_type:
            return self.geoModelExtraction(model)
        else:
            raise TypeError(f"Unsupported model type: {type(model).__name__}")

    def extractTest(self, model):
        """
        Automatically calls the correct extraction method
        based on the type of model object passed in.

        Supported models:
            - EBeamModel
            - XBeamModel
            - Geo6xfffModel
        """
        model_type = type(model).__name__.lower()

        if "ebeam" in model_type:
            return self.testeModelExtraction(model)
        elif "xbeam" in model_type:
            return self.testxModelExtraction(model)
        elif "geo" in model_type:
            return self.testGeoModelExtraction(model)
        else:
            raise TypeError(f"Unsupported model type: {type(model).__name__}")

    def _parse_xml_value(self, element, default=Decimal(-1)):
        """
        Helper method to parse XML element text to Decimal.
        Returns default value if parsing fails or element is None.
        """
        if element is None or element.text is None:
            return default
        
        try:
            return Decimal(element.text.strip())
        except (ValueError, TypeError, InvalidOperation):
            return default

    def _find_element(self, root, tag, namespaces=None):
        """
        Helper method to find element by tag, handling namespaces.
        """
        if namespaces:
            for prefix, uri in namespaces.items():
                tag_with_ns = f"{{{uri}}}{tag}"
                element = root.find(tag_with_ns)
                if element is not None:
                    return element
        
        # Try without namespace
        return root.find(tag)

    def _find_all_elements(self, root, tag, namespaces=None):
        """
        Helper method to find all elements by tag, handling namespaces.
        """
        if namespaces:
            for prefix, uri in namespaces.items():
                tag_with_ns = f"{{{uri}}}{tag}"
                elements = root.findall(tag_with_ns)
                if elements:
                    return elements
        
        # Try without namespace
        return root.findall(tag)
    
    def _find_elements_by_type(self, root, type_name, namespaces=None):
        """
        Helper method to find elements with a specific i:type attribute.
        """
        elements = []
        # Look for type attribute with or without namespace
        type_attrs = ['{http://www.w3.org/2001/XMLSchema-instance}type', 'type']
        
        for elem in root.iter():
            for attr in type_attrs:
                if elem.get(attr) == type_name:
                    elements.append(elem)
                    break
        
        return elements
    
    def _find_in_default_ns(self, parent, tag_name, default_ns='http:/www.varian.com/MPC'):
        """
        Helper to find elements in the default namespace.
        """
        # Try with namespace
        ns_tag = f"{{{default_ns}}}{tag_name}"
        elem = parent.find(ns_tag)
        if elem is not None:
            return elem
        
        # Try without namespace (in case namespace handling fails)
        for child in parent.iter():
            # Check if tag ends with the tag name (handles namespaced tags)
            if child.tag.endswith(tag_name) or child.tag == tag_name:
                return child
        
        return None

    # --- E-BEAM ---
    def eModelExtraction(self, eBeam):
        """
        Extract data for E-beam model from XML files
        
        Data Sources:
        - Results.xml: Contains beam profile check results
        """
        try:
            # Get the folder path and construct the XML file paths
            folder_path = eBeam.get_path()
            results_path = os.path.join(folder_path, "Results.xml")
            
            if not os.path.exists(results_path):
                logger.error(f"XML file not found: {results_path}")
                return

            # Parse Results.xml
            # File structure: <ProcessingSteps><CompletedSteps><d2p1:anyType i:type="BeamProfileCheck">...</d2p1:anyType></CompletedSteps></ProcessingSteps>
            tree = ET.parse(results_path)
            root = tree.getroot()
            
            # Define namespaces - note: default namespace has typo (missing slash)
            namespaces = {
                'mpc': 'http:/www.varian.com/MPC',  # Note: actual namespace in XML has typo
                'i': 'http://www.w3.org/2001/XMLSchema-instance',
                'd2p1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
            }
            
            # Register namespaces for cleaner XPath queries
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            # Find BeamProfileCheck elements by i:type attribute
            # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"]
            beam_profile_checks = self._find_elements_by_type(root, 'BeamProfileCheck', namespaces)
            
            for check_elem in beam_profile_checks:
                # Extract beam profile data from BeamProfileCheck element
                # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"] -> RelativeOutput
                # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"] -> RelativeUniformity
                for child in check_elem:
                    tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    
                    if tag_name == 'RelativeOutput':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeOutput
                        # Maps to: eBeam.set_relative_output()
                        dec_val = self._parse_xml_value(child)
                        eBeam.set_relative_output(dec_val)
                    elif tag_name == 'RelativeUniformity':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeUniformity
                        # Maps to: eBeam.set_relative_uniformity()
                        dec_val = self._parse_xml_value(child)
                        eBeam.set_relative_uniformity(dec_val)
                
        except FileNotFoundError:
            logger.error(f"XML file not found: {results_path}")
        except ET.ParseError as e:
            logger.error(f"Error parsing XML file: {e}")
        except Exception as e:
            logger.error(f"Error during extraction: {e}", exc_info=True)

    def testeModelExtraction(self, eBeam):
        """
        Test method for E model extraction.
        Runs eModelExtraction() and prints all values using getters.
        """
        self.eModelExtraction(eBeam)
        print(f"E-Beam Model - Relative Output: {eBeam.get_relative_output()}")
        print(f"E-Beam Model - Relative Uniformity: {eBeam.get_relative_uniformity()}")

    # --- X-BEAM ---
    def xModelExtraction(self, xBeam):
        """
        Extract data for X-beam model from XML files
        
        Data Sources:
        - Results.xml: Contains beam profile check results including center shift
        """
        try:
            # Get the folder path and construct the XML file paths
            folder_path = xBeam.get_path()
            results_path = os.path.join(folder_path, "Results.xml")
            
            if not os.path.exists(results_path):
                logger.error(f"XML file not found: {results_path}")
                return

            # Parse Results.xml
            # File structure: <ProcessingSteps><CompletedSteps><d2p1:anyType i:type="BeamProfileCheck">...</d2p1:anyType></CompletedSteps></ProcessingSteps>
            tree = ET.parse(results_path)
            root = tree.getroot()
            
            # Define namespaces - note: default namespace has typo (missing slash)
            namespaces = {
                'mpc': 'http:/www.varian.com/MPC',  # Note: actual namespace in XML has typo
                'i': 'http://www.w3.org/2001/XMLSchema-instance',
                'd2p1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'
            }
            
            # Register namespaces for cleaner XPath queries
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            # Find BeamProfileCheck elements by i:type attribute
            # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"]
            beam_profile_checks = self._find_elements_by_type(root, 'BeamProfileCheck', namespaces)
            
            for check_elem in beam_profile_checks:
                # Extract beam profile data from BeamProfileCheck element
                # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"] -> RelativeOutput
                # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"] -> RelativeUniformity
                # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"] -> BeamCenterShift
                for child in check_elem:
                    tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    
                    if tag_name == 'RelativeOutput':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeOutput
                        # Maps to: xBeam.set_relative_output()
                        dec_val = self._parse_xml_value(child)
                        xBeam.set_relative_output(dec_val)
                    elif tag_name == 'RelativeUniformity':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeUniformity
                        # Maps to: xBeam.set_relative_uniformity()
                        dec_val = self._parse_xml_value(child)
                        xBeam.set_relative_uniformity(dec_val)
                    elif tag_name == 'BeamCenterShift':
                        # Source: Results.xml -> BeamProfileCheck -> BeamCenterShift
                        # Maps to: xBeam.set_center_shift()
                        dec_val = self._parse_xml_value(child)
                        xBeam.set_center_shift(dec_val)
                
        except FileNotFoundError:
            logger.error(f"XML file not found: {results_path}")
        except ET.ParseError as e:
            logger.error(f"Error parsing XML file: {e}")
        except Exception as e:
            logger.error(f"Error during extraction: {e}", exc_info=True)

    def testxModelExtraction(self, xBeam):
        """
        Test method for X model extraction.
        Runs xModelExtraction() and prints all values using getters.
        """
        self.xModelExtraction(xBeam)
        print(f"X-Beam Model - Relative Output: {xBeam.get_relative_output()}")
        print(f"X-Beam Model - Relative Uniformity: {xBeam.get_relative_uniformity()}")
        print(f"X-Beam Model - Center Shift: {xBeam.get_center_shift()}")

    # --- GEO MODEL ---
    def geoModelExtraction(self, geoModel):
        """
        Extract data for Geo6xfffModel from XML files.
        Reads from Results.xml and SetBeam-*.xml files.
        
        Data Sources:
        - Results.xml: Contains beam profile check results and couch reference data
        - SetBeam-*.xml: Contains control point data with gantry, collimation, jaws, and MLC positions
        """
        try:
            # Get the folder path and construct the XML file paths
            folder_path = geoModel.get_path()
            results_path = os.path.join(folder_path, "Results.xml")
            
            # Find SetBeam XML file (could be SetBeam-6e.xml, SetBeam-6x.xml, etc.)
            setbeam_files = [f for f in os.listdir(folder_path) if f.startswith('SetBeam') and f.endswith('.xml')]
            
            if not os.path.exists(results_path):
                logger.error(f"Results.xml file not found: {results_path}")
                return

            # Parse Results.xml
            # File structure: <ProcessingSteps><CompletedSteps>...</CompletedSteps><CouchReference>...</CouchReference></ProcessingSteps>
            tree = ET.parse(results_path)
            root = tree.getroot()
            
            # Define namespaces - note: default namespace has typo (missing slash)
            namespaces = {
                'mpc': 'http:/www.varian.com/MPC',  # Note: actual namespace in XML has typo
                'i': 'http://www.w3.org/2001/XMLSchema-instance',
                'd2p1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays',
                'd2p2': 'http://schemas.datacontract.org/2004/07/VMS.CA.Base.Common.Calc6DoF'
            }
            
            # Register namespaces for cleaner XPath queries
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            # ========== Extract from Results.xml ==========
            
            # ---- BeamGroup - RelativeOutput, RelativeUniformity, BeamCenterShift ----
            # XML Location: Results.xml -> ProcessingSteps -> CompletedSteps -> d2p1:anyType[@i:type="BeamProfileCheck"]
            beam_profile_checks = self._find_elements_by_type(root, 'BeamProfileCheck', namespaces)
            
            for check_elem in beam_profile_checks:
                for child in check_elem:
                    tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    
                    if tag_name == 'RelativeOutput':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeOutput
                        # Maps to: geoModel.set_relative_output()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_relative_output(dec_val)
                    elif tag_name == 'RelativeUniformity':
                        # Source: Results.xml -> BeamProfileCheck -> RelativeUniformity
                        # Maps to: geoModel.set_relative_uniformity()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_relative_uniformity(dec_val)
                    elif tag_name == 'BeamCenterShift':
                        # Source: Results.xml -> BeamProfileCheck -> BeamCenterShift
                        # Maps to: geoModel.set_center_shift()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_center_shift(dec_val)
            
            # ---- EnhancedCouchGroup - CouchReference ----
            # XML Location: Results.xml -> ProcessingSteps -> CouchReference
            # Search for CouchReference element by tag name (handling namespaces)
            couch_ref = None
            for elem in root.iter():
                tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if tag_name == 'CouchReference':
                    couch_ref = elem
                    break
            
            if couch_ref is not None:
                for child in couch_ref:
                    tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    
                    if tag_name == 'CouchLat':
                        # Source: Results.xml -> CouchReference -> CouchLat
                        # Maps to: geoModel.set_CouchLat()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_CouchLat(dec_val)
                    elif tag_name == 'CouchLng':
                        # Source: Results.xml -> CouchReference -> CouchLng
                        # Maps to: geoModel.set_CouchLng()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_CouchLng(dec_val)
                    elif tag_name == 'CouchVrt':
                        # Source: Results.xml -> CouchReference -> CouchVrt
                        # Maps to: geoModel.set_CouchVrt()
                        dec_val = self._parse_xml_value(child)
                        geoModel.set_CouchVrt(dec_val)
                    elif tag_name == 'CouchRtn':
                        # Source: Results.xml -> CouchReference -> CouchRtn
                        # Maps to: geoModel.set_CouchRtnFine() or geoModel.set_CouchRtnLarge()
                        # Determine if it's fine or large rotation (typically fine if < 360)
                        dec_val = self._parse_xml_value(child)
                        if abs(dec_val) < 360:
                            geoModel.set_CouchRtnFine(dec_val)
                        else:
                            geoModel.set_CouchRtnLarge(dec_val)
            
            # ========== Extract from SetBeam XML file ==========
            # File structure: <SetBeam><ControlPoints><Cp><WorkObjectID>Linac</WorkObjectID>...</Cp></ControlPoints></SetBeam>
            if setbeam_files:
                setbeam_path = os.path.join(folder_path, setbeam_files[0])
                try:
                    setbeam_tree = ET.parse(setbeam_path)
                    setbeam_root = setbeam_tree.getroot()
                    
                    # Find ControlPoints
                    # XML Location: SetBeam-*.xml -> SetBeam -> ControlPoints
                    control_points = setbeam_root.find('ControlPoints')
                    if control_points is not None:
                        # Get the first Cp with WorkObjectID="Linac" (main control point)
                        # XML Location: SetBeam-*.xml -> SetBeam -> ControlPoints -> Cp[WorkObjectID="Linac"]
                        for cp in control_points.findall('Cp'):
                            work_object = cp.find('WorkObjectID')
                            if work_object is not None and work_object.text == 'Linac':
                                
                                # ---- GantryGroup ----
                                # Extract Gantry rotation
                                # XML Location: SetBeam-*.xml -> ControlPoints -> Cp -> GantryRtn
                                gantry_rtn = cp.find('GantryRtn')
                                if gantry_rtn is not None:
                                    # Source: SetBeam-*.xml -> Cp -> GantryRtn
                                    # Maps to: geoModel.set_GantryAbsolute()
                                    dec_val = self._parse_xml_value(gantry_rtn)
                                    geoModel.set_GantryAbsolute(dec_val)
                                
                                # ---- CollimationGroup ----
                                # Extract Collimation rotation
                                # XML Location: SetBeam-*.xml -> ControlPoints -> Cp -> CollRtn
                                coll_rtn = cp.find('CollRtn')
                                if coll_rtn is not None:
                                    # Source: SetBeam-*.xml -> Cp -> CollRtn
                                    # Maps to: geoModel.set_CollimationRotationOffset()
                                    dec_val = self._parse_xml_value(coll_rtn)
                                    geoModel.set_CollimationRotationOffset(dec_val)
                                
                                # ---- JawsGroup ----
                                # Extract Jaw positions
                                # XML Location: SetBeam-*.xml -> ControlPoints -> Cp -> X1, X2, Y1, Y2
                                jaw_x1 = cp.find('X1')
                                jaw_x2 = cp.find('X2')
                                jaw_y1 = cp.find('Y1')
                                jaw_y2 = cp.find('Y2')
                                
                                if jaw_x1 is not None:
                                    # Source: SetBeam-*.xml -> Cp -> X1
                                    # Maps to: geoModel.set_JawX1()
                                    dec_val = self._parse_xml_value(jaw_x1)
                                    geoModel.set_JawX1(dec_val)
                                
                                if jaw_x2 is not None:
                                    # Source: SetBeam-*.xml -> Cp -> X2
                                    # Maps to: geoModel.set_JawX2()
                                    dec_val = self._parse_xml_value(jaw_x2)
                                    geoModel.set_JawX2(dec_val)
                                
                                if jaw_y1 is not None:
                                    # Source: SetBeam-*.xml -> Cp -> Y1
                                    # Maps to: geoModel.set_JawY1()
                                    dec_val = self._parse_xml_value(jaw_y1)
                                    geoModel.set_JawY1(dec_val)
                                
                                if jaw_y2 is not None:
                                    # Source: SetBeam-*.xml -> Cp -> Y2
                                    # Maps to: geoModel.set_JawY2()
                                    dec_val = self._parse_xml_value(jaw_y2)
                                    geoModel.set_JawY2(dec_val)
                                
                                # ---- MLC Leaves ----
                                # Extract MLC positions
                                # XML Location: SetBeam-*.xml -> ControlPoints -> Cp -> Mlc -> A (space-separated values for 60 leaves)
                                # XML Location: SetBeam-*.xml -> ControlPoints -> Cp -> Mlc -> B (space-separated values for 60 leaves)
                                mlc = cp.find('Mlc')
                                if mlc is not None:
                                    mlc_a = mlc.find('A')
                                    mlc_b = mlc.find('B')
                                    
                                    if mlc_a is not None and mlc_a.text:
                                        # Source: SetBeam-*.xml -> Cp -> Mlc -> A (contains 60 space-separated values)
                                        # Maps to: geoModel.set_MLCLeafA(index, value) for indices 1-60
                                        # Parse space-separated values for 60 leaves
                                        leaf_values = mlc_a.text.strip().split()
                                        for idx, val_str in enumerate(leaf_values[:60], start=1):
                                            try:
                                                dec_val = Decimal(val_str)
                                                geoModel.set_MLCLeafA(idx, dec_val)
                                            except (ValueError, InvalidOperation):
                                                pass
                                    
                                    if mlc_b is not None and mlc_b.text:
                                        # Source: SetBeam-*.xml -> Cp -> Mlc -> B (contains 60 space-separated values)
                                        # Maps to: geoModel.set_MLCLeafB(index, value) for indices 1-60
                                        # Parse space-separated values for 60 leaves
                                        leaf_values = mlc_b.text.strip().split()
                                        for idx, val_str in enumerate(leaf_values[:60], start=1):
                                            try:
                                                dec_val = Decimal(val_str)
                                                geoModel.set_MLCLeafB(idx, dec_val)
                                            except (ValueError, InvalidOperation):
                                                pass
                                
                                break  # Only process first matching control point
                
                except ET.ParseError as e:
                    logger.error(f"Error parsing SetBeam XML file: {e}")
                except Exception as e:
                    logger.error(f"Error processing SetBeam XML: {e}", exc_info=True)
            
            # Note: Many fields like IsoCenterSize, MLC offsets, backlash, etc.
            # may not be present in the XML files provided. They would need to be
            # extracted from additional XML structures if available.
                
        except FileNotFoundError:
            logger.error(f"XML file not found: {results_path}")
        except ET.ParseError as e:
            logger.error(f"Error parsing XML file: {e}")
        except Exception as e:
            logger.error(f"Error during extraction: {e}", exc_info=True)

    def testGeoModelExtraction(self, geoModel):
        """
        Test method for Geo model extraction.
        Runs geoModelExtraction() and prints all values using getters.
        """
        self.geoModelExtraction(geoModel)
        print(f"Geo Model - Relative Output: {geoModel.get_relative_output()}")
        print(f"Geo Model - Relative Uniformity: {geoModel.get_relative_uniformity()}")
        print(f"Geo Model - Center Shift: {geoModel.get_center_shift()}")
        print(f"Geo Model - Couch Lat: {geoModel.get_CouchLat()}")
        print(f"Geo Model - Couch Lng: {geoModel.get_CouchLng()}")
        print(f"Geo Model - Couch Vrt: {geoModel.get_CouchVrt()}")
        print(f"Geo Model - Gantry Absolute: {geoModel.get_GantryAbsolute()}")
        print(f"Geo Model - Collimation Rotation Offset: {geoModel.get_CollimationRotationOffset()}")
        print(f"Geo Model - Jaw X1: {geoModel.get_JawX1()}, X2: {geoModel.get_JawX2()}")
        print(f"Geo Model - Jaw Y1: {geoModel.get_JawY1()}, Y2: {geoModel.get_JawY2()}")
