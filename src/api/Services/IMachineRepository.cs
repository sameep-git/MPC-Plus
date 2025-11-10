using Api.Models;

namespace Api.Services;

/// <summary>
/// Contract for machine persistence operations.
/// </summary>
public interface IMachineRepository
{
    Task<IReadOnlyList<Machine>> GetAllAsync(CancellationToken cancellationToken = default);

    Task<Machine?> GetByIdAsync(string id, CancellationToken cancellationToken = default);

    Task<bool> CreateAsync(Machine machine, CancellationToken cancellationToken = default);

    Task<bool> UpdateAsync(Machine machine, CancellationToken cancellationToken = default);

    Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default);
}

