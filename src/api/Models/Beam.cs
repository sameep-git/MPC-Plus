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
    public required DateTime Date { get; set; }

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

    /// <summary>Name of the person who accepted/signed off the beam check.</summary>
    public string? AcceptedBy { get; set; }

    /// <summary>Date when the beam check was accepted/signed off.</summary>
    public DateTime? AcceptedDate { get; set; }

    /// <summary>
    /// Convenience property representing a single numeric value to display in UIs.
    /// Priority: RelOutput, RelUniformity, CenterShift.
    /// This is not persisted to the database; it's computed by repositories.
    /// </summary>
    public double? Value { get; set; }
}

