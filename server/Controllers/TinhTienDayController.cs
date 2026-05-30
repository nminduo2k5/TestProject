using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class TinhTienDayController(IConfiguration configuration, AppDbContext context) : ControllerBase
{
  readonly AppDbContext context = context;
  readonly string connectionString = configuration.GetConnectionString("DefaultConnection")!;

  [HttpGet]
  public async Task<ActionResult> GetAsync()
  {
    using NpgsqlConnection conn = new(connectionString);
    await conn.OpenAsync();

    using var command = new NpgsqlCommand("""
SELECT 
	gv."Id",
	gv."MaGiangVien",
	gv."TenGiangVien",
	k."Id" MaKhoa,
	k."MaKhoa",
	k."TenKhoa",
	bc."MaBangCap",
	bc."TenBangCap",
	lhp."MaLop",
	lhp."TenLop",
	lhp."SoLuongSinhVien",
	hk."Id" MaHocKi,
	hk."ThoiGianBatDau",
	hk."ThoiGianKetThuc",
	CASE (
		SELECT hsbc."HeSo"
		FROM "HeSoBangCap" hsbc
		WHERE 
			hsbc."MaBangCap" = bc."Id" AND
			DATE_PART('year', hk."ThoiGianBatDau") = hsbc."Nam"
		LIMIT 1
	) IS NULL 
	WHEN TRUE THEN 1
	ELSE (
		SELECT hsbc."HeSo"
		FROM "HeSoBangCap" hsbc
		WHERE 
			hsbc."MaBangCap" = bc."Id" AND
			DATE_PART('year', hk."ThoiGianBatDau") = hsbc."Nam"
		LIMIT 1
	) END heSoBangCap,
  hp."Id" HocPhanId,
  hp."MaHocPhan",
  hp."TenHocPhan",
  hp."SoTiet",
  hp."SoTinChi",
  hp."HeSoHocPhan"
FROM "GiangVien" gv
INNER JOIN "LopHocPhan" lhp ON lhp."GiangVienId" = gv."Id"
INNER JOIN "BangCap" bc ON bc."Id" = gv."BangCapId"
INNER JOIN "Khoa_GiangVien" kgv ON kgv."GiangVienId" = gv."Id"
INNER JOIN "Khoa" k ON k."Id" = kgv."KhoaId"
INNER JOIN "HocKi" hk ON hk."Id" = lhp."HocKiId"
INNER JOIN "HocPhan" hp ON hp."Id" = lhp."HocPhanId"
ORDER BY hk."ThoiGianBatDau"
""", conn);
    using var reader = command.ExecuteReader();
    List<object> items = [];
    while (reader.Read())
    {
      items.Add(new
      {
        Id = reader.GetGuid(0),
        MaGiangVien = reader.GetString(1),
        TenGiangVien = reader.GetString(2),
        KhoaId = reader.GetGuid(3),
        MaKhoa = reader.GetString(4),
        TenKhoa = reader.GetString(5),
        MaBangCap = reader.GetString(6),
        TenBangCap = reader.GetString(7),
        MaLop = reader.GetString(8),
        TenLop = reader.GetString(9),
        SoLuongSinhVien = reader.GetInt32(10),
        MaHocKi = reader.GetGuid(11),
        ThoiGianBatDau = reader.GetDateTime(12),
        ThoiGianKetThuc = reader.GetDateTime(13),
        HeSoBangCap = reader.GetDouble(14),
        HocPhanId = reader.GetGuid(15),
        MaHocPhan = reader.GetString(16),
        TenHocPhan = reader.GetString(17),
        SoTiet = reader.GetInt32(18),
        SoTinChi = reader.GetInt32(19),
        HeSoHocPhan = reader.GetDouble(20)
      });
    }
    await conn.CloseAsync();

    return Ok(items);
  }

  [HttpGet("lay-danh-sach-dinh-muc")]
  public ActionResult GetDinhMuc()
  {
    var result =
      from dm in context.DinhMucTien
      orderby dm.NgayCapNhat descending
      select dm;

    return Ok(result.ToList());
  }

  [HttpGet("lay-danh-sach-he-so-lop-hoc-phan")]
  public ActionResult GetHeSoLopHocPhan()
  {
    var result =
      from hslhp in context.HeSoLop
      orderby hslhp.NamHoc descending, hslhp.SoHocSinhToiThieu ascending
      select hslhp;

    return Ok(result.ToList());
  }
}