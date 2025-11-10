using System.Text.Json.Serialization;

namespace Api.Models;

/// <summary>
/// Represents a machine definition.
/// </summary>
public class Machine
{
    /// <summary>Unique identifier for the machine.</summary>
    [JsonPropertyName("id")]
    public required string Id { get; set; }

    /// <summary>Physical location of the machine.</summary>
    [JsonPropertyName("location")]
    public required string Location { get; set; }

    /// <summary>Name of the machine.</summary>
    [JsonPropertyName("name")]
    public required string Name { get; set; }

    /// <summary>Type of machine.</summary>
    [JsonPropertyName("type")]
    public required string Type { get; set; }
}

