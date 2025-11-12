namespace Api.Configuration;

public class SupabaseSettings
{
    public const string SectionName = "Supabase";

    public string? Url { get; init; }

    public string? Key { get; init; }
}

