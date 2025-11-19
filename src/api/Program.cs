using Api.Extensions;
using DotNetEnv;

// Load environment variables from .env file
Env.Load();

var builder = WebApplication.CreateBuilder(args);

// Override configuration with environment variables
var supabaseUrl = Environment.GetEnvironmentVariable("SUPABASE_URL");
var supabaseKey = Environment.GetEnvironmentVariable("SUPABASE_KEY");

Console.WriteLine($"[DEBUG] SUPABASE_URL: {supabaseUrl}");
Console.WriteLine($"[DEBUG] SUPABASE_KEY: {(string.IsNullOrWhiteSpace(supabaseKey) ? "EMPTY" : "SET")}");

builder.Configuration["Supabase:Url"] = supabaseUrl;
builder.Configuration["Supabase:Key"] = supabaseKey;

builder.Services.AddMachineDataAccess(builder.Configuration);
builder.Services.AddBeamDataAccess(builder.Configuration);
builder.Services.AddUpdateDataAccess(builder.Configuration);
builder.Services.AddGeoCheckDataAccess(builder.Configuration);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddOpenApi();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });   
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

app.UseCors("AllowFrontend");

app.MapControllers();

app.Run();
