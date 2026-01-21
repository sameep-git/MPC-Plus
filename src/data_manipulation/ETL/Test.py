"""
Overview: 
    This script serves as a simple driver to invoke the DataProcessor on 
    a single dataset directory. It is primarily intended for local testing, 
    validation, or debugging of the data extraction pipeline.

Usage:
    1) Update the `path` variable below to point to a directory containing 
       beam test results (a Results.csv file is expected inside).
    2) Run this script directly to process that dataset.

Command:
    python -m src.data_manipulation.ETL.Test
""" 
from .DataProcessor import DataProcessor
from dotenv import load_dotenv
#-- TEMP__
import os

def main():
    load_dotenv()
    ##Unsure but i think for window the slashes are a different direction
    # ##TODO: Make this more flexible for different operating systems
    # path = r"data/csv_data/NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    # dp = DataProcessor(path)
    # dp.RunTest()
    # print("----------------------------------------------------------------")
    # path = r"data/csv_data/NDS-WKS-SN6543-2025-09-19-07-41-49-0003-BeamCheckTemplate15x"
    # dp = DataProcessor(path)
    # dp.RunTest()
    # print("----------------------------------------------------------------")
    # path = r"data/csv_data/NDS-WKS-SN6543-2025-09-19-07-41-49-0008-GeometryCheckTemplate6xMVkVEnhancedCouch"
    # dp = DataProcessor(path)
    # dp.RunTest()
    # print("--------------------Image Processing Test----------------------------")
    # path = r"data/csv_data/NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    # dp = DataProcessor(path)
    # dp.RunTest()
    print("--------------------Baseline Table Uploader----------------------------")
    print("IN TEST.PY:  SUPABASE_URL =", os.getenv("SUPABASE_URL"))
    path = r"data\csv_data\TST-TST-SN5512-2015-09-19-11-11-11-0004-BeamForceBaseline6e"
    dp = DataProcessor(path)
            #Run, not RunTest so we can see if it makes it to the DB
    dp.Run()
    
if __name__ == "__main__":
    main()
