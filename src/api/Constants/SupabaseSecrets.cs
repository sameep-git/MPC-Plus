using Microsoft.Extensions.Configuration;

namespace Api.Constants;

/// <summary>
/// Provides a hook for injecting Supabase secrets from local, ignored files.
/// </summary>
public static partial class SupabaseSecrets
{
    public static void ConfigureSupabase(IConfiguration configuration)
    {
        ConfigureSupabaseInternal(configuration);
    }

    static partial void ConfigureSupabaseInternal(IConfiguration configuration);
}

