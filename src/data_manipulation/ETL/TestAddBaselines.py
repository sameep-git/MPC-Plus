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
    python -m src.data_manipulation.ETL.TestAddBaselines
""" 
from src.data_manipulation.ETL.DataProcessor import DataProcessor
from dotenv import load_dotenv

def main():
    load_dotenv()
    # print("----------------------6e Baseline Beam Upload--------------------------------")
    # path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0004-BeamForceBaseline6e"
    # dp = DataProcessor(path)
    # dp.Run()
    # print("----------------------6e Baseline Beam Upload Complete--------------------------------")

    # print("----------------------9e Baseline Beam Upload--------------------------------")
    # path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0005-BeamForceBaseline9e"
    # dp = DataProcessor(path)
    # dp.Run()
    # print("----------------------9e Baseline Beam Upload Complete--------------------------------")

    # print("----------------------12e Baseline Beam Upload--------------------------------")
    # path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0006-BeamForceBaseline12e"
    # dp = DataProcessor(path)
    # dp.Run()
    # print("----------------------12e Baseline Beam Upload Complete--------------------------------")

    # print("----------------------16e Baseline Beam Upload--------------------------------")
    # path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0007-BeamForceBaseline16e"
    # dp = DataProcessor(path)
    # dp.Run()
    # print("----------------------16e Baseline Beam Upload Complete--------------------------------")

    #X beams
    print("----------------------2.5x Baseline Beam Upload--------------------------------")
    path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0000-BeamForceBaseline2.5x"
    dp = DataProcessor(path)
    dp.Run()
    print("----------------------2.5x Baseline Beam Upload Complete--------------------------------")

    print("----------------------6xfff Baseline Beam Upload--------------------------------")
    path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0001-BeamForceBaseline6xfff"
    dp = DataProcessor(path)
    dp.Run()
    print("----------------------6xfff Baseline Beam Upload Complete--------------------------------")

    print("----------------------10x Baseline Beam Upload--------------------------------")
    path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0002-BeamForceBaseline10x"
    dp = DataProcessor(path)
    dp.Run()
    print("----------------------10x Baseline Beam Upload Complete--------------------------------")

    print("----------------------15x Baseline Beam Upload--------------------------------")
    path = r"data/baselines/TST-TST-SN6543-2025-08-19-07-41-49-0003-BeamForceBaseline15x"
    dp = DataProcessor(path)
    dp.Run()
    print("----------------------15x Baseline Beam Upload Complete--------------------------------")
    
if __name__ == "__main__":
    main()
