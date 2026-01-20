using Api.Models;
using Api.Repositories.Abstractions;
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

    public async Task<IEnumerable<Threshold>> GetAllAsync()
    {
        try
        {
            var result = await _client.From<ThresholdEntity>().Get();
            return result.Models.Select(e => e.ToModel());
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching thresholds from Supabase");
            throw;
        }
    }

    public async Task<Threshold?> GetAsync(string machineId, string checkType, string metricType, string? beamVariant = null)
    {
        try
        {
            var query = _client.From<ThresholdEntity>()
                .Match(new Dictionary<string, string>
                {
                    { "machine_id", machineId },
                    { "check_type", checkType },
                    { "metric_type", metricType }
                });

            if (!string.IsNullOrEmpty(beamVariant))
            {
                query = query.Filter("beam_variant", Supabase.Postgrest.Constants.Operator.Equals, beamVariant);
            }
             
            var result = await query.Get();
            return result.Models.FirstOrDefault()?.ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching threshold from Supabase");
            throw;
        }
    }

    public async Task<Threshold> UpsertAsync(Threshold threshold)
    {
        try
        {
            var entity = ThresholdEntity.FromModel(threshold);
            
            var result = await _client
                .From<ThresholdEntity>()
                .Upsert(entity);
            
            var model = result.Models.FirstOrDefault();

            if (model == null)
            {
                // If upsert doesn't return model, maybe fetch it? 
                // Supabase usually returns the row if we ask, or standard Upsert response.
                // Assuming it works like Insert.
                throw new InvalidOperationException("Failed to upsert threshold");
            }

            return model.ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error upserting threshold to Supabase");
            throw;
        }
    }
}
