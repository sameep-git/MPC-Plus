using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using System.Text.Json;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for results data.
/// </summary>
[Table("results")]
public class ResultEntity : BaseModel
{
    [PrimaryKey("id", false)]
    public string Id { get; set; } = default!;

    [Column("month")]
    public int? Month { get; set; }

    [Column("year")]
    public int? Year { get; set; }

    [Column("beam_check")]
    public string? BeamCheckJson { get; set; }

    [Column("status")]
    public string? Status { get; set; }

    /// <summary>
    /// Converts this entity to a domain model.
    /// </summary>
    public Result ToModel()
    {
        IDictionary<string, object?>? beamCheck = null;
        if (!string.IsNullOrWhiteSpace(BeamCheckJson))
        {
            try
            {
                beamCheck = JsonSerializer.Deserialize<IDictionary<string, object?>>(BeamCheckJson);
            }
            catch
            {
                // If deserialization fails, leave beamCheck as null
            }
        }

        return new Result
        {
            Id = Id,
            Month = Month,
            Year = Year,
            BeamCheck = beamCheck,
            Status = Status
        };
    }

    /// <summary>
    /// Converts a domain model to this entity.
    /// </summary>
    public static ResultEntity FromModel(Result result)
    {
        string? beamCheckJson = null;
        if (result.BeamCheck != null)
        {
            try
            {
                beamCheckJson = JsonSerializer.Serialize(result.BeamCheck);
            }
            catch
            {
                // If serialization fails, leave beamCheckJson as null
            }
        }

        return new ResultEntity
        {
            Id = result.Id,
            Month = result.Month,
            Year = result.Year,
            BeamCheckJson = beamCheckJson,
            Status = result.Status
        };
    }
}

