using Api.Models;
using Api.Repositories.Abstractions;
using Api.Repositories.Entities;
using Microsoft.Extensions.Logging;
using Supabase;
using Supabase.Postgrest.Exceptions;

namespace Api.Repositories;

public class SupabaseGeoCheckRepository : IGeoCheckRepository
{
    private readonly Client _client;
    private readonly ILogger<SupabaseGeoCheckRepository> _logger;

    public SupabaseGeoCheckRepository(Client client, ILogger<SupabaseGeoCheckRepository> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<IReadOnlyList<GeoCheck>> GetAllAsync(
        string? machineId = null,
        string? type = null,
        DateTime? date = null,
        DateTime? startDate = null,
        DateTime? endDate = null,
        CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<GeoCheckFullEntity>().Get();
            var geoChecks = response.Models.Select(e => e.ToModel()).ToList();

            if (!string.IsNullOrWhiteSpace(machineId))
                geoChecks = geoChecks.Where(g => g.MachineId == machineId).ToList();
            if (!string.IsNullOrWhiteSpace(type))
                geoChecks = geoChecks.Where(g => g.Type == type).ToList();
            if (date.HasValue)
                geoChecks = geoChecks.Where(g => g.Date.Date == date.Value.Date).ToList();
            if (startDate.HasValue)
                geoChecks = geoChecks.Where(g => g.Date.Date >= startDate.Value.Date).ToList();
            if (endDate.HasValue)
                geoChecks = geoChecks.Where(g => g.Date.Date <= endDate.Value.Date).ToList();

            return geoChecks.OrderByDescending(g => g.Date).ThenBy(g => g.Type).ToList().AsReadOnly();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving geometry checks");
            throw;
        }
    }

    public async Task<GeoCheck?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<GeoCheckFullEntity>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id)
                .Get();
            return response.Models.FirstOrDefault()?.ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving geometry check {GeoCheckId}", id);
            return null;
        }
    }

    public async Task<GeoCheck> CreateAsync(GeoCheck geoCheck, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<GeoCheckEntity>().Insert(GeoCheckEntity.FromModel(geoCheck));
            return response.Models.First().ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating geometry check");
            throw;
        }
    }

    public async Task<bool> UpdateAsync(GeoCheck geoCheck, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var entity = GeoCheckEntity.FromModel(geoCheck);
            await _client.From<GeoCheckEntity>().Update(entity);
            return true;
        }
        catch (PostgrestException ex) when (ex.Message.Contains("no rows"))
        {
            _logger.LogWarning("Geometry check {GeoCheckId} not found for update", geoCheck.Id);
            return false;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating geometry check {GeoCheckId}", geoCheck.Id);
            throw;
        }
    }

    public async Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            await _client.From<GeoCheckEntity>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id)
                .Delete();
            return true;
        }
        catch (PostgrestException ex) when (ex.Message.Contains("no rows"))
        {
            _logger.LogWarning("Geometry check {GeoCheckId} not found for deletion", id);
            return false;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting geometry check {GeoCheckId}", id);
            throw;
        }
    }
}
