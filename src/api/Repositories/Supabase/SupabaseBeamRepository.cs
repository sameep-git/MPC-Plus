using Api.Models;
using Api.Repositories.Abstractions;
using Api.Repositories.Entities;
using Microsoft.Extensions.Logging;
using Supabase;
using Supabase.Postgrest.Exceptions;

namespace Api.Repositories;

public class SupabaseBeamRepository : IBeamRepository
{
    private readonly Client _client;
    private readonly ILogger<SupabaseBeamRepository> _logger;
    private readonly IThresholdRepository _thresholdRepository;

    public SupabaseBeamRepository(Client client, ILogger<SupabaseBeamRepository> logger, IThresholdRepository thresholdRepository)
    {
        _client = client;
        _logger = logger;
        _thresholdRepository = thresholdRepository;
    }

    public async Task<IReadOnlyList<Beam>> GetAllAsync(
        string? machineId = null, string? type = null, DateOnly? date = null,
        DateOnly? startDate = null, DateOnly? endDate = null,
        CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<BeamEntity>().Get();
            var beams = response.Models.Select(e => e.ToModel()).ToList();
            
            if (!string.IsNullOrWhiteSpace(machineId))
                beams = beams.Where(b => b.MachineId == machineId).ToList();
            if (!string.IsNullOrWhiteSpace(type))
                beams = beams.Where(b => b.Type == type).ToList();
            if (date.HasValue)
                beams = beams.Where(b => b.Date == date.Value).ToList();
            if (startDate.HasValue)
                beams = beams.Where(b => b.Date >= startDate.Value).ToList();
            if (endDate.HasValue)
                beams = beams.Where(b => b.Date <= endDate.Value).ToList();

            // Populate Status
            var thresholds = (await _thresholdRepository.GetAllAsync()).ToList();
            foreach (var beam in beams)
            {
                EvaluateBeamStatus(beam, thresholds);
            }
            
            return beams.OrderByDescending(b => b.Date).ThenBy(b => b.Type).ToList().AsReadOnly();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving beams");
            throw;
        }
    }

    public async Task<Beam?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<BeamEntity>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id).Get();
            var beam = response.Models.FirstOrDefault()?.ToModel();
            
            if (beam != null)
            {
                var thresholds = await _thresholdRepository.GetAllAsync();
                EvaluateBeamStatus(beam, thresholds);
            }

            return beam;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving beam {BeamId}", id);
            return null;
        }
    }

    public async Task<Beam> CreateAsync(Beam beam, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<BeamEntity>().Insert(BeamEntity.FromModel(beam));
            return response.Models.First().ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating beam");
            throw;
        }
    }

    public async Task<bool> UpdateAsync(Beam beam, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client.From<BeamEntity>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, beam.Id)
                .Update(BeamEntity.FromModel(beam));
            return response.Models.Any();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating beam {BeamId}", beam.Id);
            return false;
        }
    }

    public async Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            await _client.From<BeamEntity>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id)
                .Delete();
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting beam {BeamId}", id);
            return false;
        }
    }

    public async Task<IReadOnlyList<string>> GetBeamTypesAsync(CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        var types = new[] { "2.5x", "6x", "6xFFF", "10x", "10xFFF", "15x", "6e", "9e", "12e", "16e" };
        return await Task.FromResult(types.ToList().AsReadOnly());
    }

    private void EvaluateBeamStatus(Beam beam, IEnumerable<Threshold> thresholds)
    {
        // Helper to check status
        string Check(double? value, string metricType)
        {
            if (!value.HasValue) return "PASS";
            
            // Find threshold
            // Priority: Specific variant > Generic
            var threshold = thresholds.FirstOrDefault(t => 
                t.MachineId == beam.MachineId && 
                t.CheckType == "beam" && 
                t.MetricType == metricType && 
                string.Equals(t.BeamVariant, beam.Type, StringComparison.OrdinalIgnoreCase)) 
            ?? thresholds.FirstOrDefault(t => 
                t.MachineId == beam.MachineId && 
                t.CheckType == "beam" && 
                t.MetricType == metricType && 
                string.IsNullOrEmpty(t.BeamVariant));

            if (threshold?.Value != null)
            {
                if (Math.Abs(value.Value) > threshold.Value) return "FAIL";
            }
            return "PASS";
        }

        beam.RelOutputStatus = Check(beam.RelOutput, "Relative Output");
        beam.RelUniformityStatus = Check(beam.RelUniformity, "Relative Uniformity");
        beam.CenterShiftStatus = Check(beam.CenterShift, "Center Shift");

        if (beam.RelOutputStatus == "FAIL" || beam.RelUniformityStatus == "FAIL" || beam.CenterShiftStatus == "FAIL")
        {
            beam.Status = "FAIL";
        }
        else
        {
            beam.Status = "PASS";
        }
    }
}
