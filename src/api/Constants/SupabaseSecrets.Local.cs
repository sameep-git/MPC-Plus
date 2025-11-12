using Microsoft.Extensions.Configuration;

namespace Api.Constants;

/// <summary>
/// Example secrets file for local development.
/// Copy this file to <c>SupabaseSecrets.Local.cs</c> and fill in real values.
/// </summary>
public static partial class SupabaseSecrets
{
    /// <summary>
    /// Applies local Supabase secrets to the runtime configuration.
    /// </summary>
    /// <remarks>
    /// Replace the placeholder values below in your local copy with real credentials.
    /// This sample returns without modifying configuration so that repository builds
    /// succeed without any local secrets present.
    /// </remarks>
    static partial void ConfigureSupabaseInternal(IConfiguration configuration)
    {
        // Example (uncomment and update in your local copy only):
        // configuration["Supabase:Url"] = "https://your-project.supabase.co";
        // configuration["Supabase:ApiKey"] = "service-role-key";
        // configuration["Supabase:Schema"] = "public";
        // configuration["Supabase:MachinesTable"] = "machines";
    }
}

