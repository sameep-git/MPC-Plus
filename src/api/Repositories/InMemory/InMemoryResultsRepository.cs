using System.Collections.Concurrent;
using Api.Models;
using Api.Repositories.Abstractions;

namespace Api.Repositories.InMemory;

/// <summary>
/// In-memory implementation of the results repository with seed data.
/// Useful for development and testing.
/// </summary>
public class InMemoryResultsRepository : IResultsRepository
{
    private static readonly IReadOnlyList<Result> SeedResults =
    [
        new Result
        {
            Id = "result-001",
            Month = 9,
            Year = 2025,
            BeamCheck = new Dictionary<string, object?>
            {
                { "totalChecks", 15 },
                { "passedChecks", 14 },
                { "failedChecks", 1 },
                { "averageOutput", 98.5 },
                { "averageUniformity", 99.2 }
            },
            Status = "Good"
        },
        new Result
        {
            Id = "result-002",
            Month = 9,
            Year = 2025,
            BeamCheck = new Dictionary<string, object?>
            {
                { "totalChecks", 12 },
                { "passedChecks", 12 },
                { "failedChecks", 0 },
                { "averageOutput", 99.1 },
                { "averageUniformity", 99.4 }
            },
            Status = "Excellent"
        },
        new Result
        {
            Id = "result-003",
            Month = 8,
            Year = 2025,
            BeamCheck = new Dictionary<string, object?>
            {
                { "totalChecks", 18 },
                { "passedChecks", 17 },
                { "failedChecks", 1 },
                { "averageOutput", 97.8 },
                { "averageUniformity", 98.9 }
            },
            Status = "Good"
        },
        new Result
        {
            Id = "result-004",
            Month = 10,
            Year = 2025,
            BeamCheck = new Dictionary<string, object?>
            {
                { "totalChecks", 10 },
                { "passedChecks", 9 },
                { "failedChecks", 1 },
                { "averageOutput", 98.2 },
                { "averageUniformity", 99.0 }
            },
            Status = "Good"
        }
    ];

    private readonly ConcurrentDictionary<string, Result> _results;

    public InMemoryResultsRepository()
    {
        _results = new ConcurrentDictionary<string, Result>(
            SeedResults.Select(result => new KeyValuePair<string, Result>(result.Id, Clone(result))));
    }

    public Task<IReadOnlyList<Result>> GetByMonthAndYearAsync(
        int month,
        int year,
        CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var query = _results.Values.AsEnumerable()
            .Where(r => r.Month == month && r.Year == year);

        var result = query
            .Select(Clone)
            .OrderByDescending(r => r.Year)
            .ThenByDescending(r => r.Month)
            .ToList()
            .AsReadOnly();

        return Task.FromResult<IReadOnlyList<Result>>(result);
    }

    private static Result Clone(Result result)
    {
        IDictionary<string, object?>? beamCheck = null;
        if (result.BeamCheck != null)
        {
            beamCheck = new Dictionary<string, object?>(result.BeamCheck);
        }

        return new Result
        {
            Id = result.Id,
            Month = result.Month,
            Year = result.Year,
            BeamCheck = beamCheck,
            Status = result.Status
        };
    }
}

