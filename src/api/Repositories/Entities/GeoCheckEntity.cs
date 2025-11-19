using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using System.Text.Json;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for geometry check data.
/// </summary>
[Table("geochecks")]
public class GeoCheckEntity : BaseModel
{
    [PrimaryKey("id", false)]
    public string Id { get; set; } = default!;

    [Column("type")]
    public string Type { get; set; } = default!;

    [Column("date")]
    public DateOnly Date { get; set; }

    [Column("machine_id")]
    public string MachineId { get; set; } = default!;

    [Column("path")]
    public string? Path { get; set; }

    // ---- IsoCenterGroup ----
    [Column("iso_center_size")]
    public double? IsoCenterSize { get; set; }

    [Column("iso_center_mv_offset")]
    public double? IsoCenterMVOffset { get; set; }

    [Column("iso_center_kv_offset")]
    public double? IsoCenterKVOffset { get; set; }

    // ---- BeamGroup ----
    [Column("relative_output")]
    public double? RelativeOutput { get; set; }

    [Column("relative_uniformity")]
    public double? RelativeUniformity { get; set; }

    [Column("center_shift")]
    public double? CenterShift { get; set; }

    // ---- CollimationGroup ----
    [Column("collimation_rotation_offset")]
    public double? CollimationRotationOffset { get; set; }

    // ---- GantryGroup ----
    [Column("gantry_absolute")]
    public double? GantryAbsolute { get; set; }

    [Column("gantry_relative")]
    public double? GantryRelative { get; set; }

    // ---- EnhancedCouchGroup ----
    [Column("couch_max_position_error")]
    public double? CouchMaxPositionError { get; set; }

    [Column("couch_lat")]
    public double? CouchLat { get; set; }

    [Column("couch_lng")]
    public double? CouchLng { get; set; }

    [Column("couch_vrt")]
    public double? CouchVrt { get; set; }

    [Column("couch_rtn_fine")]
    public double? CouchRtnFine { get; set; }

    [Column("couch_rtn_large")]
    public double? CouchRtnLarge { get; set; }

    [Column("rotation_induced_couch_shift_full_range")]
    public double? RotationInducedCouchShiftFullRange { get; set; }

    // ---- MLCGroup ----
    [Column("mlc_leaves_a")]
    public string? MLCLeavesAJson { get; set; }

    [Column("mlc_leaves_b")]
    public string? MLCLeavesBJson { get; set; }

    [Column("max_offset_a")]
    public double? MaxOffsetA { get; set; }

    [Column("max_offset_b")]
    public double? MaxOffsetB { get; set; }

    [Column("mean_offset_a")]
    public double? MeanOffsetA { get; set; }

    [Column("mean_offset_b")]
    public double? MeanOffsetB { get; set; }

    // ---- MLCBacklashGroup ----
    [Column("mlc_backlash_a")]
    public string? MLCBacklashAJson { get; set; }

    [Column("mlc_backlash_b")]
    public string? MLCBacklashBJson { get; set; }

    [Column("mlc_backlash_max_a")]
    public double? MLCBacklashMaxA { get; set; }

    [Column("mlc_backlash_max_b")]
    public double? MLCBacklashMaxB { get; set; }

    [Column("mlc_backlash_mean_a")]
    public double? MLCBacklashMeanA { get; set; }

    [Column("mlc_backlash_mean_b")]
    public double? MLCBacklashMeanB { get; set; }

    // ---- JawsGroup ----
    [Column("jaw_x1")]
    public double? JawX1 { get; set; }

    [Column("jaw_x2")]
    public double? JawX2 { get; set; }

    [Column("jaw_y1")]
    public double? JawY1 { get; set; }

    [Column("jaw_y2")]
    public double? JawY2 { get; set; }

    // ---- JawsParallelismGroup ----
    [Column("jaw_parallelism_x1")]
    public double? JawParallelismX1 { get; set; }

    [Column("jaw_parallelism_x2")]
    public double? JawParallelismX2 { get; set; }

    [Column("jaw_parallelism_y1")]
    public double? JawParallelismY1 { get; set; }

    [Column("jaw_parallelism_y2")]
    public double? JawParallelismY2 { get; set; }

    [Column("note")]
    public string? Note { get; set; }

