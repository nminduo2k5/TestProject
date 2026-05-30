using System.Collections;
using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using Npgsql;
using server.Models;
using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class GiangVienController(
  IRepository<GiangVien> repo,
  IRepository<BangCap> bangCapRepository,
  IRepository<Khoa_GiangVien> k_gvRepository,
  AppDbContext context,
  IConfiguration configuration) : TemplatePostgreController<GiangVien, GiangVienDto>(repo)
{
  readonly string _connection = configuration.GetConnectionString("DefaultConnection")!;
  readonly IRepository<BangCap> _bangCapRepository = bangCapRepository;
  readonly IRepository<Khoa_GiangVien> _k_gvRepository = k_gvRepository;
  readonly AppDbContext _ct = context;

  [HttpGet("/thong-ke-giao-vien")]
  public async Task<ActionResult> GetKhoa()
  {
    using var conn = new NpgsqlConnection(_connection);
    await conn.OpenAsync();

    string bangCapQuery = """
SELECT
	K."MaKhoa",
	K."TenKhoa",
	B."MaBangCap",
	B."TenBangCap",
	COUNT(G."Id") SOGIAOVIEN
FROM
	"GiangVien" G
	LEFT JOIN "BangCap" B ON B."Id" = G."BangCapId"
	INNER JOIN "Khoa_GiangVien" KG ON G."Id" = KG."GiangVienId"
	LEFT JOIN "Khoa" K ON K."Id" = KG."KhoaId"
GROUP BY
	K."Id",
	B."Id"
ORDER BY
	LENGTH(K."MaKhoa"),
	K."MaKhoa",
	LENGTH(B."MaBangCap"),
	B."MaBangCap";

SELECT
	K."MaKhoa",
	K."TenVietTat" TenKhoa,
	G."GioiTinh",
	CASE
		WHEN G."GioiTinh" = 0 THEN 'Nam'
		ELSE 'Nữ'
	END,
	COUNT(G."Id")
FROM
	"GiangVien" G
	INNER JOIN "Khoa_GiangVien" KG ON KG."GiangVienId" = G."Id"
	RIGHT JOIN "Khoa" K ON K."Id" = KG."KhoaId"
GROUP BY
	K."Id",
	G."GioiTinh"
ORDER BY
	LENGTH(K."MaKhoa"),
	K."MaKhoa";

SELECT
	K."MaKhoa",
	K."TenKhoa",
	K."TenVietTat"
FROM
	"Khoa" K;

SELECT
	B."MaBangCap",
	B."TenBangCap",
	B."TenVietTat"
FROM
	"BangCap" B;
""";
    List<object> user = [];
    using var cmd = new NpgsqlCommand(bangCapQuery, conn);
    using var reader = cmd.ExecuteReader();
    while (reader.Read())
    {
      user.Add(new
      {
        MaKhoa = reader.GetString(0),
        TenKhoa = reader.GetString(1),
        MaBangCap = reader.GetString(2),
        TenBangCap = reader.GetString(3),
        SoGiangVien = reader.GetInt32(4)
      });
    }

    List<object> user2 = [];
    await reader.NextResultAsync();
    while (reader.Read())
    {
      user2.Add(new
      {
        MaKhoa = reader.GetString(0),
        TenKhoa = reader.GetString(1),
        GioiTinh = reader.IsDBNull(2) ? 0 : reader.GetInt32(2),
        GioiTinhText = reader.GetString(3),
        SoGiangVien = reader.GetInt32(4)
      });
    }

    List<object> khoa = [];
    await reader.NextResultAsync();
    while (reader.Read())
    {
      khoa.Add(new
      {
        MaKhoa = reader.GetString(0),
        TenKhoa = reader.GetString(1),
        TenVietTat = reader.GetString(2),
      });
    }

    List<object> bangCap = [];
    await reader.NextResultAsync();
    while (reader.Read())
    {
      bangCap.Add(new
      {
        MaBangCap = reader.GetString(0),
        TenBangCap = reader.GetString(1),
        TenVietTat = reader.GetString(2)
      });
    }
    await conn.CloseAsync();

    return Ok(new { BangCap = user, GioiTinh = user2, KhoaList = khoa, BangCapList = bangCap });
  }

  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get()
  {
    var result =
    from g in _ct.GiangVien
    join b in _ct.BangCap on g.BangCapId equals b.Id
    join kgv in _ct.Khoa_GiangVien on g.Id equals kgv.GiangVienId
    join k in _ct.Khoa on kgv.KhoaId equals k.Id
    join c in _ct.ChucVu on kgv.ChucVuId equals c.Id
    orderby g.MaGiangVien.Length, g.MaGiangVien
    select new
    {
      g.Id,
      g.MaGiangVien,
      g.TenGiangVien,
      GioiTinh = g.GioiTinh == 0 ? "Nam" : "Nữ",
      g.SinhNhat,
      g.SoDienThoai,
      g.Mail,
      b.MaBangCap,
      TenBangCap = b.TenVietTat,
      idBangCap = b.Id,
      k.MaKhoa,
      k.TenKhoa,
      idKhoa = k.Id,
      c.MaChucVu,
      c.TenChucVu,
      IdChucVu = c.Id
    };
    return Ok(await result.ToListAsync());
  }

  [HttpPut("sua-thong-tin")]
  public async Task<ActionResult> GetInfo([FromBody] UpdateGiangVienDto c)
  {
    GiangVien gv = c.GiangVien!;
    await _context.UpdateAsync([gv]);

    Khoa_GiangVien? kgv = await _ct.Khoa_GiangVien.FirstOrDefaultAsync(a => a.GiangVienId == c.GiangVien!.Id);
    if (kgv is null) return BadRequest();

    await _k_gvRepository.UpdateAsync([new() {
      ChucVuId = c.ChucVuId,
      GiangVienId = gv.Id,
      KhoaId = c.KhoaId,
      Id = kgv.Id
    }]);
    // Console.WriteLine(kgv.Id);
    // if (kgv is null) await _ct.Khoa_GiangVien.AddAsync(
    //   new() { ChucVuId = c.ChucVuId, GiangVienId = gv.Id, KhoaId = c.KhoaId });
    var result =
      from g in _ct.GiangVien
      join b in _ct.BangCap on g.BangCapId equals b.Id
      join _kgv in _ct.Khoa_GiangVien on g.Id equals _kgv.GiangVienId
      join k in _ct.Khoa on _kgv.KhoaId equals k.Id
      join _c in _ct.ChucVu on _kgv.ChucVuId equals _c.Id
      where g.Id == gv.Id
      orderby g.MaGiangVien.Length, g.MaGiangVien
      select new
      {
        g.Id,
        g.MaGiangVien,
        g.TenGiangVien,
        GioiTinh = g.GioiTinh == 0 ? "Nam" : "Nữ",
        g.SinhNhat,
        g.SoDienThoai,
        g.Mail,
        b.MaBangCap,
        TenBangCap = b.TenVietTat,
        idBangCap = b.Id,
        k.MaKhoa,
        TenKhoa = k.TenVietTat,
        idKhoa = k.Id,
        _c.MaChucVu,
        _c.TenChucVu,
        IdChucVu = _c.Id
      };
    return Ok(await result.ToListAsync());
  }

  [HttpPost]
  public override async Task<IActionResult> Create(GiangVienDto _gv)
  {
    var bangCap = await _bangCapRepository.FindAsync(i => i.Id == _gv.BangCapId);

    if (bangCap.Count == 0) return BadRequest(new { Message = "BangCap is invalid!" });

    GiangVien giangVien = new()
    {
      MaGiangVien = _gv.MaGiangVien,
      BangCapId = _gv.BangCapId,
      GioiTinh = _gv.GioiTinh,
      Mail = _gv.Mail,
      SinhNhat = _gv.SinhNhat,
      SoDienThoai = _gv.SoDienThoai,
      TenGiangVien = _gv.TenGiangVien
    };

    try { await _context.CreateAsync([giangVien]); }
    catch (Exception) { return BadRequest(new { Message = "Invalid Input!" }); }

    return CreatedAtAction(nameof(Get), new { id = giangVien.Id }, _gv);
  }
  [HttpPost("them-giang-vien")]

  public async Task<IActionResult> AddNewGiangVien([FromBody] CreateGiangVienDto d)
  {
    try
    {
      GiangVienDto _gv = d.GiangVien!;
      Khoa khoa = await _ct.Khoa.FirstOrDefaultAsync(i => i.Id == d.KhoaId);
      if (khoa is null) return BadRequest("Không tìm thấy khoa");

      string err = GiangVien.IsValid(_ct, d);
      if (!string.IsNullOrWhiteSpace(err)) return BadRequest(err);

      GiangVien giangVien = GiangVien.FormatInput(_ct, d);
      await _context.CreateAsync([giangVien]);

      Khoa_GiangVien kgv = new()
      {
        ChucVuId = d.ChucVuId,
        GiangVienId = giangVien.Id,
        KhoaId = d.KhoaId
      };
      await _k_gvRepository.CreateAsync([kgv]);

    }
    catch (Exception e)
    {
      Console.WriteLine(e);
      return BadRequest();
    }

    return Ok();
  }
}