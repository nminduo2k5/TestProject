using System.Collections;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using server.Models;
using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class ChucVuController(IRepository<ChucVu> repo, AppDbContext context) : TemplatePostgreController<ChucVu, ChucVuDto>(repo)
{
  readonly AppDbContext _ct = context;
  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get()
  {
    // Khoi tao gia tri
    if (!_ct.ChucVu.Any())
    {
      List<ChucVu> _chucVu = [
        new () { MaChucVu = "DEG-1", TenChucVu = "Hiệu trưởng", TenVietTat = "HT" },
        new () { MaChucVu = "DEG-2", TenChucVu = "Phó Hiệu trưởng", TenVietTat = "PHT" },
        new () { MaChucVu = "DEG-3", TenChucVu = "Trưởng khoa", TenVietTat = "TK" },
        new () { MaChucVu = "DEG-4", TenChucVu = "Phó Trưởng khoa", TenVietTat = "PTK" },
        new () { MaChucVu = "DEG-5", TenChucVu = "Trưởng bộ môn", TenVietTat = "TBM" },
        new () { MaChucVu = "DEG-6", TenChucVu = "Phó Trưởng bộ môn", TenVietTat = "PTBM" },
        new () { MaChucVu = "DEG-7", TenChucVu = "Chủ nhiệm chương trình", TenVietTat = "CNCTr" },
        new () { MaChucVu = "DEG-8", TenChucVu = "Thư ký khoa", TenVietTat = "TKhK" },
        new () { MaChucVu = "DEG-9", TenChucVu = "Giảng viên chính", TenVietTat = "GVC" },
        new () { MaChucVu = "DEG-10", TenChucVu = "Giảng viên", TenVietTat = "GV" },
        new () { MaChucVu = "DEG-11", TenChucVu = "Trợ giảng", TenVietTat = "TG" },
        new () { MaChucVu = "DEG-12", TenChucVu = "Nghiên cứu viên", TenVietTat = "NCV" },
        new () { MaChucVu = "DEG-13", TenChucVu = "Thư ký khoa học", TenVietTat = "TKKH" },
        new () { MaChucVu = "DEG-14", TenChucVu = "Trưởng phòng đào tạo", TenVietTat = "TPĐT" },
        new () { MaChucVu = "DEG-15", TenChucVu = "Cán bộ quản lý đào tạo", TenVietTat = "CBQLĐT" }
      ];

      await _ct.ChucVu.AddRangeAsync(_chucVu);
      await _ct.SaveChangesAsync();
    }
    var result =
      from c in _ct.ChucVu
      orderby c.MaChucVu.Length, c.MaChucVu
      select c;

    return Ok(await result.ToListAsync());
  }
  [HttpPost]
  public override async Task<IActionResult> Create(ChucVuDto _cv)
  {
    ChucVu chucVu = new()
    {
      MaChucVu = _cv.MaChucVu,
      TenChucVu = _cv.TenChucVu,
      TenVietTat = _cv.TenVietTat
    };
    List<string> strings = [
      _cv.MaChucVu,
      _cv.TenChucVu,
      _cv.TenVietTat,
    ];
    if (strings.Any(string.IsNullOrEmpty)) return BadRequest("Nhập thiếu thông tin");
    await _context.CreateAsync([chucVu]);
    return CreatedAtAction(nameof(Get), new { id = chucVu.Id }, _cv);
  }
}