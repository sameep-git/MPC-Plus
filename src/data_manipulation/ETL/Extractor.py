"""
Extractor Module
----------------
This module defines the `Extractor` class, responsible for reading and parsing
beam data from CSV files and populating model objects (EBeamModel, XBeamModel,
Geo6xfffModel) with corresponding numerical values.

Each extractor method is tailored to a specific beam type and calls the
appropriate model's setter methods based on CSV field names.

Supported beam models:
    - Electron beams: `EBeamModel`
    - X-ray beams: `XBeamModel`
    - Geometric beams: `Geo6xfffModel`
"""

import xml.etree.ElementTree as ET
import csv
import decimal
from decimal import Decimal
import math

class Extractor:
    """
    Handles data extraction from CSV files for various beam models.
    Each method corresponds to a specific model type and maps CSV entries
    to model attributes via setter methods.
    """

    # --- E-BEAM ---
    def eModelExtraction(self, eBeam):
        """
        Extract data for E-beam model from CSV file
        """
        try:
            # Get the path from the eBeam object
            path = eBeam.get_path()
            
            # Parse the CSV file
            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Read through the CSV rows
                for row in reader:
                    name = row.get('Name [Unit]', '').strip()
                    value = row.get(' Value', '')
                    # Check for relative output (BeamOutputChange)
                    if 'BeamOutputChange' in name:
                        try:
                            eBeam.set_relative_output(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            eBeam.set_relative_output(Decimal(-1))
                    
                    # Check for relative uniformity (BeamUniformityChange)
                    elif 'BeamUniformityChange' in name:
                        try:
                            eBeam.set_relative_uniformity(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            eBeam.set_relative_uniformity(Decimal(-1))
                
        except FileNotFoundError:
            print(f"CSV file not found: {path}")
        except csv.Error as e:
            print(f"Error parsing CSV file: {e}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    def testeModelExtraction(self, eBeam):
        """
        Test method for E-beam extraction.
        Prints relative uniformity and output values after parsing.        
        """
        try:
            # Get the path from the eBeam object
            path = eBeam.get_path()
            
            # Parse the CSV file
            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Read through the CSV rows
                for row in reader:
                    name = row.get('Name [Unit]', '').strip()
                    value = row.get(' Value', '')
                    # Check for relative output (BeamOutputChange)
                    if 'BeamOutputChange' in name:
                        try:
                            eBeam.set_relative_output(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            eBeam.set_relative_output(Decimal(-1))
                    
                    # Check for relative uniformity (BeamUniformityChange)
                    elif 'BeamUniformityChange' in name:
                        try:
                            eBeam.set_relative_uniformity(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            eBeam.set_relative_uniformity(Decimal(-1))
            # Print the values
            print(f"Relative Uniformity: {eBeam.get_relative_uniformity()}")
            print(f"Relative Output: {eBeam.get_relative_output()}")
                
        except FileNotFoundError:
            print(f"CSV file not found: {path}")
        except csv.Error as e:
            print(f"Error parsing CSV file: {e}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    # --- X-BEAM ---
    def xModelExtraction(self, xBeam):
        """
        Extract data for X-beam model from CVS file
        """
        try:
            # Get the path from the eBeam object
            path = xBeam.get_path()
            
            # Parse the CSV file
            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Read through the CSV rows
                for row in reader:
                    name = row.get('Name [Unit]', '').strip()
                    value = row.get(' Value', '')
                    
                    # Check for relative output (BeamOutputChange)
                    if 'BeamOutputChange' in name:
                        print(value)
                        try:
                            xBeam.set_relative_output(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            xBeam.set_relative_output(Decimal(-1))
                    
                    # Check for relative uniformity (BeamUniformityChange)
                    elif 'BeamUniformityChange' in name:
                        try:
                            xBeam.set_relative_uniformity(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            xBeam.set_relative_uniformity(Decimal(-1))

                    # Check for Center Shift (BeamCenterShift)
                    elif 'BeamCenterShift' in name:
                        try:
                            xBeam.set_center_shift(Decimal(value))
                        except (ValueError, TypeError, decimal.InvalidOperation):
                            xBeam.set_center_shift(Decimal(-1))
                
        except FileNotFoundError:
            print(f"CSV file not found: {path}")
        except csv.Error as e:
            print(f"Error parsing CSV file: {e}")
        except Exception as e:
            print(f"Error during extraction: {e}")


        
    
    def geoModelExtraction(self, geoModel):
        """
        Extract data for Geo6xfffModel from CSV file.
        Reads each row and calls the appropriate setter.
        """
        import csv
        from decimal import Decimal, InvalidOperation

        try:
            path = geoModel.get_path()

            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    name = row.get('Name [Unit]', '').strip()
                    value = row.get(' Value', '').strip()
                    if not name or not value:
                        continue
                    
                    # Convert value to Decimal
                    try:
                        dec_val = Decimal(value)
                    except (ValueError, TypeError, InvalidOperation):
                        dec_val = Decimal(-1)

                    # ---- IsoCenterGroup ----
                    if 'IsoCenterSize' in name:
                        geoModel.set_IsoCenterSize(dec_val)
                    elif 'IsoCenterMVOffset' in name:
                        geoModel.set_IsoCenterMVOffset(dec_val)
                    elif 'IsoCenterKVOffset' in name:
                        geoModel.set_IsoCenterKVOffset(dec_val)

                    # ---- BeamGroup ----
                    elif 'BeamOutputChange' in name:
                        geoModel.set_relative_output(dec_val)
                    elif 'BeamUniformityChange' in name:
                        geoModel.set_relative_uniformity(dec_val)
                    elif 'BeamCenterShift' in name:
                        geoModel.set_center_shift(dec_val)

                    # ---- CollimationGroup ----
                    elif 'CollimationRotationOffset' in name:
                        geoModel.set_CollimationRotationOffset(dec_val)

                    # ---- GantryGroup ----
                    elif 'GantryAbsolute' in name:
                        geoModel.set_GantryAbsolute(dec_val)
                    elif 'GantryRelative' in name:
                        geoModel.set_GantryRelative(dec_val)

                    # ---- EnhancedCouchGroup ----
                    elif 'CouchMaxPositionError' in name:
                        geoModel.set_CouchMaxPositionError(dec_val)
                    elif 'CouchLat' in name:
                        geoModel.set_CouchLat(dec_val)
                    elif 'CouchLng' in name:
                        geoModel.set_CouchLng(dec_val)
                    elif 'CouchVrt' in name:
                        geoModel.set_CouchVrt(dec_val)
                    elif 'CouchRtnFine' in name:
                        geoModel.set_CouchRtnFine(dec_val)
                    elif 'CouchRtnLarge' in name:
                        geoModel.set_CouchRtnLarge(dec_val)
                    elif 'RotationInducedCouchShiftFullRange' in name:
                        geoModel.set_RotationInducedCouchShiftFullRange(dec_val)

                    # ---- MLC Leaves ----
                    elif 'MLCLeavesA/MLCLeaf' in name:
                        try:
                            index = int(name.split('MLCLeaf')[1].split()[0])
                            geoModel.set_MLCLeafA(index, dec_val)
                        except Exception:
                            pass
                    elif 'MLCLeavesB/MLCLeaf' in name:
                        try:
                            index = int(name.split('MLCLeaf')[1].split()[0])
                            geoModel.set_MLCLeafB(index, dec_val)
                        except Exception:
                            pass

                    # ---- MLC Offsets ----
                    elif 'MaxOffsetA' in name:
                        geoModel.set_MaxOffsetA(dec_val)
                    elif 'MaxOffsetB' in name:
                        geoModel.set_MaxOffsetB(dec_val)
                    elif 'MeanOffsetA' in name:
                        geoModel.set_MeanOffsetA(dec_val)
                    elif 'MeanOffsetB' in name:
                        geoModel.set_MeanOffsetB(dec_val)

                    # ---- MLC Backlash ----
                    elif 'MLCBacklashLeavesA/MLCBacklashLeaf' in name:
                        try:
                            index = int(name.split('MLCBacklashLeaf')[1].split()[0])
                            geoModel.set_MLCBacklashA(index, dec_val)
                        except Exception:
                            pass
                    elif 'MLCBacklashLeavesB/MLCBacklashLeaf' in name:
                        try:
                            index = int(name.split('MLCBacklashLeaf')[1].split()[0])
                            geoModel.set_MLCBacklashB(index, dec_val)
                        except Exception:
                            pass
                    elif 'MLCBacklashMaxA' in name:
                        geoModel.set_MLCBacklashMaxA(dec_val)
                    elif 'MLCBacklashMaxB' in name:
                        geoModel.set_MLCBacklashMaxB(dec_val)
                    elif 'MLCBacklashMeanA' in name:
                        geoModel.set_MLCBacklashMeanA(dec_val)
                    elif 'MLCBacklashMeanB' in name:
                        geoModel.set_MLCBacklashMeanB(dec_val)

                    # ---- Jaws Group ----
                    elif 'JawX1' in name:
                        geoModel.set_JawX1(dec_val)
                    elif 'JawX2' in name:
                        geoModel.set_JawX2(dec_val)
                    elif 'JawY1' in name:
                        geoModel.set_JawY1(dec_val)
                    elif 'JawY2' in name:
                        geoModel.set_JawY2(dec_val)

                    # ---- Jaws Parallelism ----
                    elif 'JawParallelismX1' in name:
                        geoModel.set_JawParallelismX1(dec_val)
                    elif 'JawParallelismX2' in name:
                        geoModel.set_JawParallelismX2(dec_val)
                    elif 'JawParallelismY1' in name:
                        geoModel.set_JawParallelismY1(dec_val)
                    elif 'JawParallelismY2' in name:
                        geoModel.set_JawParallelismY2(dec_val)

        except FileNotFoundError:
            print(f"CSV file not found: {path}")
        except csv.Error as e:
            print(f"Error parsing CSV file: {e}")
        except Exception as e:
            print(f"Error during extraction: {e}")

    def testGeoModelExtraction(self, geoModel):
        """
        Test method for Geo model extraction.
        Runs geoModelExtraction() and prints all values using getters.
        """
        print("\n--- Starting Geo Model Extraction Test ---")
        self.geoModelExtraction(geoModel)
        print("--- Extraction Complete ---\n")

        try:
            # IsoCenterGroup
            print(f"IsoCenterSize: {geoModel.get_IsoCenterSize()}")
            print(f"IsoCenterMVOffset: {geoModel.get_IsoCenterMVOffset()}")
            print(f"IsoCenterKVOffset: {geoModel.get_IsoCenterKVOffset()}")

            # BeamGroup
            print(f"BeamOutputChange: {geoModel.get_relative_output()}")
            print(f"BeamUniformityChange: {geoModel.get_relative_uniformity()}")
            print(f"BeamCenterShift: {geoModel._relative_uniformity()}")

            # CollimationGroup
            print(f"CollimationRotationOffset: {geoModel.get_CollimationRotationOffset()}")

            # GantryGroup
            print(f"GantryAbsolute: {geoModel.get_GantryAbsolute()}")
            print(f"GantryRelative: {geoModel.get_GantryRelative()}")

            # EnhancedCouchGroup
            print(f"CouchMaxPositionError: {geoModel.get_CouchMaxPositionError()}")
            print(f"CouchLat: {geoModel.get_CouchLat()}")
            print(f"CouchLng: {geoModel.get_CouchLng()}")
            print(f"CouchVrt: {geoModel.get_CouchVrt()}")
            print(f"CouchRtnFine: {geoModel.get_CouchRtnFine()}")
            print(f"CouchRtnLarge: {geoModel.get_CouchRtnLarge()}")
            print(f"RotationInducedCouchShiftFullRange: {geoModel.get_RotationInducedCouchShiftFullRange()}")

            # MLC Groups
            print(f"MaxOffsetA: {geoModel.get_MaxOffsetA()}")
            print(f"MaxOffsetB: {geoModel.get_MaxOffsetB()}")
            print(f"MeanOffsetA: {geoModel.get_MeanOffsetA()}")
            print(f"MeanOffsetB: {geoModel.get_MeanOffsetB()}")
            print(f"MLCBacklashMaxA: {geoModel.get_MLCBacklashMaxA()}")
            print(f"MLCBacklashMaxB: {geoModel.get_MLCBacklashMaxB()}")
            print(f"MLCBacklashMeanA: {geoModel.get_MLCBacklashMeanA()}")
            print(f"MLCBacklashMeanB: {geoModel.get_MLCBacklashMeanB()}")

            # Individual MLC leaf/backlash arrays (if implemented)
            if hasattr(geoModel, "get_MLCLeafA"):
                print(f"MLCLeafA: {geoModel.get_MLCLeafA()}")
            if hasattr(geoModel, "get_MLCLeafB"):
                print(f"MLCLeafB: {geoModel.get_MLCLeafB()}")
            if hasattr(geoModel, "get_MLCBacklashA"):
                print(f"MLCBacklashA: {geoModel.get_MLCBacklashA()}")
            if hasattr(geoModel, "get_MLCBacklashB"):
                print(f"MLCBacklashB: {geoModel.get_MLCBacklashB()}")

            # Jaw Group
            print(f"JawX1: {geoModel.get_JawX1()}")
            print(f"JawX2: {geoModel.get_JawX2()}")
            print(f"JawY1: {geoModel.get_JawY1()}")
            print(f"JawY2: {geoModel.get_JawY2()}")

            # Jaw Parallelism
            print(f"JawParallelismX1: {geoModel.get_JawParallelismX1()}")
            print(f"JawParallelismX2: {geoModel.get_JawParallelismX2()}")
            print(f"JawParallelismY1: {geoModel.get_JawParallelismY1()}")
            print(f"JawParallelismY2: {geoModel.get_JawParallelismY2()}")

        except Exception as e:
            print(f"Error printing Geo model data: {e}")

        print("\n--- End of Geo Model Test ---\n")

