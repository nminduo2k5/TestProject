using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace server.Repositories;

public interface IEntityPostgre
{
  Guid Id { get; set; }
}