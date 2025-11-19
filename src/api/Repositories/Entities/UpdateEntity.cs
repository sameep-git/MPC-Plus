using Api.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace Api.Repositories.Entities;

[Table("updates")]
public class UpdateEntity : BaseModel
{
    [PrimaryKey("id", false)]
    [Column("id")]
    public string Id { get; set; } = string.Empty;

    [Column("machine")]
    public string Machine { get; set; } = string.Empty;

    [Column("info")]
    public string Info { get; set; } = string.Empty;

    [Column("type")]
    public string Type { get; set; } = string.Empty;

    public Update ToModel()
    {
        return new Update
        {
            Id = Id,
            Machine = Machine,
            Info = Info,
            Type = Type
        };
    }

    public static UpdateEntity FromModel(Update update)
    {
        return new UpdateEntity
        {
            Id = update.Id,
            Machine = update.Machine,
            Info = update.Info,
            Type = update.Type
        };
    }
}
