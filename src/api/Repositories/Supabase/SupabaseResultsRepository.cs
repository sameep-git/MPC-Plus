using Api.Models;
using Api.Repositories.Abstractions;
using Api.Repositories.Entities;
using Microsoft.Extensions.Logging;
using Supabase;

namespace Api.Repositories;

public class SupabaseResultsRepository : IResultsRepository
{
    private readonly Client _client;
    private readonly ILogger<SupabaseResultsRepository> _logger;

    public SupabaseResultsRepository(Client client, ILogger<SupabaseResultsRepository> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<IReadOnlyList<Result>> GetByMonthAndYearAsync(
        int month,
        int year,
        CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        try
        {
            var response = await _client
                .From<ResultEntity>()
                .Filter(nameof(ResultEntity.Month), Supabase.Postgrest.Constants.Operator.Equals, month)
                .Filter(nameof(ResultEntity.Year), Supabase.Postgrest.Constants.Operator.Equals, year)
                .Get();

            var results = response.Models
                .Select(e => e.ToModel())
                .OrderByDescending(r => r.Year)
                .ThenByDescending(r => r.Month)
                .ToList();

            return results.AsReadOnly();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving results for month {Month} and year {Year}", month, year);
            throw;
        }
    }
}

