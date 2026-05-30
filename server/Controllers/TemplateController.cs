using System.Collections;
using Microsoft.AspNetCore.Mvc;
using server.Repositories;

namespace server.Controllers;

public abstract class TemplatePostgreController<T, Dto>(IRepository<T> context) :
  ITemplateController<T, Dto> where T : class, Dto, IEntityPostgre
{
  protected readonly IRepository<T> _context = context;

  [HttpGet]
  public override async Task<ActionResult<ICollection>> Get() =>
    Ok(await _context.GetAllAsync());

  [HttpGet("{id}")]
  public override async Task<ActionResult> Get(string id) =>
    Ok(await _context.FindAsync(i => i.Id.ToString() == id));

  [HttpPost]
  public override abstract Task<IActionResult> Create(Dto item);

  [HttpPut]
  public override async Task<IActionResult> Update(T instances)
  {
    await _context.UpdateAsync([instances]);
    return NoContent();
  }

  [HttpDelete("{id}")]
  public override async Task<IActionResult> Delete(string id)
  {
    ICollection<T> khoa = await _context.FindAsync(i => i.Id.ToString() == id);
    if (khoa is null) return NotFound();

    await _context.DeleteAsync(khoa);
    return NoContent();
  }
}