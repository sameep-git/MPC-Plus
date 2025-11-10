namespace Api.Services;

/// <summary>
/// Simplified REST client abstraction targeting Supabase PostgREST endpoints.
/// </summary>
public interface ISupabaseRestClient
{
    Task<IReadOnlyList<T>> GetListAsync<T>(string resource, string query, CancellationToken cancellationToken);

    Task<T?> GetSingleAsync<T>(string resource, string query, CancellationToken cancellationToken);

    Task<bool> InsertAsync<T>(string resource, T payload, CancellationToken cancellationToken);

    Task<bool> UpsertAsync<T>(string resource, T payload, string matchQuery, CancellationToken cancellationToken);

    Task<bool> DeleteAsync(string resource, string matchQuery, CancellationToken cancellationToken);
}

