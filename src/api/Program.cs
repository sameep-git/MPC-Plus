using Api.Extensions;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMachineDataAccess(builder.Configuration);
builder.Services.AddBeamDataAccess(builder.Configuration);
builder.Services.AddResultsDataAccess(builder.Configuration);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

app.MapControllers();

app.Run();
