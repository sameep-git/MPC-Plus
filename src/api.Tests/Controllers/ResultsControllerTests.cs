using Api.Controllers;
using Api.Models;
using Api.Repositories.Abstractions;
using Microsoft.AspNetCore.Mvc;

namespace Api.Tests.Controllers;

public class ResultsControllerTests
{
    private readonly Mock<IResultsRepository> _mockRepository;
    private readonly ResultsController _controller;

    public ResultsControllerTests()
    {
        _mockRepository = new Mock<IResultsRepository>();
        _controller = new ResultsController(_mockRepository.Object);
    }

    [Fact]
    public async Task Get_WithValidMonthAndYear_ReturnsOkWithResults()
    {
        // Arrange
        var results = new List<Result>
        {
            new()
            {
                Id = "result-001",
                Month = 9,
                Year = 2025,
                BeamCheck = new Dictionary<string, object?>
                {
                    { "totalChecks", 15 },
                    { "passedChecks", 14 }
                },
                Status = "Good"
            },
            new()
            {
                Id = "result-002",
                Month = 9,
                Year = 2025,
                BeamCheck = new Dictionary<string, object?>
                {
                    { "totalChecks", 12 },
                    { "passedChecks", 12 }
                },
                Status = "Excellent"
            }
        };
        _mockRepository.Setup(r => r.GetByMonthAndYearAsync(9, 2025, It.IsAny<CancellationToken>()))
            .ReturnsAsync(results);

        // Act
        var result = await _controller.Get(9, 2025, CancellationToken.None);

        // Assert
        var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
        var returnedResults = okResult.Value.Should().BeAssignableTo<IEnumerable<Result>>().Subject;
        returnedResults.Should().HaveCount(2);
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(9, 2025, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task Get_WithMonthLessThanOne_ReturnsBadRequest()
    {
        // Act
        var result = await _controller.Get(0, 2025, CancellationToken.None);

        // Assert
        result.Result.Should().BeOfType<BadRequestObjectResult>();
        var badRequest = result.Result as BadRequestObjectResult;
        badRequest!.Value.Should().Be("Month must be between 1 and 12.");
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(It.IsAny<int>(), It.IsAny<int>(), It.IsAny<CancellationToken>()), Times.Never);
    }

    [Fact]
    public async Task Get_WithMonthGreaterThanTwelve_ReturnsBadRequest()
    {
        // Act
        var result = await _controller.Get(13, 2025, CancellationToken.None);

        // Assert
        result.Result.Should().BeOfType<BadRequestObjectResult>();
        var badRequest = result.Result as BadRequestObjectResult;
        badRequest!.Value.Should().Be("Month must be between 1 and 12.");
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(It.IsAny<int>(), It.IsAny<int>(), It.IsAny<CancellationToken>()), Times.Never);
    }

    [Fact]
    public async Task Get_WithYearLessThan1900_ReturnsBadRequest()
    {
        // Act
        var result = await _controller.Get(9, 1899, CancellationToken.None);

        // Assert
        result.Result.Should().BeOfType<BadRequestObjectResult>();
        var badRequest = result.Result as BadRequestObjectResult;
        badRequest!.Value.Should().Be("Year must be between 1900 and 2100.");
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(It.IsAny<int>(), It.IsAny<int>(), It.IsAny<CancellationToken>()), Times.Never);
    }

    [Fact]
    public async Task Get_WithYearGreaterThan2100_ReturnsBadRequest()
    {
        // Act
        var result = await _controller.Get(9, 2101, CancellationToken.None);

        // Assert
        result.Result.Should().BeOfType<BadRequestObjectResult>();
        var badRequest = result.Result as BadRequestObjectResult;
        badRequest!.Value.Should().Be("Year must be between 1900 and 2100.");
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(It.IsAny<int>(), It.IsAny<int>(), It.IsAny<CancellationToken>()), Times.Never);
    }

    [Fact]
    public async Task Get_WithValidBoundaryValues_ReturnsOk()
    {
        // Arrange
        var results = new List<Result>();
        _mockRepository.Setup(r => r.GetByMonthAndYearAsync(1, 1900, It.IsAny<CancellationToken>()))
            .ReturnsAsync(results);
        _mockRepository.Setup(r => r.GetByMonthAndYearAsync(12, 2100, It.IsAny<CancellationToken>()))
            .ReturnsAsync(results);

        // Act
        var result1 = await _controller.Get(1, 1900, CancellationToken.None);
        var result2 = await _controller.Get(12, 2100, CancellationToken.None);

        // Assert
        result1.Result.Should().BeOfType<OkObjectResult>();
        result2.Result.Should().BeOfType<OkObjectResult>();
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(1, 1900, It.IsAny<CancellationToken>()), Times.Once);
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(12, 2100, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task Get_WithNoResults_ReturnsOkWithEmptyList()
    {
        // Arrange
        var emptyResults = new List<Result>();
        _mockRepository.Setup(r => r.GetByMonthAndYearAsync(6, 2024, It.IsAny<CancellationToken>()))
            .ReturnsAsync(emptyResults);

        // Act
        var result = await _controller.Get(6, 2024, CancellationToken.None);

        // Assert
        var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
        var returnedResults = okResult.Value.Should().BeAssignableTo<IEnumerable<Result>>().Subject;
        returnedResults.Should().BeEmpty();
    }

    [Fact]
    public async Task Get_WithValidParameters_PassesCorrectValuesToRepository()
    {
        // Arrange
        var results = new List<Result>();
        _mockRepository.Setup(r => r.GetByMonthAndYearAsync(9, 2025, It.IsAny<CancellationToken>()))
            .ReturnsAsync(results);

        // Act
        await _controller.Get(9, 2025, CancellationToken.None);

        // Assert
        _mockRepository.Verify(r => r.GetByMonthAndYearAsync(9, 2025, It.IsAny<CancellationToken>()), Times.Once);
    }
}

