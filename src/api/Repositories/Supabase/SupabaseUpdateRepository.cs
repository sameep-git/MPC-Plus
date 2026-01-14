using Api.Models;
using Api.Repositories.Abstractions;
using Api.Repositories.Entities;
using Microsoft.Extensions.Logging;
using Supabase;
using Supabase.Postgrest.Exceptions;

namespace Api.Repositories;

public class SupabaseUpdateRepository : IUpdateRepository
{
    private readonly Client _client;
    private readonly ILogger<SupabaseUpdateRepository> _logger;

    public SupabaseUpdateRepository(Client client, ILogger<SupabaseUpdateRepository> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<IReadOnlyList<Update>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        try
        {
            var response = await _client
                .From<UpdateEntity>()
                .Get();

            return response.Models.Select(entity => entity.ToModel()).ToList();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving updates");
            throw;
        }
    }

    public async Task<Update?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        try
        {
            var response = await _client
                .From<UpdateEntity>()
                .Filter(nameof(UpdateEntity.Id), Supabase.Postgrest.Constants.Operator.Equals, id)
                .Get();

            return response.Models.FirstOrDefault()?.ToModel();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving update {UpdateId}", id);
            return null;
        }
    }

    public async Task<Update> CreateAsync(Update update, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var entity = UpdateEntity.FromModel(update);

        try
        {
            var response = await _client.From<UpdateEntity>().Insert(entity);
            var created = response.Models.FirstOrDefault();

            if (created is null)
            {
                _logger.LogWarning("Supabase insert returned no models for update {UpdateId}", update.Id);
                return update;
            }

            return created.ToModel();
        }
        catch (PostgrestException exception) when (IsUniqueConstraintViolation(exception))
        {
            throw new InvalidOperationException($"Update with id '{update.Id}' already exists.", exception);
        }
    }

    public async Task<bool> UpdateAsync(Update update, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var entity = UpdateEntity.FromModel(update);

        try
        {
            var response = await _client
                .From<UpdateEntity>()
                .Filter(nameof(UpdateEntity.Id), Supabase.Postgrest.Constants.Operator.Equals, update.Id)
                .Update(entity);

            return response.Models.Any();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating update {UpdateId}", update.Id);
            return false;
        }
    }

    public async Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        try
        {
            var existing = await GetByIdAsync(id, cancellationToken);
            if (existing is null)
            {
                return false;
            }

            await _client
                .From<UpdateEntity>()
                .Filter(nameof(UpdateEntity.Id), Supabase.Postgrest.Constants.Operator.Equals, id)
                .Delete();

            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting update {UpdateId}", id);
            return false;
        }
    }

    private static bool IsUniqueConstraintViolation(PostgrestException exception) =>
        exception.Message.Contains("duplicate key", StringComparison.OrdinalIgnoreCase);
}
