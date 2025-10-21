using System;

public class BeamCaller
{
    private string pathName = string.Empty;

    // Constructor: takes a pathname
    public BeamCaller(string pathName)
    {
        this.pathName = pathName;
    }

    // Default Constructor: Creates an error
    public BeamCaller()
    {
        //throw new NoPathGivenException($"Failed to load XML file at path: {pathName}", ex);
    }

    // The main method that decides what to do based on the path
    public void Run()
    {
        if (pathName.Contains("6e"))
        {
            //Create a 6e beam instance
            Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
            //Populate the instance vairables with data from the XML file
            my6e_beam.Extract();
            //Upload the instace vairables to the database
            my6e_beam.Upload();
        }
        // else if (pathName.Contains("9e"))
        // {
        //     //Create a 6e beam instance
        //     Beam_9e_Data_Extraction my9e_beam = new Beam_9e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my9e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my9e_beam.Upload();
        // }
        // else if (pathName.Contains("12e"))
        // {
        //     //Create a 6e beam instance
        //     Beam_12e_Data_Extraction my12e_beam = new Beam_12e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my12e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my12e_beam.Upload();
        // }
        // else if (pathName.Contains("16e"))
        // {
        //     //Create a 6e beam instance
        //     Beam_16e_Data_Extraction my16e_beam = new Beam_16e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my16e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my16e_beam.Upload();
        // }
        // else if (pathName.Contains("2.5x"))
        // {
        //     //Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my6e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("6x")) //Geometry Check
        // {
        //     //Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my6e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("6xfff"))
        // {
        //     //Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my6e_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("10x"))
        // {
        //     //Create a 6e beam instance
        //     Beam_10x_Data_Extraction my10x_beam = new Beam_10x_Data_Extraction(pathName);
        //     //Populate the instance vairables with data from the XML file
        //     my10x_beam.Extract();
        //     //Upload the instace vairables to the database
        //     my10x_beam.Upload();
        // }
        else if (pathName.Contains("15x"))
        {
            //Create a 15x beam instance
            Beam_15x_Data_Extraction my15x_beam = new Beam_15x_Data_Extraction(pathName);
            //Populate the instance vairables with data from the XML file
            my15x_beam.Extract();
            //Upload the instace vairables to the database
            my15x_beam.Upload();
        }
        else
        {
            //throw new NoPathGivenException($"Failed to load XML file at path: {pathName}", ex); 
        }
    }



    public void RunTest()
    {
        if (pathName.Contains("6e"))
        {
            //Create a 6e beam instance
            Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
            //Populate the instance vairables with data from the XML file
            my6e_beam.ExtractTest();
            //Upload the instace vairables to the database
            my6e_beam.Upload();
        }
        // else if (pathName.Contains("9e"))
        // {
        //     // Create a 9e beam instance
        //     Beam_9e_Data_Extraction my9e_beam = new Beam_9e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my9e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my9e_beam.Upload();
        // }
        // else if (pathName.Contains("12e"))
        // {
        //     // Create a 12e beam instance
        //     Beam_12e_Data_Extraction my12e_beam = new Beam_12e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my12e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my12e_beam.Upload();
        // }
        // else if (pathName.Contains("16e"))
        // {
        //     // Create a 16e beam instance
        //     Beam_16e_Data_Extraction my16e_beam = new Beam_16e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my16e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my16e_beam.Upload();
        // }
        // else if (pathName.Contains("2.5x"))
        // {
        //     // Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my6e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("6x")) // Geometry Check
        // {
        //     // Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my6e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("6xfff"))
        // {
        //     // Create a 6e beam instance
        //     Beam_6e_Data_Extraction my6e_beam = new Beam_6e_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my6e_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my6e_beam.Upload();
        // }
        // else if (pathName.Contains("10x"))
        // {
        //     // Create a 10x beam instance
        //     Beam_10x_Data_Extraction my10x_beam = new Beam_10x_Data_Extraction(pathName);
        //     // Populate the instance variables with data from the XML file
        //     my10x_beam.ExtractTest();
        //     // Upload the instance variables to the database
        //     my10x_beam.Upload();
        // }
        else if (pathName.Contains("15x"))
        {
            //Create a 15x beam instance
            Beam_15x_Data_Extraction my15x_beam = new Beam_15x_Data_Extraction(pathName);
            //Populate the instance vairables with data from the XML file
            my15x_beam.ExtractTest();
            //Upload the instace vairables to the database
            my15x_beam.Upload();
        }
        else
        {
            //throw new NoPathGivenException($"Failed to load XML file at path: {pathName}", ex); 
        }

    }
}