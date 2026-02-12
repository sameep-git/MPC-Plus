# Use Microsoft's official .NET SDK image to build the app
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY ["api.csproj", "./"]
RUN dotnet restore "api.csproj"

# Copy everything else and build
COPY . .
RUN dotnet publish "api.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build /app/publish .

# Expose port 8080 (default for .NET 8/9 containers)
EXPOSE 8080

# Run the app
ENTRYPOINT ["dotnet", "api.dll"]