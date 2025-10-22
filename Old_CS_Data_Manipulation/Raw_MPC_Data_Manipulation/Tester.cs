public class Tester
{
    public static void Main()
    {
        Console.WriteLine("6e Beam Test");
        string path = "/Users/braeogle/Desktop/MPC-Plus/data/NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e";
        BeamCaller BC_6e_test = new BeamCaller(path);
        BC_6e_test.RunTest();

        Console.WriteLine("15x Beam Test");
        path = "/Users/braeogle/Desktop/MPC-Plus/data/NDS-WKS-SN6543-2025-09-19-07-41-49-0003-BeamCheckTemplate15x";
        BeamCaller BC_15x_test = new BeamCaller(path);
        BC_15x_test.RunTest();

        Console.WriteLine("Exception Test 1");
        path = "bad_Path";
        BeamCaller bc_except_test1 = new BeamCaller(path);
        bc_except_test1.Run();

        Console.WriteLine("Exception Test 2");
        path = "6e_bad_Path";
        BeamCaller bc_except_test2 = new BeamCaller(path);
        bc_except_test2.Run();

    }
}