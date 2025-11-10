using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Api.Options;
using Microsoft.Extensions.Options;

namespace Api.Services;

/// <summary>
/// HTTP client wrapper for interacting with Supabase PostgREST endpoints.
/// </summary>
public class SupabaseRestClient : ISupabaseRestClient
{
    private static readonly JsonSerializerOptions SerializerOptions = new(JsonSerializerDefaults.Web)
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull,
    };

    private readonly HttpClient _httpClient;
    private readonly SupabaseOptions _options;

    public SupabaseRestClient(HttpClient httpClient, IOptions<SupabaseOptions> options)
    {
        _httpClient = httpClient;
        _options = options.Value;

        _httpClient.BaseAddress ??= new Uri(new Uri(_options.Url), "/rest/v1/");
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        _httpClient.DefaultRequestHeaders.Add("apikey", _options.ApiKey);
        _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _options.ApiKey);
        if (!string.IsNullOrWhiteSpace(_options.Schema))
        {
            _httpClient.DefaultRequestHeaders.Add("Accept-Profile", _options.Schema);
            _httpClient.DefaultRequestHeaders.Add("Content-Profile", _options.Schema);
        }
    }

    public async Task<IReadOnlyList<T>> GetListAsync<T>(string resource, string query, CancellationToken cancellationToken)
    {
        using var response = await _httpClient.GetAsync($"{resource}?{query}", cancellationToken);
        if (!response.IsSuccessStatusCode)
        {
            return Array.Empty<T>();
        }

        var stream = await response.Content.ReadAsStreamAsync(cancellationToken);
        var data = await JsonSerializer.DeserializeAsync<List<T>>(stream, SerializerOptions, cancellationToken);
        return data ?? new List<T>();
    }

    public async Task<T?> GetSingleAsync<T>(string resource, string query, CancellationToken cancellationToken)
    {
        var results = await GetListAsync<T>(resource, query, cancellationToken);
        return results.FirstOrDefault();
    }

    public async Task<bool> InsertAsync<T>(string resource, T payload, CancellationToken cancellationToken)
    {
        var content = SerializePayload(payload);
        using var response = await _httpClient.PostAsync(resource, content, cancellationToken);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> UpsertAsync<T>(string resource, T payload, string matchQuery, CancellationToken cancellationToken)
    {
        var request = new HttpRequestMessage(HttpMethod.Patch, $"{resource}?{matchQuery}")
        {
            Content = SerializePayload(payload),
        };
        request.Headers.Add("Prefer", "return=representation");

        using var response = await _httpClient.SendAsync(request, cancellationToken);
        return response.IsSuccessStatusCode;
    }

    public async Task<bool> DeleteAsync(string resource, string matchQuery, CancellationToken cancellationToken)
    {
        using var response = await _httpClient.DeleteAsync($"{resource}?{matchQuery}", cancellationToken);
        return response.IsSuccessStatusCode;
    }

    private static StringContent SerializePayload<T>(T payload)
    {
        var json = JsonSerializer.Serialize(payload, SerializerOptions);
        return new StringContent(json, Encoding.UTF8, "application/json");
    }
}

