using Api.Models;
using Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Api.Controllers;

[ApiController]
[Route("machines")]
public class MachinesController : ControllerBase
{
    private readonly IMachineRepository _repository;

    public MachinesController(IMachineRepository repository)
    {
        _repository = repository;
    }

    /// <summary>Returns a list of all machines.</summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<Machine>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<Machine>>> GetMachines(CancellationToken cancellationToken)
    {
        var machines = await _repository.GetAllAsync(cancellationToken);
        return Ok(machines);
    }

    /// <summary>Creates a new machine record.</summary>
    [HttpPost]
    [ProducesResponseType(typeof(Machine), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<Machine>> CreateMachine([FromBody] Machine machine, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var existing = await _repository.GetByIdAsync(machine.Id, cancellationToken);
        if (existing is not null)
        {
            return Conflict($"Machine with id '{machine.Id}' already exists.");
        }

        var created = await _repository.CreateAsync(machine, cancellationToken);
        if (!created)
        {
            return StatusCode(StatusCodes.Status502BadGateway, "Failed to persist machine.");
        }

        return CreatedAtAction(nameof(GetMachineById), new { machineId = machine.Id }, machine);
    }

    /// <summary>Returns details for a specific machine.</summary>
    [HttpGet("{machineId}")]
    [ProducesResponseType(typeof(Machine), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<Machine>> GetMachineById(string machineId, CancellationToken cancellationToken)
    {
        var machine = await _repository.GetByIdAsync(machineId, cancellationToken);
        return machine is null ? NotFound() : Ok(machine);
    }

    /// <summary>Updates an existing machine.</summary>
    [HttpPut("{machineId}")]
    [ProducesResponseType(typeof(Machine), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<Machine>> UpdateMachine(string machineId, [FromBody] Machine machine, CancellationToken cancellationToken)
    {
        if (!string.Equals(machineId, machine.Id, StringComparison.OrdinalIgnoreCase))
        {
            ModelState.AddModelError(nameof(machine.Id), "Machine ID in path and payload must match.");
            return ValidationProblem(ModelState);
        }

        var existing = await _repository.GetByIdAsync(machineId, cancellationToken);
        if (existing is null)
        {
            return NotFound();
        }

        var success = await _repository.UpdateAsync(machine, cancellationToken);
        if (!success)
        {
            return StatusCode(StatusCodes.Status502BadGateway, "Failed to update machine.");
        }

        return Ok(machine);
    }

    /// <summary>Deletes a machine.</summary>
    [HttpDelete("{machineId}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteMachine(string machineId, CancellationToken cancellationToken)
    {
        var deleted = await _repository.DeleteAsync(machineId, cancellationToken);
        return deleted ? NoContent() : NotFound();
    }
}

