using Supabase.Postgrest.Attributes;
using Api.Repositories.Entities;

namespace Api.Repositories.Entities;

/// <summary>
/// Supabase entity model for geometry check data (reads from view).
/// </summary>
[Table("geochecks_full")]
public class GeoCheckFullEntity : GeoCheckEntityBase
{
}
