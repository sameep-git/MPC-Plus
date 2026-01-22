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
    private readonly IThresholdRepository _thresholdRepository;

    public SupabaseGeoCheckRepository(Client client, ILogger<SupabaseGeoCheckRepository> logger, IThresholdRepository thresholdRepository)
    {
        _client = client;
        _logger = logger;
        _thresholdRepository = thresholdRepository;
    }

    public async Task<IReadOnlyList<GeoCheck>> GetAllAsync(
        string? machineId = null,
        string? type = null,
        DateOnly? date = null,
        DateOnly? startDate = null,
        DateOnly? endDate = null,
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
                geoChecks = geoChecks.Where(g => g.Date == date.Value).ToList();
            if (startDate.HasValue)
                geoChecks = geoChecks.Where(g => g.Date >= startDate.Value).ToList();
            if (endDate.HasValue)
                geoChecks = geoChecks.Where(g => g.Date <= endDate.Value).ToList();

            // Populate Status
            var thresholds = (await _thresholdRepository.GetAllAsync()).ToList();
            foreach (var geo in geoChecks)
            {
                EvaluateGeoCheckStatus(geo, thresholds);
            }

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
                .Filter(nameof(GeoCheckFullEntity.Id), Supabase.Postgrest.Constants.Operator.Equals, id)
                .Get();
            var geoCheck = response.Models.FirstOrDefault()?.ToModel();
            
            if (geoCheck != null)
            {
                var thresholds = await _thresholdRepository.GetAllAsync();
                EvaluateGeoCheckStatus(geoCheck, thresholds);
            }

            return geoCheck;
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
                .Filter(nameof(GeoCheckEntity.Id), Supabase.Postgrest.Constants.Operator.Equals, id)
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

    private void EvaluateGeoCheckStatus(GeoCheck geo, IEnumerable<Threshold> thresholds)
    {
        bool isAnyFail = false;
        
        void Check(double? value, string metricType, string? key = null)
        {
            if (!value.HasValue) return;

            var threshold = thresholds.FirstOrDefault(t => 
                t.MachineId == geo.MachineId && 
                t.CheckType == "geometry" && 
                t.MetricType == metricType);
            
            if (threshold?.Value != null)
            {
                if (Math.Abs(value.Value) > threshold.Value)
                {
                    isAnyFail = true;
                    // If key is provided, we could store specific failure
                    if (key != null) geo.MetricStatuses[key] = "FAIL";
                }
            }
        }

        // IsoCenter
        Check(geo.IsoCenterSize, "Iso Center Size", "IsoCenterSize");
        Check(geo.IsoCenterMVOffset, "Iso Center MV Offset", "IsoCenterMVOffset");
        Check(geo.IsoCenterKVOffset, "Iso Center KV Offset", "IsoCenterKVOffset");
        
        // Couch
        Check(geo.CouchLat, "Couch Lat", "CouchLat");
        Check(geo.CouchLng, "Couch Lng", "CouchLng");
        Check(geo.CouchVrt, "Couch Vrt", "CouchVrt");
        Check(geo.CouchRtnFine, "Couch Rtn Fine", "CouchRtnFine");
        Check(geo.CouchRtnLarge, "Couch Rtn Large", "CouchRtnLarge");
        Check(geo.CouchMaxPositionError, "Max Position Error", "MaxPositionError");
        Check(geo.RotationInducedCouchShiftFullRange, "Rotation Induced Shift", "RotationInducedShift");

        // Gantry
        Check(geo.GantryAbsolute, "Gantry Absolute", "GantryAbsolute");
        Check(geo.GantryRelative, "Gantry Relative", "GantryRelative");

        // Collimation
        Check(geo.CollimationRotationOffset, "Collimation Rotation Offset", "CollimationRotationOffset");
        
        // MLC (Collections) - Simplified check for all values
        if (geo.MLCLeavesA != null)
        {
             foreach (var val in geo.MLCLeavesA.Values) Check(val, "MLC Leaf Position"); 
        }
        if (geo.MLCLeavesB != null)
        {
             foreach (var val in geo.MLCLeavesB.Values) Check(val, "MLC Leaf Position"); 
        }
        
        // MLC Offsets
        Check(geo.MeanOffsetA, "Mean Offset A", "MeanOffsetA");
        Check(geo.MaxOffsetA, "Max Offset A", "MaxOffsetA");
        Check(geo.MeanOffsetB, "Mean Offset B", "MeanOffsetB");
        Check(geo.MaxOffsetB, "Max Offset B", "MaxOffsetB");
        
        // Jaws
        Check(geo.JawX1, "Jaw X1", "JawX1");
        Check(geo.JawX2, "Jaw X2", "JawX2");
        Check(geo.JawY1, "Jaw Y1", "JawY1");
        Check(geo.JawY2, "Jaw Y2", "JawY2");
        
        // Parallelism
        Check(geo.JawParallelismX1, "Parallelism X1", "ParallelismX1");
        Check(geo.JawParallelismX2, "Parallelism X2", "ParallelismX2");
        Check(geo.JawParallelismY1, "Parallelism Y1", "ParallelismY1");
        Check(geo.JawParallelismY2, "Parallelism Y2", "ParallelismY2");

        geo.Status = isAnyFail ? "FAIL" : "PASS";
    }
}
