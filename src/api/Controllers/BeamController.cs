using Api.Models;
using Api.Repositories.Abstractions;
using Microsoft.AspNetCore.Mvc;

namespace Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BeamController : ControllerBase
{
    private readonly IBeamRepository _repository;

    public BeamController(IBeamRepository repository)
    {
        _repository = repository;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Beam>>> GetAll(
        [FromQuery] string? type = null,
        [FromQuery] string? machineId = null,
        [FromQuery] string? date = null,
        [FromQuery] string? startDate = null,
        [FromQuery] string? endDate = null,
        CancellationToken cancellationToken = default)
    {
        DateOnly? dateOnly = null;
        if (!string.IsNullOrWhiteSpace(date))
            dateOnly = DateOnly.Parse(date);

        DateOnly? startDateOnly = null;
        if (!string.IsNullOrWhiteSpace(startDate))
            startDateOnly = DateOnly.Parse(startDate);

        DateOnly? endDateOnly = null;
        if (!string.IsNullOrWhiteSpace(endDate))
            endDateOnly = DateOnly.Parse(endDate);

        var beams = await _repository.GetAllAsync(
            machineId: machineId,
            type: type,
            date: dateOnly,
            startDate: startDateOnly,
            endDate: endDateOnly,
            cancellationToken: cancellationToken);

        return Ok(beams);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Beam>> GetById(string id, CancellationToken cancellationToken)
    {
        var beam = await _repository.GetByIdAsync(id, cancellationToken);
        if (beam is null)
        {
            return NotFound($"Beam with id '{id}' was not found.");
        }

        return Ok(beam);
    }

    [HttpPost]
    public async Task<ActionResult<Beam>> Create([FromBody] Beam beam, CancellationToken cancellationToken)
    {
        try
        {
            var created = await _repository.CreateAsync(beam, cancellationToken);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (InvalidOperationException exception)
        {
            return Conflict(exception.Message);
        }
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(string id, [FromBody] Beam beam, CancellationToken cancellationToken)
    {
        if (!string.Equals(id, beam.Id, StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest("The beam id in the route must match the payload.");
        }

        var updated = await _repository.UpdateAsync(beam, cancellationToken);
        if (!updated)
        {
            return NotFound($"Beam with id '{id}' was not found.");
        }

        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(string id, CancellationToken cancellationToken)
    {
        var deleted = await _repository.DeleteAsync(id, cancellationToken);
        if (!deleted)
        {
            return NotFound($"Beam with id '{id}' was not found.");
        }

        return NoContent();
    }

    [HttpGet("types")]
    public async Task<ActionResult<IEnumerable<string>>> GetBeamTypes(CancellationToken cancellationToken)
    {
        var types = await _repository.GetBeamTypesAsync(cancellationToken);
        return Ok(types);
    }
}
