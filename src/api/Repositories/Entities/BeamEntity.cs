using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for beam data.
/// </summary>
[Table("beams")]
public class BeamEntity : BaseModel
{
    [PrimaryKey("id", false)]
    public string Id { get; set; } = default!;

    [Column("type")]
    public string Type { get; set; } = default!;

    [Column("date")]
    public DateTime Date { get; set; }

    [Column("path")]
    public string? Path { get; set; }

    [Column("rel_uniformity")]
    public double? RelUniformity { get; set; }

    [Column("rel_output")]
    public double? RelOutput { get; set; }

    [Column("center_shift")]
    public double? CenterShift { get; set; }

    [Column("machine_id")]
    public string MachineId { get; set; } = default!;

    [Column("note")]
    public string? Note { get; set; }

    [Column("approved_by")]
    public string? AcceptedBy { get; set; }

    [Column("approved_date")]
    public DateTime? AcceptedDate { get; set; }

    [Column("timestamp")]
    public DateTime? Timestamp { get; set; }

    /// <summary>
    /// Converts this entity to a domain model.
    /// </summary>
    public Beam ToModel() =>
        new()
        {
            Id = Id,
            Type = Type,
            Date = Date,
            Timestamp = Timestamp,
            Path = Path,
            RelUniformity = RelUniformity,
            RelOutput = RelOutput,
            CenterShift = CenterShift,
            MachineId = MachineId,
            Note = Note,
            AcceptedBy = AcceptedBy,
            AcceptedDate = AcceptedDate
        };

    /// <summary>
    /// Converts a domain model to this entity.
    /// </summary>
    public static BeamEntity FromModel(Beam beam) =>
        new()
        {
            Id = beam.Id,
            Type = beam.Type,
            Date = beam.Date,
            Timestamp = beam.Timestamp,
            Path = beam.Path,
            RelUniformity = beam.RelUniformity,
            RelOutput = beam.RelOutput,
            CenterShift = beam.CenterShift,
            MachineId = beam.MachineId,
            Note = beam.Note,
            AcceptedBy = beam.AcceptedBy,
            AcceptedDate = beam.AcceptedDate
        };
}
