using System;
using System.Xml;

class Program
{
    static void Main()
    {
        // Load XML file
        XmlDocument doc = new XmlDocument();
        doc.Load("BeamCheck16e.xml"); // Make sure Results.xml is in the same folder

        // Select the BeamProfileCheck node
        XmlNode node = doc.SelectSingleNode("//d2p1:anyType[@i:type='BeamProfileCheck']", ns);

        if (node != null)
        {
            string relativeOutput = node["RelativeOutput"]?.InnerText;
            string relativeUniformity = node["RelativeUniformity"]?.InnerText;

            Console.WriteLine("BeamProfileCheck Data:");
            Console.WriteLine($"  RelativeOutput: {relativeOutput}");
            Console.WriteLine($"  RelativeUniformity: {relativeUniformity}");
        }
        else
        {
            Console.WriteLine("BeamProfileCheck node not found.");
        }
    }
}
