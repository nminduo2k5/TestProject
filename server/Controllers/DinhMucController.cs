using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using server.Models;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class DinhMucController(AppDbContext context) : ControllerBase
{
  private readonly AppDbContext _context = context;

  [HttpGet]
  public ActionResult Get()
  {
    var result =
      from dm in _context.DinhMucTien
      orderby dm.NgayCapNhat descending
      select dm;
    return Ok(result.ToList());
  }

  [HttpPost]
  public async Task<IActionResult> Create(DinhMucInput item)
  {
    DinhMucTien dinhMuc = new()
    {
      SoTien = item.SoTien,
      LyDo = item.LyDo
    };
    _context.DinhMucTien.Add(dinhMuc);
    await _context.SaveChangesAsync();
    return Ok(dinhMuc);
  }

  [HttpDelete("{id}")]
  public async Task<IActionResult> Delete(string id)
  {
    var dinhMuc = await _context.DinhMucTien.FindAsync(id);
    if (dinhMuc == null) return NotFound();

    _context.DinhMucTien.Remove(dinhMuc);
    return NoContent();
  }
}

public class DinhMucInput
{
  public ulong SoTien { get; set; }
  public string? LyDo { get; set; }
}