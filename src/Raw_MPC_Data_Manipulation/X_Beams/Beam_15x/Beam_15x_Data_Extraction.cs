using System;
using System.Xml;

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
        // throw new NoPathGivenException();
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
        RelativeOutput = outputValue;

        // Get first <RelativeUniformity> node
        XmlNode uniformityNode = doc.GetElementsByTagName("RelativeUniformity")[0];
        if (!decimal.TryParse(uniformityNode.InnerText, out decimal uniformityValue))
            throw new Exception("Invalid decimal value in RelativeUniformity node.");
        RelativeUniformity = uniformityValue;
        
        //Calculate and Set center shift
        CenterShift = calculateCenterShift();
    }

    public decimal calculateCenterShift(){
        decimal baselineX, baselineY;
        decimal isoX, isoY;
        decimal shift;
        

        // Extract BaselineIsoCenter
        XmlNode baselineNode = doc.SelectSingleNode("//BaselineIsoCenter");
        if (baselineNode == null)
        {
            Console.WriteLine("<BaselineIsoCenter> node not found.");
            return -1; //FIX LATER
        }
        baselineX = decimal.Parse(baselineNode["X"].InnerText);
        baselineY = decimal.Parse(baselineNode["Y"].InnerText);

        // Extract IsoCenter
        XmlNode isoNode = doc.SelectSingleNode("//IsoCenter");
        if (isoNode == null)
        {
            Console.WriteLine("<IsoCenter> node not found.");
            return -1; //FIX????
        }
        isoX = decimal.Parse(isoNode["X"].InnerText);
        isoY = decimal.Parse(isoNode["Y"].InnerText);

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
