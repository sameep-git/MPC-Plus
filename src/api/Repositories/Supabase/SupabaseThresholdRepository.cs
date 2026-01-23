using Api.Models;
using Api.Repositories.Entities;
using Microsoft.Extensions.Logging;
using Supabase;

namespace Api.Repositories;

public class SupabaseThresholdRepository : IThresholdRepository
{
    private readonly Client _client;
    private readonly ILogger<SupabaseThresholdRepository> _logger;

    public SupabaseThresholdRepository(Client client, ILogger<SupabaseThresholdRepository> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<IReadOnlyList<Threshold>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var response = await _client
            .From<ThresholdEntity>()
            .Get();

        return response.Models.Select(entity => entity.ToModel()).ToList();
    }
}
