"""
Overview: 
    This script serves as a simple driver to invoke the DataProcessor on 
    a single dataset directory. It is primarily intended for local testing, 
    validation, or debugging of the data extraction pipeline.

Usage:
    1) Update the `path` variable below to point to a directory containing 
       beam test results (a Results.csv file is expected inside).
    2) Run this script directly to process that dataset.
""" 
from .DataProcessor import DataProcessor

def main():
    # path = r"C:\Users\Bonny Brae\Desktop\MPC-Plus\data\csv_data\NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    path = r"data\csv_data\NDS-WKS-SN6543-2025-09-19-07-41-49-0008-GeometryCheckTemplate6xMVkVEnhancedCouch"
    dp = DataProcessor(path)
    dp.Run()

if __name__ == "__main__":
    main()
