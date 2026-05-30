using System.Collections;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using server.Models;

using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class KhoaController(IRepository<Khoa> repo, AppDbContext context) : TemplatePostgreController<Khoa, KhoaDto>(repo)
{
  readonly AppDbContext _ct = context;

  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get()
  {
    var result =
      from c in _ct.Khoa
      orderby c.MaKhoa.Length, c.MaKhoa
      select new
      {
        c.Id,
        c.MaKhoa,
        c.TenKhoa,
        c.TenVietTat,
        c.MoTa,
        c.ViTri,
        soLop = _ct.HocPhan.Count(i => i.KhoaId == c.Id),
        soGiangVien = _ct.Khoa_GiangVien.Count(i => i.KhoaId == c.Id)
      };

    return Ok(await result.ToListAsync());
  }

  [HttpPost]
  public override async Task<IActionResult> Create(KhoaDto _k)
  {
    Khoa khoa = Khoa.FormatInput(_ct, _k);
    List<string> strings = [
      khoa.MaKhoa,
      khoa.TenKhoa,
      khoa.ViTri,
      khoa.MaKhoa
    ];
    if (strings.Any(string.IsNullOrEmpty)) return BadRequest("Nhập thiếu thông tin");

    if (await _ct.Khoa.AnyAsync(c => c.TenKhoa == _k.TenKhoa))
      return BadRequest("Tên khoa đã tồn tại");

    if (await _ct.Khoa.AnyAsync(c => c.TenVietTat == _k.TenVietTat))
      return BadRequest("Tên viết tắt đã tồn tại");

    try
    {
      await _context.CreateAsync([khoa]);

    }
    catch (Exception)
    {
      return BadRequest("");
      throw;
    }

    return CreatedAtAction(nameof(Get), new { id = khoa.Id }, _k);
  }
}