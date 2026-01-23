using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace Api.Repositories.Entities;

[Table("thresholds")]
public class ThresholdEntity : BaseModel
{
    [Column("machine_id")]
    public string MachineId { get; set; } = default!;

    [Column("check_type")]
    public string CheckType { get; set; } = default!;

    [Column("beam_variant")]
    public string? BeamVariant { get; set; }

    [Column("metric_type")]
    public string MetricType { get; set; } = default!;

    [Column("last_updated")]
    public DateTime LastUpdated { get; set; }

    [Column("value")]
    public double? Value { get; set; }

    public static ThresholdEntity FromModel(Threshold threshold) =>
        new()
        {
            MachineId = threshold.MachineId,
            CheckType = threshold.CheckType,
            BeamVariant = threshold.BeamVariant,
            MetricType = threshold.MetricType,
            LastUpdated = threshold.LastUpdated,
            Value = threshold.Value
        };

    public Threshold ToModel() =>
        new()
        {
            MachineId = MachineId,
            CheckType = CheckType,
            BeamVariant = BeamVariant,
            MetricType = MetricType,
            LastUpdated = LastUpdated,
            Value = Value
        };
}
