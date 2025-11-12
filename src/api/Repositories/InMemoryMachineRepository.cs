using System.Collections.Concurrent;
using Api.Models;

namespace Api.Repositories;

public class InMemoryMachineRepository : IMachineRepository
{
    private static readonly IReadOnlyList<Machine> SeedMachines = new[]
    {
        new Machine
        {
            Id = "MPC-001",
            Name = "Primary Gantry",
            Type = "Linear Accelerator",
            Location = "Room A"
        },
        new Machine
        {
            Id = "MPC-002",
            Name = "Secondary Gantry",
            Type = "Linear Accelerator",
            Location = "Room B"
        },
        new Machine
        {
            Id = "MPC-003",
            Name = "QA Test Bench",
            Type = "Diagnostic",
            Location = "Lab 1"
        }
    };

    private readonly ConcurrentDictionary<string, Machine> _machines;

    public InMemoryMachineRepository()
    {
        _machines = new ConcurrentDictionary<string, Machine>(
            SeedMachines.Select(machine => new KeyValuePair<string, Machine>(machine.Id, Clone(machine))));
    }

    public Task<IReadOnlyList<Machine>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var result = _machines.Values
            .Select(Clone)
            .OrderBy(machine => machine.Id)
            .ToList()
            .AsReadOnly();

        return Task.FromResult<IReadOnlyList<Machine>>(result);
    }

    public Task<Machine?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        return Task.FromResult(_machines.TryGetValue(id, out var machine) ? Clone(machine) : null);
    }

    public Task<Machine> CreateAsync(Machine machine, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        if (!_machines.TryAdd(machine.Id, Clone(machine)))
        {
            throw new InvalidOperationException($"Machine with id '{machine.Id}' already exists.");
        }

        return Task.FromResult(Clone(machine));
    }

    public Task<bool> UpdateAsync(Machine machine, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        if (!_machines.ContainsKey(machine.Id))
        {
            return Task.FromResult(false);
        }

        _machines[machine.Id] = Clone(machine);
        return Task.FromResult(true);
    }

    public Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        return Task.FromResult(_machines.TryRemove(id, out _));
    }

    private static Machine Clone(Machine machine) =>
        new()
        {
            Id = machine.Id,
            Location = machine.Location,
            Name = machine.Name,
            Type = machine.Type
        };
}

