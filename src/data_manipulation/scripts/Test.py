from data_manipulation.scripts.DataProcessor import DataProcessor

def main():
    #path = r"C:\Users\Bonny Brae\Desktop\MPC-Plus\data\NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e"
    path = r"C:\Users\Bonny Brae\Desktop\MPC-Plus\data\NDS-WKS-SN6543-2025-09-19-07-41-49-0003-BeamCheckTemplate15x"
    dp = DataProcessor(path)
    dp.Run()

if __name__ == "__main__":
    main()