using System.Collections;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query.SqlExpressions;
using server.Models;
using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class BangCapController(IRepository<BangCap> repo, AppDbContext context) : TemplatePostgreController<BangCap, BangCapDto>(repo)
{
  readonly AppDbContext _ct = context;

  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get()
  {
    var result =
      from c in _ct.BangCap
      orderby c.MaBangCap.Length, c.MaBangCap
      select c;

    return Ok(await result.ToListAsync());
  }

  [HttpPost]
  public override async Task<IActionResult> Create(BangCapDto item)
  {
    // if (item.GetType() == typeof(BangCapD))
    List<string> strings = [
      // item.MaBangCap,
      item.TenBangCap,
      item.TenVietTat,
    ];
    if (strings.Any(string.IsNullOrEmpty)) return BadRequest("Nhập thiếu thông tin");

    BangCap bc = BangCap.FormatInput(_ct, item);
    if ((from c in _ct.BangCap
         where c.TenBangCap == item.TenBangCap
         select c).Any())
      return BadRequest("Tên bằng cấp đã tồn tại");

    if ((from c in _ct.BangCap
         where c.TenVietTat == item.TenVietTat
         select c).Any())
      return BadRequest("Tên viết tắt đã tồn tại");

    if (item.TenVietTat.Length > 10) return BadRequest("Tên viết tắt dài quá 10 ký tự!");
    try
    {
      await _context.CreateAsync([bc]);

    }
    catch (Exception)
    {
      return BadRequest("Thông tin không hợp lệ!");
    }
    return CreatedAtAction(nameof(Get), new { id = bc.Id }, item);
  }
}