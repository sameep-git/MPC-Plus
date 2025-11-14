using Api.Models;

namespace Api.Repositories.Abstractions;

/// <summary>
/// Repository interface for results data operations.
/// </summary>
public interface IResultsRepository
{
    /// <summary>
    /// Gets all results for a specific month and year.
    /// </summary>
    /// <param name="month">Month (1-12)</param>
    /// <param name="year">Year</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>List of results for the specified month and year</returns>
    Task<IReadOnlyList<Result>> GetByMonthAndYearAsync(
        int month,
        int year,
        CancellationToken cancellationToken = default);
}

