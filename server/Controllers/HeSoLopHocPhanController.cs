using Microsoft.AspNetCore.Mvc;
using server.Models;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class HeSoLopHocPhanController(AppDbContext context) : ControllerBase
{
  readonly AppDbContext context = context;

  [HttpGet]
  public ActionResult Get()
  {
    var result =
      from h in context.HeSoLop
      orderby h.SoHocSinhToiThieu ascending
      select h;

    return Ok(result.ToList());
  }

  [HttpGet("{nam}")]
  public ActionResult GetByYear(uint nam)
  {
    var result =
      from h in context.HeSoLop
      where h.NamHoc == nam
      orderby h.SoHocSinhToiThieu ascending
      select h;

    if (result.Count() > 0) return Ok(result.ToList());
    try
    {
      context.HeSoLop.AddRange([
        new HeSoLop()
      {
        HeSo = -0.3,
        SoHocSinhToiThieu = 20,
        NamHoc = nam
      },
      new HeSoLop(){
        HeSo = 0.2,
        SoHocSinhToiThieu = 70,
        NamHoc = nam
      },
      new HeSoLop(){
        HeSo = 0.3,
        SoHocSinhToiThieu = 100,
        NamHoc = nam
      }
      ]);
      context.SaveChanges();
    }
    catch (Exception) { }

    result =
      from h in context.HeSoLop
      where h.NamHoc == nam
      orderby h.SoHocSinhToiThieu ascending
      select h;
    return Ok(result.ToList());
  }

  [HttpPost]
  public async Task<ActionResult> Post(HeSoLopInput input)
  {
    Console.WriteLine($"{input.NamHoc} {input.SoHocSinhToiThieu} {input.HeSo}");
    HeSoLop h = new()
    {
      HeSo = input.HeSo,
      SoHocSinhToiThieu = input.SoHocSinhToiThieu,
      NamHoc = input.NamHoc
    };

    context.HeSoLop.Add(h);
    await context.SaveChangesAsync();

    return Ok();
  }

  [HttpPut("{id}")]
  public async Task<ActionResult> Put(Guid id, HeSoLopInput input)
  {
    HeSoLop heSoLop = context.HeSoLop.Find(id)!;
    if (heSoLop is null) return NotFound();

    heSoLop.HeSo = input.HeSo;
    heSoLop.SoHocSinhToiThieu = input.SoHocSinhToiThieu;
    heSoLop.NamHoc = input.NamHoc;

    await context.SaveChangesAsync();
    return Ok();
  }

  [HttpDelete("{id}")]
  public ActionResult Delete(Guid id)
  {
    try
    {
      context.HeSoLop.Remove(context.HeSoLop.FirstOrDefault(i => i.Id == id)!);
      context.SaveChanges();
    }
    catch (Exception)
    {
      return NotFound();
    }
    return NoContent();
  }
}

public class HeSoLopInput()
{
  public uint SoHocSinhToiThieu { get; set; }
  public uint NamHoc { get; set; }
  public double HeSo { get; set; }
}