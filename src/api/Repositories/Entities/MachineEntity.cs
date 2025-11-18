using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace Api.Repositories.Entities;

[Table("machines")]
public class MachineEntity : BaseModel
{
    [PrimaryKey("id", false)]
    public string Id { get; set; } = default!;

    [Column("location")]
    public string Location { get; set; } = default!;

    [Column("name")]
    public string Name { get; set; } = default!;

    [Column("type")]
    public string Type { get; set; } = default!;

    public static MachineEntity FromModel(Machine machine) =>
        new()
        {
            Id = machine.Id,
            Location = machine.Location,
            Name = machine.Name,
            Type = machine.Type
        };

    public Machine ToModel() =>
        new()
        {
            Id = Id,
            Location = Location,
            Name = Name,
            Type = Type
        };
}