    /// <summary>
    /// Converts this entity to a domain model.
    /// </summary>
    public GeoCheck ToModel()
    {
        return new GeoCheck
        {
            Id = Id,
            Type = Type,
            Date = Date,
            MachineId = MachineId,
            Path = Path,
            IsoCenterSize = IsoCenterSize,
            IsoCenterMVOffset = IsoCenterMVOffset,
            IsoCenterKVOffset = IsoCenterKVOffset,
            RelativeOutput = RelativeOutput,
            RelativeUniformity = RelativeUniformity,
            CenterShift = CenterShift,
            CollimationRotationOffset = CollimationRotationOffset,
            GantryAbsolute = GantryAbsolute,
            GantryRelative = GantryRelative,
            CouchMaxPositionError = CouchMaxPositionError,
            CouchLat = CouchLat,
            CouchLng = CouchLng,
            CouchVrt = CouchVrt,
            CouchRtnFine = CouchRtnFine,
            CouchRtnLarge = CouchRtnLarge,
            RotationInducedCouchShiftFullRange = RotationInducedCouchShiftFullRange,
            MLCLeavesA = DeserializeLeaves(MLCLeavesAJson),
            MLCLeavesB = DeserializeLeaves(MLCLeavesBJson),
            MaxOffsetA = MaxOffsetA,
            MaxOffsetB = MaxOffsetB,
            MeanOffsetA = MeanOffsetA,
            MeanOffsetB = MeanOffsetB,
            MLCBacklashA = DeserializeLeaves(MLCBacklashAJson),
            MLCBacklashB = DeserializeLeaves(MLCBacklashBJson),
            MLCBacklashMaxA = MLCBacklashMaxA,
            MLCBacklashMaxB = MLCBacklashMaxB,
            MLCBacklashMeanA = MLCBacklashMeanA,
            MLCBacklashMeanB = MLCBacklashMeanB,
            JawX1 = JawX1,
            JawX2 = JawX2,
            JawY1 = JawY1,
            JawY2 = JawY2,
            JawParallelismX1 = JawParallelismX1,
            JawParallelismX2 = JawParallelismX2,
            JawParallelismY1 = JawParallelismY1,
            JawParallelismY2 = JawParallelismY2,
            Note = Note
        };
    }

    /// <summary>
    /// Converts a domain model to this entity.
    /// </summary>
    public static GeoCheckEntity FromModel(GeoCheck geoCheck)
    {
        return new GeoCheckEntity
        {
            Id = geoCheck.Id,
            Type = geoCheck.Type,
            Date = geoCheck.Date,
            MachineId = geoCheck.MachineId,
            Path = geoCheck.Path,
            IsoCenterSize = geoCheck.IsoCenterSize,
            IsoCenterMVOffset = geoCheck.IsoCenterMVOffset,
            IsoCenterKVOffset = geoCheck.IsoCenterKVOffset,
            RelativeOutput = geoCheck.RelativeOutput,
            RelativeUniformity = geoCheck.RelativeUniformity,
            CenterShift = geoCheck.CenterShift,
            CollimationRotationOffset = geoCheck.CollimationRotationOffset,
            GantryAbsolute = geoCheck.GantryAbsolute,
            GantryRelative = geoCheck.GantryRelative,
            CouchMaxPositionError = geoCheck.CouchMaxPositionError,
            CouchLat = geoCheck.CouchLat,
            CouchLng = geoCheck.CouchLng,
            CouchVrt = geoCheck.CouchVrt,
            CouchRtnFine = geoCheck.CouchRtnFine,
            CouchRtnLarge = geoCheck.CouchRtnLarge,
            RotationInducedCouchShiftFullRange = geoCheck.RotationInducedCouchShiftFullRange,
            MLCLeavesAJson = SerializeLeaves(geoCheck.MLCLeavesA),
            MLCLeavesBJson = SerializeLeaves(geoCheck.MLCLeavesB),
            MaxOffsetA = geoCheck.MaxOffsetA,
            MaxOffsetB = geoCheck.MaxOffsetB,
            MeanOffsetA = geoCheck.MeanOffsetA,
            MeanOffsetB = geoCheck.MeanOffsetB,
            MLCBacklashAJson = SerializeLeaves(geoCheck.MLCBacklashA),
            MLCBacklashBJson = SerializeLeaves(geoCheck.MLCBacklashB),
            MLCBacklashMaxA = geoCheck.MLCBacklashMaxA,
            MLCBacklashMaxB = geoCheck.MLCBacklashMaxB,
            MLCBacklashMeanA = geoCheck.MLCBacklashMeanA,
            MLCBacklashMeanB = geoCheck.MLCBacklashMeanB,
            JawX1 = geoCheck.JawX1,
            JawX2 = geoCheck.JawX2,
            JawY1 = geoCheck.JawY1,
            JawY2 = geoCheck.JawY2,
            JawParallelismX1 = geoCheck.JawParallelismX1,
            JawParallelismX2 = geoCheck.JawParallelismX2,
            JawParallelismY1 = geoCheck.JawParallelismY1,
            JawParallelismY2 = geoCheck.JawParallelismY2,
            Note = geoCheck.Note
        };
    }

    private static Dictionary<string, double>? DeserializeLeaves(string? json)
    {
        if (string.IsNullOrWhiteSpace(json))
            return null;

        try
        {
            return JsonSerializer.Deserialize<Dictionary<string, double>>(json);
        }
        catch
        {
            return null;
        }
    }

    private static string? SerializeLeaves(Dictionary<string, double>? leaves)
    {
        if (leaves == null || leaves.Count == 0)
            return null;

        return JsonSerializer.Serialize(leaves);
    }
}
