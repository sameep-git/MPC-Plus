import xml.etree.ElementTree as ET
import csv
import decimal
from decimal import Decimal
import math

class Extractor:
    
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
        Test method to print relative uniformity and relative output values from CSV
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


        
    
    def geoModelExtraction(self, geoBeam):
        """
        Extract data for Geo6xfff model
        """
        # TODO: Implement Geo6xfff data extraction logic
        pass
