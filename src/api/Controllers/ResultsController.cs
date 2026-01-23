using Api.Models;
using Api.Repositories.Abstractions;
using Microsoft.AspNetCore.Mvc;

namespace Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ResultsController : ControllerBase
{
    private readonly IBeamRepository _beamRepository;
    private readonly IGeoCheckRepository _geoCheckRepository;

    public ResultsController(IBeamRepository beamRepository, IGeoCheckRepository geoCheckRepository)
    {
        _beamRepository = beamRepository;
        _geoCheckRepository = geoCheckRepository;
    }

    [HttpGet]
    public async Task<ActionResult<MonthlyResults>> Get(
        [FromQuery] int month,
        [FromQuery] int year,
        [FromQuery] string machineId,
        CancellationToken cancellationToken = default)
    {
        // Validate month range (1-12)
        if (month < 1 || month > 12)
        {
            return BadRequest("Month must be between 1 and 12.");
        }

        // Validate year (reasonable range)
        if (year < 1900 || year > 2100)
        {
            return BadRequest("Year must be between 1900 and 2100.");
        }

        // Validate machineId
        if (string.IsNullOrWhiteSpace(machineId))
        {
            return BadRequest("MachineId is required.");
        }

        // Get all beam checks for this machine, month, and year
        var startDate = new DateTime(year, month, 1);
        var endDate = month == 12 
            ? new DateTime(year + 1, 1, 1).AddDays(-1).AddTicks(-1) // End of last day of month? Or just cover the day.
            // Actually Repositories usually check date equality or range. 
            // If we want the whole month, we should probably set time to end of day if time matters.
            // But let's stick to start of day for boundaries if repositories treat them inclusively?
            // The repositories use Date >= startDate and Date <= endDate.
            // To capture everything in the month, startDate should be YYYY-MM-01 00:00:00
            // endDate should be YYYY-MM-Last 23:59:59 OR YYYY-(M+1)-01 00:00:00 exclusive.
            // But the repository logic is: b.Date.Date >= startDate.Value.Date
            // and b.Date.Date <= endDate.Value.Date.
            // This compares just the dates. So using start of day is correct.
            : new DateTime(year, month + 1, 1).AddDays(-1);
        
        var beamChecks = await _beamRepository.GetAllAsync(
            machineId: machineId,
            startDate: startDate,
            endDate: endDate,
            cancellationToken: cancellationToken);

        var geoChecks = await _geoCheckRepository.GetAllAsync(
            machineId: machineId,
            startDate: startDate,
            endDate: endDate,
            cancellationToken: cancellationToken);

    // Group by date and aggregate status + example display values
    var dailyChecks = new Dictionary<DateOnly, (string? beamStatus, double? beamValue, string? geoStatus, double? geoValue)>();
        
        // Process beam checks
        foreach (var check in beamChecks)
        {
            var date = DateOnly.FromDateTime(check.Date);
            var status = DetermineCheckStatus(check);
            // derive a single numeric value for display (prefer RelOutput, then RelUniformity, then CenterShift)
            double? value = check.RelOutput ?? check.RelUniformity ?? check.CenterShift;

            if (dailyChecks.ContainsKey(date))
            {
                var (existingBeamStatus, existingBeamValue, geoStatus, geoValue) = dailyChecks[date];
                dailyChecks[date] = (AggregateStatuses(existingBeamStatus, status), existingBeamValue ?? value, geoStatus, geoValue);
            }
            else
            {
                dailyChecks[date] = (status, value, null, null);
            }
        }

        // Process geometry checks
        foreach (var check in geoChecks)
        {
            var date = DateOnly.FromDateTime(check.Date);
            var status = DetermineGeoCheckStatus(check);
            // derive a single numeric value for display (prefer RelativeOutput, then RelativeUniformity, then CenterShift, then IsoCenterSize)
            double? value = check.RelativeOutput ?? check.RelativeUniformity ?? check.CenterShift ?? check.IsoCenterSize;

            if (dailyChecks.ContainsKey(date))
            {
                var (beamStatus, beamValue, existingGeoStatus, existingGeoValue) = dailyChecks[date];
                dailyChecks[date] = (beamStatus, beamValue, AggregateStatuses(existingGeoStatus, status), existingGeoValue ?? value);
            }
            else
            {
                dailyChecks[date] = (null, null, status, value);
            }
        }

        var checks = dailyChecks
            .OrderBy(kvp => kvp.Key)
            .Select(kvp => new DayCheckStatus
            {
                Date = kvp.Key.ToDateTime(TimeOnly.MinValue),
                BeamCheckStatus = kvp.Value.beamStatus,
                GeometryCheckStatus = kvp.Value.geoStatus,
                BeamValue = kvp.Value.beamValue,
                GeometryValue = kvp.Value.geoValue
            })
            .ToList();

        var monthlyResults = new MonthlyResults
        {
            Month = month,
            Year = year,
            MachineId = machineId,
            Checks = checks.AsReadOnly()
        };

        return Ok(monthlyResults);
    }

    /// <summary>
    /// Determine the status of a single beam check based on pass criteria.
    /// </summary>
    private static string DetermineCheckStatus(Beam beam)
    {
        // TODO: Implement actual pass/warning/fail logic based on beam metrics
        // For now, return "pass" as default
        return "pass";
    }

    /// <summary>
    /// Determine the status of a geometry check based on pass criteria.
    /// </summary>
    private static string DetermineGeoCheckStatus(GeoCheck geoCheck)
    {
        // TODO: Implement actual pass/warning/fail logic based on geometry check metrics
        // For now, return "pass" as default
        return "pass";
    }

    /// <summary>
    /// Aggregate two statuses, returning the worse one.
    /// Hierarchy: fail > warning > pass
    /// </summary>
    private static string AggregateStatuses(string? status1, string? status2)
    {
        if (status1 == "fail" || status2 == "fail") return "fail";
        if (status1 == "warning" || status2 == "warning") return "warning";
        return "pass";
    }


}
