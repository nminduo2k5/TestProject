using System.Collections;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Npgsql;
using server.Models;
using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class HocPhanController(AppDbContext context, IConfiguration configuration) : ControllerBase
{
  readonly AppDbContext context = context;
  readonly string connectionString = configuration.GetConnectionString("DefaultConnection")!;


  [HttpGet]
  public async Task<ActionResult<ICollection>> Get()
  {
    var result =
      from c in context.HocPhan
      join k in context.Khoa on c.KhoaId equals k.Id
      orderby c.MaHocPhan.Length, c.MaHocPhan
      select new
      {
        c.Id,
        c.MaHocPhan,
        c.TenHocPhan,
        c.HeSoHocPhan,
        c.SoTiet,
        c.SoTinChi,
        KhoaId = k.Id,
        k.TenKhoa,
        k.MaKhoa
      };
    return Ok(await result.ToListAsync());
  }

  [HttpGet("tinh-trang-hoc-phan")]
  public async Task<ActionResult> GetTheoThoiGianAsync()
  {
    using NpgsqlConnection conn = new(connectionString);
    await conn.OpenAsync();

    var query = """
SELECT 
  hp."Id",
  hp."MaHocPhan",
  hp."TenHocPhan",
  hp."SoTinChi",
  hp."HeSoHocPhan",
  hp."SoTiet",
  k."Id" KhoaId,
  k."TenKhoa",
  hk."Id" hocKiId,
  hk."ThoiGianBatDau",
  hk."ThoiGianKetThuc",
  COUNT(lhp."Id")
FROM "HocPhan" hp
INNER JOIN "Khoa" k ON k."Id" = hp."KhoaId"
LEFT JOIN "LopHocPhan" lhp ON lhp."HocPhanId" = hp."Id"
LEFT JOIN "HocKi" hk ON hk."Id" = lhp."HocKiId"
GROUP BY hp."Id", hk."Id", k."Id"
ORDER BY COUNT(lhp."Id")
""";
    using var cmd = new NpgsqlCommand(query, conn);
    using var reader = cmd.ExecuteReader();
    List<object> items = [];
    while (reader.Read())
    {
      bool isKyNull = reader.IsDBNull(10);
      items.Add(new
      {
        Id = reader.GetGuid(0),
        MaHocPhan = reader.GetString(1),
        TenHocPhan = reader.GetString(2),
        SoTinChi = reader.GetInt32(3),
        HeSoHocPhan = reader.GetDouble(4),
        SoTiet = reader.GetInt32(5),
        KhoaId = reader.GetGuid(6),
        TenKhoa = reader.GetString(7),
        HocKiId = isKyNull ? new Guid() : reader.GetGuid(8),
        ThoiGianBatDau = isKyNull ? new DateTime() : reader.GetDateTime(9),
        ThoiGianKetThuc = isKyNull ? new DateTime() : reader.GetDateTime(10),
        SoLopHocPhan = reader.GetInt32(11)
      });
    }
    await conn.CloseAsync();
    return Ok(items);
  }

  [HttpPut("sua-hoc-phan/{id}")]
  public async Task<IActionResult> Update(Guid id, HocPhanInput input)
  {
    HocPhan hocPhan = await context.HocPhan.FirstOrDefaultAsync(i => i.Id == id);
    if (hocPhan is null) return BadRequest("Không tìm thấy học phần!");

    hocPhan.TenHocPhan = input.TenHocPhan;
    hocPhan.HeSoHocPhan = input.HeSoHocPhan;
    hocPhan.SoTiet = input.SoTiet;
    hocPhan.SoTinChi = input.SoTinChi;

    await context.SaveChangesAsync();

    return Ok();
  }

  [HttpDelete]
  public IActionResult Delete(string id)
  {
    try
    {
      context.HocPhan.Remove(context.HocPhan.FirstOrDefault(i => i.Id.ToString() == id)!);
      context.SaveChanges();
    }
    catch (Exception)
    {
      throw new Exception("Không tìm thấy học phần!");
    }
    return Ok();
  }

  [HttpPost]
  public async Task<IActionResult> Create(HocPhanDto item)
  {
    HocPhan hocPhan = HocPhan.FormatInput(context, item);
    List<string> strings = [
      hocPhan.MaHocPhan,
      hocPhan.TenHocPhan,
      hocPhan.HeSoHocPhan.ToString(),
      hocPhan.KhoaId.ToString()
    ];
    if (strings.Any(string.IsNullOrEmpty)) return BadRequest("Nhập thiếu thông tin");

    if (await context.HocPhan.AnyAsync(c => c.TenHocPhan == item.TenHocPhan))
      return BadRequest("Tên học phần đã tồn tại");

    try
    {
      context.HocPhan.Add(hocPhan);
      await context.SaveChangesAsync();
    }
    catch (Exception)
    {
      throw new Exception("Thông tin không hợp lệ!");
    }

    return CreatedAtAction(nameof(Get), new { id = hocPhan.Id }, item);
  }
}

public class HocPhanInput
{
  public string TenHocPhan { get; set; } = null!;
  public int HeSoHocPhan { get; set; }
  public uint SoTinChi { get; set; } = 0!;
  public uint SoTiet { get; set; } = 0!;
  public Guid KhoaId { get; set; }
}