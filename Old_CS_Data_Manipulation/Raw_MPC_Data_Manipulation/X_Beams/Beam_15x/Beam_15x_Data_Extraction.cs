using System;
using System.Xml;
using MPC_Plus.Exceptions;

public class Beam_15x_Data_Extraction : X_Data_Extraction
{
    private string pathName = string.Empty;
    private XmlDocument doc = new XmlDocument();

    // Store single values instead of node lists
    public decimal RelativeOutput { get; private set; }
    public decimal RelativeUniformity { get; private set; }
    public decimal CenterShift { get; private set; }

    // Constructor: takes a pathname
    public Beam_15x_Data_Extraction(string pathName)
    {
        this.pathName = System.IO.Path.Combine(pathName, "results.xml");
        this.doc = new XmlDocument();
    }

    // Default constructor (optional)
    public Beam_15x_Data_Extraction()
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
        RelativeOutput = (outputValue - 1) * 100;

        // Get first <RelativeUniformity> node
        XmlNode uniformityNode = doc.GetElementsByTagName("RelativeUniformity")[0];
        if (!decimal.TryParse(uniformityNode.InnerText, out decimal uniformityValue))
            throw new Exception("Invalid decimal value in RelativeUniformity node.");
        //Convert to Percentage
        RelativeUniformity = uniformityValue * 100;
        
        //Calculate and Set center shift
        CenterShift = calculateCenterShift();
    }

    public decimal calculateCenterShift(){
        decimal baselineX, baselineY;
        decimal isoX, isoY;
        decimal shift;
        
        // Create a namespace manager to handle the "http:/www.varian.com/MPC" namespace
        XmlNamespaceManager ns = new XmlNamespaceManager(doc.NameTable);
        ns.AddNamespace("v", "http:/www.varian.com/MPC");

        // Select the BaselineIsoCenter and IsoCenter nodes
        XmlNode baselineNode = doc.SelectSingleNode("//v:BaselineIsoCenter", ns);
        XmlNode isoNode = doc.SelectSingleNode("//v:IsoCenter", ns);

        if (baselineNode != null && isoNode != null)
        {
            baselineX = decimal.Parse(baselineNode.SelectSingleNode("v:X", ns).InnerText);
            baselineY = decimal.Parse(baselineNode.SelectSingleNode("v:Y", ns).InnerText);
            isoX = decimal.Parse(isoNode.SelectSingleNode("v:X", ns).InnerText);
            isoY = decimal.Parse(isoNode.SelectSingleNode("v:Y", ns).InnerText);
        }
        else
        {
            return -1;
        }

        // Compute deltas
        decimal deltaX = isoX - baselineX;
        decimal deltaY = isoY - baselineY;

        //Compute Euclidean distance (cm)
        shift = (decimal)Math.Sqrt((double)(deltaX * deltaX + deltaY * deltaY));

        //Convert to mm
        shift = shift * 10;
        return shift;


    }

    // Test method to print the values
    public void ExtractTest()
    {
        Extract();
        Console.WriteLine($"RelativeOutput: {RelativeOutput}");
        Console.WriteLine($"RelativeUniformity: {RelativeUniformity}");
        Console.WriteLine($"CenterShift: {CenterShift}");
    }

    public void Upload()
    {
        // Implement database upload if needed
    }
}
