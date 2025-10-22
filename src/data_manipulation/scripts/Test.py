from DataProcessor import DataProcessor

def main():
    path = "/Users/braeogle/Desktop/MPC-Plus/data/NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    dp = DataProcessor("path")
    dp.Run()

if __name__ == "__main__":
    main()