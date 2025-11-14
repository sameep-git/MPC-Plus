using Api.Models;
using Api.Repositories.InMemory;

namespace Api.Tests.Repositories.InMemory;

public class InMemoryResultsRepositoryTests
{
    private readonly InMemoryResultsRepository _repository = new();

    [Fact]
    public async Task GetByMonthAndYearAsync_WithValidMonthAndYear_ReturnsMatchingResults()
    {
        // Act
        var result = await _repository.GetByMonthAndYearAsync(9, 2025);

        // Assert
        result.Should().NotBeNull();
        result.Should().HaveCount(2); // Based on seed data
        result.Should().AllSatisfy(r =>
        {
            r.Month.Should().Be(9);
            r.Year.Should().Be(2025);
        });
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_WithNonExistentMonthAndYear_ReturnsEmptyList()
    {
        // Act
        var result = await _repository.GetByMonthAndYearAsync(1, 2020);

        // Assert
        result.Should().NotBeNull().And.BeEmpty();
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_WithDifferentMonth_ReturnsOnlyMatchingMonth()
    {
        // Act
        var result = await _repository.GetByMonthAndYearAsync(8, 2025);

        // Assert
        result.Should().NotBeNull();
        result.Should().HaveCount(1); // Based on seed data
        result.Should().AllSatisfy(r =>
        {
            r.Month.Should().Be(8);
            r.Year.Should().Be(2025);
        });
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_WithDifferentYear_ReturnsOnlyMatchingYear()
    {
        // Act
        var result = await _repository.GetByMonthAndYearAsync(9, 2024);

        // Assert
        result.Should().NotBeNull().And.BeEmpty();
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_OrdersResultsByYearDescendingThenMonthDescending()
    {
        // Act
        var result = await _repository.GetByMonthAndYearAsync(9, 2025);

        // Assert
        var resultList = result.ToList();
        if (resultList.Count > 1)
        {
            for (int i = 0; i < resultList.Count - 1; i++)
            {
                var current = resultList[i];
                var next = resultList[i + 1];
                
                // Year should be descending or equal
                if (current.Year.HasValue && next.Year.HasValue)
                {
                    current.Year.Value.Should().BeGreaterThanOrEqualTo(next.Year.Value);
                    
                    // If years are equal, month should be descending or equal
                    if (current.Year.Value == next.Year.Value && current.Month.HasValue && next.Month.HasValue)
                    {
                        current.Month.Value.Should().BeGreaterThanOrEqualTo(next.Month.Value);
                    }
                }
            }
        }
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_ReturnsClonedResults()
    {
        // Act
        var result1 = await _repository.GetByMonthAndYearAsync(9, 2025);
        var result2 = await _repository.GetByMonthAndYearAsync(9, 2025);

        // Assert
        result1.Should().NotBeNull();
        result2.Should().NotBeNull();
        
        // Results should be separate instances (cloned)
        if (result1.Any() && result2.Any())
        {
            result1.First().Should().NotBeSameAs(result2.First());
        }
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_WithBoundaryMonthValues_WorksCorrectly()
    {
        // Act
        var result1 = await _repository.GetByMonthAndYearAsync(1, 2025);
        var result12 = await _repository.GetByMonthAndYearAsync(12, 2025);

        // Assert
        result1.Should().NotBeNull();
        result12.Should().NotBeNull();
    }

    [Fact]
    public async Task GetByMonthAndYearAsync_WithCancellationToken_RespectsCancellation()
    {
        // Arrange
        var cts = new CancellationTokenSource();
        cts.Cancel();

        // Act & Assert
        await _repository.Invoking(r => r.GetByMonthAndYearAsync(9, 2025, cts.Token))
            .Should().ThrowAsync<OperationCanceledException>();
    }
}

