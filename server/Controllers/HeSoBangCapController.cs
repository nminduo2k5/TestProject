using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Npgsql;
using NpgsqlTypes;
using server.Models;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class HeSoBangCapController(AppDbContext context, IConfiguration configuration) : ControllerBase
{
  readonly AppDbContext context = context;
  readonly string conntectionString = configuration.GetConnectionString("DefaultConnection")!;

  [HttpGet]
  public async Task<ActionResult> Get()
  {
    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT 
	hsbc."Id",
	bc."Id" bangCapId,
	bc."MaBangCap", 
	bc."TenBangCap",
	bc."TenVietTat",
	hsbc."HeSo", 
	hsbc."Nam"
FROM "HeSoBangCap" hsbc
INNER JOIN "BangCap" bc ON bc."Id" = hsbc."MaBangCap"
ORDER BY hsbc."Nam";
""";
    using var cmd = new NpgsqlCommand(query, conn);
    using var reader = cmd.ExecuteReader();

    List<object> items = [];
    while (reader.Read())
    {
      bool isNull = reader.IsDBNull(0);
      items.Add(new
      {
        id = isNull ? new Guid() : reader!.GetGuid(0),
        bangCapId = reader.GetGuid(1),
        maBangCap = reader.GetString(2),
        tenBangCap = reader.GetString(3),
        tenBangCapVietTat = reader.GetString(4),
        heSo = reader.IsDBNull(5) ? -1 : reader.GetDouble(5),
        nam = reader.IsDBNull(6) ? -1 : reader.GetDouble(6)
      });
    }
    return Ok(items);
  }
  [HttpGet("{year}")]
  public async Task<ActionResult> GetByYear(uint year)
  {
    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT * 
FROM "BangCap" bc 
WHERE NOT bc."Id" IN (
	SELECT bc."Id"
	FROM "HeSoBangCap" hsbc
	INNER JOIN "BangCap" bc ON bc."Id" = hsbc."MaBangCap"
	WHERE hsbc."Nam" = @nam
	ORDER BY hsbc."Nam"
);
""";

    using var cmd = new NpgsqlCommand(query, conn);
    cmd.Parameters.Add("nam", NpgsqlDbType.Bigint).Value = (long)year;
    using var reader = await cmd.ExecuteReaderAsync();

    List<HeSoBangCap> items2 = [];
    while (reader.Read())
    {
      items2.Add(new HeSoBangCap
      {
        MaBangCap = reader.GetGuid(0),
        HeSo = 1.0,
        Nam = year
      });
    }
    await context.HeSoBangCap.AddRangeAsync(items2);
    await context.SaveChangesAsync();

    string query2 = """
SELECT 
	hsbc."Id",
	bc."Id" bangCapId,
	bc."MaBangCap", 
	bc."TenBangCap",
	bc."TenVietTat",
	hsbc."HeSo", 
	hsbc."Nam"
FROM "HeSoBangCap" hsbc
INNER JOIN "BangCap" bc ON bc."Id" = hsbc."MaBangCap"
WHERE hsbc."Nam" = @nam 
ORDER BY hsbc."Nam", hsbc."HeSo";;
""";

    List<object> items = [];
    using var conn2 = new NpgsqlConnection(conntectionString);
    await conn2.OpenAsync();
    using var cmd2 = new NpgsqlCommand(query2, conn2);
    cmd2.Parameters.Add("nam", NpgsqlDbType.Bigint).Value = (long)year;
    using var reader2 = cmd2.ExecuteReader();

    while (reader2.Read())
    {
      bool isNull = reader2.IsDBNull(0);
      items.Add(new
      {
        id = isNull ? new Guid() : reader2!.GetGuid(0),
        bangCapId = reader2.GetGuid(1),
        maBangCap = reader2.GetString(2),
        tenBangCap = reader2.GetString(3),
        tenBangCapVietTat = reader2.GetString(4),
        heSo = reader2.IsDBNull(5) ? -1 : reader2.GetDouble(5),
        nam = reader2.IsDBNull(6) ? -1 : reader2.GetDouble(6)
      });
    }

    return Ok(items);
  }

  [HttpPost]
  public ActionResult Post(HeSoBangCapInput input)
  {
    HeSoBangCap? t = context.HeSoBangCap.Where(i => i.MaBangCap == input.MaBangCap && i.Nam == input.Nam).FirstOrDefault();
    if (t == null)
    {
      HeSoBangCap heSoBangCap = new()
      {
        MaBangCap = input.MaBangCap,
        HeSo = input.HeSo,
        Nam = input.Nam
      };

      context.HeSoBangCap.Add(heSoBangCap);
      context.SaveChanges();

      return Ok(heSoBangCap);
    }
    t.HeSo = input.HeSo;
    context.SaveChanges();
    return Ok();
  }

  [HttpPut]
  public ActionResult Put(HeSoBangCapInput input)
  {
    HeSoBangCap? bc = context.HeSoBangCap.Find(input.Id);
    if (bc is null) return NotFound();

    bc.HeSo = input.HeSo;
    context.SaveChanges();

    return Ok();
  }

  [HttpDelete("{id}")]
  public ActionResult Delete(Guid id)
  {
    HeSoBangCap? bc = context.HeSoBangCap.Find(id);
    if (bc is null) return NotFound();

    context.HeSoBangCap.Remove(bc);
    context.SaveChanges();

    return NoContent();
  }
}

public record HeSoBangCapInput
{
  public Guid? Id { get; set; }
  public double HeSo { get; set; } = 1.0;
  public uint Nam { get; set; }

  public Guid MaBangCap { get; set; }
}