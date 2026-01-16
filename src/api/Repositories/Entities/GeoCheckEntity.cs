using Api.Models;
using Supabase.Postgrest.Attributes;
using Api.Repositories.Entities;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for geometry check data (writes to table).
/// </summary>
[Table("geochecks")]
public class GeoCheckEntity : GeoCheckEntityBase
{
    /// <summary>
    /// Converts a domain model to this entity.
    /// </summary>
    public static GeoCheckEntity FromModel(GeoCheck geoCheck)
    {
        var entity = new GeoCheckEntity();
        UpdateEntityFromModel(entity, geoCheck);
        return entity;
    }
}
