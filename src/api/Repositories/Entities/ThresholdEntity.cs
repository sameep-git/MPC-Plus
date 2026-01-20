using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for threshold data.
/// </summary>
[Table("thresholds")]
public class ThresholdEntity : BaseModel
{
    [PrimaryKey("id", false)]
    public string Id { get; set; } = default!;

    [Column("machine_id")]
    public string MachineId { get; set; } = default!;

    [Column("check_type")]
    public string CheckType { get; set; } = default!;

    [Column("beam_variant")]
    public string? BeamVariant { get; set; }

    [Column("metric_type")]
    public string MetricType { get; set; } = default!;

    [Column("value")]
    public double Value { get; set; }

    [Column("last_updated")]
    public DateTime? LastUpdated { get; set; }

    [Column("created_at")]
    public DateTime? CreatedAt { get; set; }

    /// <summary>
    /// Converts this entity to a domain model.
    /// </summary>
    public Threshold ToModel() =>
        new()
        {
            Id = Id,
            MachineId = MachineId,
            CheckType = CheckType,
            BeamVariant = BeamVariant,
            MetricType = MetricType,
            Value = Value,
            LastUpdated = LastUpdated ?? DateTime.UtcNow // Fallback if null
        };

    /// <summary>
    /// Converts a domain model to this entity.
    /// </summary>
    public static ThresholdEntity FromModel(Threshold threshold) =>
        new()
        {
            Id = threshold.Id ?? Guid.NewGuid().ToString(),
            MachineId = threshold.MachineId,
            CheckType = threshold.CheckType,
            BeamVariant = threshold.BeamVariant,
            MetricType = threshold.MetricType,
            Value = threshold.Value ?? 0,
            LastUpdated = threshold.LastUpdated
        };
}
