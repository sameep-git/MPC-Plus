public class Tester
{
    public static void Main()
    {
        string path = "/Users/braeogle/Desktop/MPC-Plus/data/NDS-WKS-SN6543-2025-09-19-07-41-49-0004-BeamCheckTemplate6e";
        BeamCaller myBC = new BeamCaller(path);
        myBC.Run();
    }
}