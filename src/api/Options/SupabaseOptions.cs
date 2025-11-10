namespace Api.Options;

/// <summary>
/// Configuration values required to interact with Supabase REST API.
/// </summary>
public class SupabaseOptions
{
    /// <summary>
    /// Base URL of the Supabase project (e.g., https://xyzcompany.supabase.co).
    /// </summary>
    public required string Url { get; set; }

    /// <summary>
    /// Service role API key used to authorize requests.
    /// </summary>
    public required string ApiKey { get; set; }

    /// <summary>
    /// Optional schema name. Defaults to public.
    /// </summary>
    public string Schema { get; set; } = "public";

    /// <summary>
    /// Optional table name override for machines. Defaults to machines.
    /// </summary>
    public string MachinesTable { get; set; } = "machines";
}

