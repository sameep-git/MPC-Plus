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
            else
            {
                // Explicitly filter for NULL if beamVariant is null, to avoid ambiguous matches
                query = query.Filter("beam_variant", Supabase.Postgrest.Constants.Operator.Is, "null");
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
            // First, try to find existing threshold by composite key
            var query = _client.From<ThresholdEntity>()
                .Filter("machine_id", Supabase.Postgrest.Constants.Operator.Equals, threshold.MachineId)
                .Filter("check_type", Supabase.Postgrest.Constants.Operator.Equals, threshold.CheckType)
                .Filter("metric_type", Supabase.Postgrest.Constants.Operator.Equals, threshold.MetricType);

            if (!string.IsNullOrEmpty(threshold.BeamVariant))
            {
                query = query.Filter("beam_variant", Supabase.Postgrest.Constants.Operator.Equals, threshold.BeamVariant);
            }
            else
            {
                query = query.Filter("beam_variant", Supabase.Postgrest.Constants.Operator.Is, "null");
            }
            
            var existingResult = await query.Get();
            var existing = existingResult.Models.FirstOrDefault();

            // If exists, delete it first (simpler than trying to Update which has issues)
            if (existing != null)
            {
                await _client.From<ThresholdEntity>()
                    .Match(new Dictionary<string, string> { { "id", existing.Id } })
                    .Delete();
            }

            // Now insert the new/updated row
            var entity = ThresholdEntity.FromModel(threshold);
            var result = await _client
                .From<ThresholdEntity>()
                .Insert(entity);
            
            var model = result.Models.FirstOrDefault();

            if (model == null)
            {
                return threshold;
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
