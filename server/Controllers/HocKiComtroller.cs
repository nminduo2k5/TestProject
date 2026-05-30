using System.Collections;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query.SqlExpressions;
using server.Models;
using server.Repositories;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class HocKiController(IRepository<HocKi> repo, AppDbContext context) : TemplatePostgreController<HocKi, HocKiDto>(repo)
{
  readonly AppDbContext _ct = context;

  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get()
  {
    var result =
        from c in _ct.HocKi
        orderby c.ThoiGianBatDau descending, c.Id.ToString().Length, c.Id
        select new
        {
          c.TenKi,
          c.ThoiGianBatDau,
          c.ThoiGianKetThuc,
          c.Id,
          soLop = c.LopHocPhan!.Count()
        };

    return Ok(await result.ToListAsync());
  }

  [HttpPost]
  public override async Task<IActionResult> Create(HocKiDto item)
  {
    // if (item.GetType() == typeof(HocKiD))
    HocKi hk = new()
    {
      TenKi = item.TenKi,
      ThoiGianBatDau = DateTime.SpecifyKind(item.ThoiGianBatDau, DateTimeKind.Utc),
      ThoiGianKetThuc = DateTime.SpecifyKind(item.ThoiGianKetThuc, DateTimeKind.Utc),
    };
    await _context.CreateAsync([hk]);
    return CreatedAtAction(nameof(Get), new { id = hk.Id }, item);
  }
}