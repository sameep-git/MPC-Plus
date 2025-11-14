namespace Api.Models;

/// <summary>
/// Represents the check statuses for a specific day in the calendar view.
/// </summary>
public class DayCheckStatus
{
    /// <summary>Date of the checks.</summary>
    public required DateTime Date { get; set; }

    /// <summary>Overall beam check status for the day (null if no checks).</summary>
    public string? BeamCheckStatus { get; set; }

    /// <summary>Overall geometry check status for the day (null if no checks).</summary>
    public string? GeometryCheckStatus { get; set; }
}
