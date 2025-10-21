using System;

public class BeamCaller
{
    private string pathName;

    // Constructor: takes a pathname
    public BeamCaller(string pathName)
    {
        this.pathName = pathName;
    }

    // Default Constructor: Creates an error
    public BeamCaller()
    {
        //throw NoPathGiven;
    }

    // The main method that decides what to do based on the path
    public void Run()
    {
        if (pathName.Contains("6e"))
        {
            Console.WriteLine("Works");
            Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
            my6e_beam.Extract();
        }
        else if(pathName.Contains("9e")){
            
        }
    }
}