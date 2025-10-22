using System;
using System.Xml;
using MPC_Plus.Exceptions;

public class Beam_6e_Data_Extraction : E_Data_Extraction
{
    private string pathName = string.Empty;
    private XmlDocument doc = new XmlDocument();

    // Store single values instead of node lists
    public decimal RelativeOutput { get; private set; }
    public decimal RelativeUniformity { get; private set; }

    // Constructor: takes a pathname
    public Beam_6e_Data_Extraction(string pathName)
    {
        this.pathName = System.IO.Path.Combine(pathName, "results.xml");
        this.doc = new XmlDocument();
    }

    // Default constructor (optional)
    public Beam_6e_Data_Extraction()
    {
        throw new NoPathGivenException($"Failed to load XML file at path: {pathName}");
    }

    // Load XML and populate the decimal values
    public void Extract()
    {
        try
        {
            doc.Load(pathName);
        }
        catch (Exception ex)
        {
            throw new Exception($"Failed to load XML file at path: {pathName}", ex);
        }

        // Get first <RelativeOutput> node
        XmlNode outputNode = doc.GetElementsByTagName("RelativeOutput")[0];
        if (!decimal.TryParse(outputNode.InnerText, out decimal outputValue))
            throw new Exception("Invalid decimal value in RelativeOutput node.");
        //!!!! Explain this formula
        RelativeOutput = ((outputValue - 1) * 100 ) * 100;

        // Get first <RelativeUniformity> node
        XmlNode uniformityNode = doc.GetElementsByTagName("RelativeUniformity")[0];
        if (!decimal.TryParse(uniformityNode.InnerText, out decimal uniformityValue))
            throw new Exception("Invalid decimal value in RelativeUniformity node.");
        //Convert to Percentage
        RelativeUniformity = uniformityValue * 100;
    }

    // Test method to print the values
    public void ExtractTest()
    {
        Extract();
        Console.WriteLine($"RelativeOutput: {RelativeOutput}");
        Console.WriteLine($"RelativeUniformity: {RelativeUniformity}");
    }

    public void Upload()
    {
        // Implement database upload if needed
    }
}
