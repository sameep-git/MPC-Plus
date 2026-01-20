using Api.Models;

namespace Api.Repositories.Abstractions;

public interface IThresholdRepository
{
    Task<IEnumerable<Threshold>> GetAllAsync();
    Task<Threshold?> GetAsync(string machineId, string checkType, string metricType, string? beamVariant = null);
    Task<Threshold> UpsertAsync(Threshold threshold);
}
