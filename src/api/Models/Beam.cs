namespace Api.Models;

/// <summary>
/// Represents beam data, as defined in the OpenAPI schema.
/// </summary>
public class Beam
{
    /// <summary>Unique identifier for the beam.</summary>
    public required string Id { get; set; }

    /// <summary>Type of beam (e.g., 6e, 9e, 12e, 16e, 10x, 15x, 6xff).</summary>
    public required string Type { get; set; }

    /// <summary>Date of the beam data.</summary>
    public required DateOnly Date { get; set; }

    /// <summary>File path to the beam data.</summary>
    public string? Path { get; set; }

    /// <summary>Relative uniformity value.</summary>
    public double? RelUniformity { get; set; }

    /// <summary>Relative output value.</summary>
    public double? RelOutput { get; set; }

    /// <summary>Center shift value (for X-Beam only).</summary>
    public double? CenterShift { get; set; }

    /// <summary>Associated machine identifier.</summary>
    public required string MachineId { get; set; }

    /// <summary>Notes about the beam.</summary>
    public string? Note { get; set; }
}

