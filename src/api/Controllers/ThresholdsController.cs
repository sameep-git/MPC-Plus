using Api.Models;
using Api.Repositories.Abstractions;
using Microsoft.AspNetCore.Mvc;

namespace Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ThresholdsController : ControllerBase
{
    private readonly IThresholdRepository _repository;
    private readonly ILogger<ThresholdsController> _logger;

    public ThresholdsController(IThresholdRepository repository, ILogger<ThresholdsController> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    [HttpGet("all")]
    public async Task<IActionResult> GetAll()
    {
        try
        {
            var thresholds = await _repository.GetAllAsync();
            return Ok(thresholds);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting all thresholds");
            // Improve error details for debugging if needed, but 500 is standard
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet]
    public async Task<IActionResult> Get(
        [FromQuery] string machineId,
        [FromQuery] string checkType,
        [FromQuery] string metricType,
        [FromQuery] string? beamVariant = null)
    {
        if (string.IsNullOrWhiteSpace(machineId) || string.IsNullOrWhiteSpace(checkType) || string.IsNullOrWhiteSpace(metricType))
        {
            return BadRequest("machineId, checkType, and metricType are required parameters.");
        }

        try
        {
            var threshold = await _repository.GetAsync(machineId, checkType, metricType, beamVariant);
            if (threshold == null)
            {
                return NotFound("Threshold not found");
            }
            return Ok(threshold);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting threshold");
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpPost]
    public async Task<IActionResult> Upsert([FromBody] Threshold threshold)
    {
        if (threshold == null)
        {
            return BadRequest("Threshold cannot be null");
        }

        // Basic validation
        if (string.IsNullOrWhiteSpace(threshold.MachineId) || 
            string.IsNullOrWhiteSpace(threshold.CheckType) || 
            string.IsNullOrWhiteSpace(threshold.MetricType))
        {
            return BadRequest("Missing required fields (MachineId, CheckType, or MetricType)");
        }

        try
        {
            // Ensure timestamp is updated
            threshold.LastUpdated = DateTime.UtcNow;

            var result = await _repository.UpsertAsync(threshold);
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error saving threshold");
            return StatusCode(500, "Internal server error");
        }
    }
}
