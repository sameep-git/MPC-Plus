using System;
using System.Xml;
public class Beam_6e_Data_Extraction : E_Data_Extraction
{
private string pathName = string.Empty;
private XmlDocument doc = new XmlDocument();
private XmlNodeList relativeOutputNodes = null!;
private XmlNodeList relativeUniformityNodes = null!;


    // Constructor: takes a pathname
    public Beam_6e_Data_Extraction(string pathName)
    {
        this.pathName = pathName;
        this.doc = new XmlDocument();
    }

    // Default Constructor: Creates an error
    public Beam_6e_Data_Extraction()
    {
        //throw NoPathGiven;
    }

    public void Extract()
    {
        doc.Load(pathName);
        relativeOutputNodes = doc.GetElementsByTagName("RelativeOutput");
        relativeUniformityNodes = doc.GetElementsByTagName("RelativeUniformity");
        // Loop through <RelativeOutput> nodes
        foreach (XmlNode node in relativeOutputNodes)
        {
            // Convert the inner text to a decimal
            if (decimal.TryParse(node.InnerText, out decimal outputValue))
            {
                Console.WriteLine($"RelativeOutput: {outputValue}");
            }
            else
            {
                Console.WriteLine("Invalid decimal value in RelativeOutput node.");
            }
        }
        // Loop through <RelativeUniformity> nodes
        foreach (XmlNode node in relativeUniformityNodes)
        {
            if (decimal.TryParse(node.InnerText, out decimal uniformityValue))
            {
                Console.WriteLine($"RelativeUniformity: {uniformityValue}");
            }
            else
            {
                Console.WriteLine("Invalid decimal value in RelativeUniformity node.");
            }
        }
        

    }

    public void Upload()
    {

    }
}
