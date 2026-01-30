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

    public async Task<Threshold> SaveAsync(Threshold threshold, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        // Update LastUpdated timestamp
        threshold.LastUpdated = DateTime.UtcNow;

        var entity = ThresholdEntity.FromModel(threshold);

        // We assume valid model here (MachineId, CheckType, MetricType must serve as keys).
        // Upsert will handle both creation and update.
        // Supabase-csharp requires properties to be mapped.
        // Note: For Upsert to work on composite keys (machine_id, check_type, metric_type), 
        // there must be a unique constraint on these columns in the DB.
        
        var response = await _client
            .From<ThresholdEntity>()
            .OnConflict("machine_id, check_type, beam_variant, metric_type")
            .Upsert(entity);

        var result = response.Models.FirstOrDefault();
        if (result == null)
        {
            throw new InvalidOperationException("Failed to save threshold.");
        }

        return result.ToModel();
    }
}
