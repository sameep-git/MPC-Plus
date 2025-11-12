namespace Api.Configuration;

public class DatabaseOptions
{
    public const string SectionName = "Database";

    public string Provider { get; init; } = "Supabase";
}

