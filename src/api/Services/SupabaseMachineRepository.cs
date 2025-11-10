using Api.Models;
using Api.Options;
using Microsoft.Extensions.Options;

namespace Api.Services;

/// <summary>
/// Repository backed by Supabase PostgREST endpoints to manage machines.
/// </summary>
public class SupabaseMachineRepository : IMachineRepository
{
    private readonly ISupabaseRestClient _restClient;
    private readonly SupabaseOptions _options;

    public SupabaseMachineRepository(ISupabaseRestClient restClient, IOptions<SupabaseOptions> options)
    {
        _restClient = restClient;
        _options = options.Value;
    }

    public Task<IReadOnlyList<Machine>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        var query = "select=*";
        return _restClient.GetListAsync<Machine>(GetResource(), query, cancellationToken);
    }

    public Task<Machine?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        var query = $"id=eq.{Uri.EscapeDataString(id)}&select=*";
        return _restClient.GetSingleAsync<Machine>(GetResource(), query, cancellationToken);
    }

    public async Task<bool> CreateAsync(Machine machine, CancellationToken cancellationToken = default)
    {
        return await _restClient.InsertAsync(GetResource(), machine, cancellationToken);
    }

    public async Task<bool> UpdateAsync(Machine machine, CancellationToken cancellationToken = default)
    {
        var matchQuery = $"id=eq.{Uri.EscapeDataString(machine.Id)}";
        return await _restClient.UpsertAsync(GetResource(), machine, matchQuery, cancellationToken);
    }

    public Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        var matchQuery = $"id=eq.{Uri.EscapeDataString(id)}";
        return _restClient.DeleteAsync(GetResource(), matchQuery, cancellationToken);
    }

    private string GetResource() => _options.MachinesTable;
}

