using System.Collections;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class LopHocPhanThongKeController(AppDbContext context, IConfiguration configuration) : ControllerBase
{
  readonly AppDbContext context = context;
  readonly string conntectionString = configuration.GetConnectionString("DefaultConnection")!;

  [HttpGet("nam-hoc-ki")]
  public async Task<ActionResult> Get()
  {
    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT DATE_PART('year', h."ThoiGianBatDau") namHoc, COUNT(h."Id") soLuong
FROM "HocKi" h
GROUP BY DATE_PART('year', h."ThoiGianBatDau")
ORDER BY namHoc DESC
""";

    List<object> nam = [];
    using var cmd = new NpgsqlCommand(query, conn);
    using var reader = cmd.ExecuteReader();
    while (reader.Read())
    {
      nam.Add(new
      {
        Nam = reader.GetDouble(0),
        SoLuong = reader.GetDouble(1)
      });
    }
    await conn.CloseAsync();

    return Ok(nam);
  }

  [HttpGet("thong-ke-khoa")]
  public async Task<ActionResult> ThongKeKhoa()
  {
    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT 
	k."Id",
	k."MaKhoa",
	k."TenKhoa",
	k."TenVietTat",
	COUNT(DISTINCT hp."Id") soHocPhan,
	COUNT(DISTINCT lhp."Id") soLopHocPhan,
	SUM(lhp."SoLuongSinhVien") tongSoSinhVien,
	AVG(lhp."SoLuongSinhVien") trungBinhSinhVienLop
FROM "Khoa" k
LEFT JOIN "HocPhan" hp ON hp."KhoaId" = k."Id"
LEFT JOIN "LopHocPhan" lhp ON lhp."HocPhanId" = hp."Id"
GROUP BY k."Id";
""";
    List<object> result = [];
    using var cmd = new NpgsqlCommand(query, conn);
    using var reader = cmd.ExecuteReader();
    while (reader.Read())
    {
      result.Add(new
      {
        Id = reader.GetGuid(0),
        MaKhoa = reader.GetString(1),
        TenKhoa = reader.GetString(2),
        TenVietTat = reader.GetString(3),
        SoHocPhan = reader.GetInt32(4),
        SoLopHocPhan = reader.GetInt32(5),
        TongSoSinhVien = reader.IsDBNull(6) ? 0 : reader.GetInt32(6),
        TrungBinhSinhVienLop = reader.IsDBNull(7) ? 0 : reader.GetDouble(7)
      });
    }
    await conn.CloseAsync();

    return Ok(result);
  }

  [HttpGet("thong-ke-hoc-phan")]
  public async Task<ActionResult> ThongKeHocPhan(DateTime? dateTime)
  {
    dateTime ??= DateTime.MinValue;

    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT 
	hp."Id",
	hp."MaHocPhan",
	hp."TenHocPhan",
  k."Id" khoaId,
	k."MaKhoa",
	k."TenKhoa", 
	k."TenVietTat",
	COUNT(DISTINCT lhp."Id") soLopHocPhan,
	SUM(DISTINCT lhp."SoLuongSinhVien") tongSinhVien,
	AVG(DISTINCT lhp."SoLuongSinhVien") trungBinhSinhVienLop
FROM "HocPhan" hp
LEFT JOIN "LopHocPhan" lhp ON lhp."HocPhanId" = hp."Id"
INNER JOIN "HocKi" hk ON hk."Id" = lhp."HocKiId"
INNER JOIN "Khoa" k ON k."Id" = hp."KhoaId"
WHERE hk."ThoiGianBatDau" >= @fromDatefromDate
GROUP BY hp."Id", k."Id"
ORDER BY k."Id";
""";
    List<object> result = [];
    using var cmd = new NpgsqlCommand(query, conn);
    cmd.Parameters.AddWithValue("fromDatefromDate", dateTime);
    using var reader = cmd.ExecuteReader();
    while (reader.Read())
    {
      result.Add(new
      {
        Id = reader.GetGuid(0),
        MaHocPhan = reader.GetString(1),
        TenHocPhan = reader.GetString(2),
        KhoaId = reader.GetGuid(3),
        MaKhoa = reader.GetString(4),
        TenKhoa = reader.GetString(5),
        TenVietTat = reader.GetString(6),
        SoLopHocPhan = reader.GetInt32(7),
        TongSinhVien = reader.IsDBNull(8) ? 0 : reader.GetInt32(8),
        TrungBinhSinhVienLop = reader.IsDBNull(9) ? 0 : reader.GetDouble(9)
      });
    }
    await conn.CloseAsync();

    return Ok(result);
  }

  [HttpGet("thong-ke-hoc-ki")]
  public async Task<ActionResult> ThongKeHocPhan(Guid hocKi)
  {
    using var conn = new NpgsqlConnection(conntectionString);
    await conn.OpenAsync();

    string query = """
SELECT 
	hp."Id",
	hp."MaHocPhan",
	hp."TenHocPhan",
  k."Id" khoaId,
	k."MaKhoa",
	k."TenKhoa", 
	k."TenVietTat",
	COUNT(DISTINCT lhp."Id") soLopHocPhan,
	SUM(DISTINCT lhp."SoLuongSinhVien") tongSinhVien,
	AVG(DISTINCT lhp."SoLuongSinhVien") trungBinhSinhVienLop
FROM "HocPhan" hp
LEFT JOIN "LopHocPhan" lhp ON lhp."HocPhanId" = hp."Id"
RIGHT JOIN "HocKi" hk ON hk."Id" = lhp."HocKiId"
INNER JOIN "Khoa" k ON k."Id" = hp."KhoaId"
WHERE hk."Id" = @hocki
GROUP BY hp."Id", k."Id"
ORDER BY k."Id";
""";
    using var cmd = new NpgsqlCommand(query, conn);
    cmd.Parameters.AddWithValue("hocki", hocKi);

    List<object> result = [];
    using var reader = cmd.ExecuteReader();
    while (reader.Read())
    {
      result.Add(new
      {
        Id = reader.GetGuid(0),
        MaHocPhan = reader.GetString(1),
        TenHocPhan = reader.GetString(2),
        KhoaId = reader.GetGuid(3),
        MaKhoa = reader.GetString(4),
        TenKhoa = reader.GetString(5),
        TenVietTat = reader.GetString(6),
        SoLopHocPhan = reader.GetInt32(7),
        TongSinhVien = reader.IsDBNull(8) ? 0 : reader.GetInt32(8),
        TrungBinhSinhVienLop = reader.IsDBNull(9) ? 0 : reader.GetDouble(9)
      });
    }
    await conn.CloseAsync();

    return Ok(result);
  }
}