using System.Collections;
using Microsoft.AspNetCore.Mvc;

namespace server.Controllers;

public abstract class ITemplateController<T, Dto> : ControllerBase where T : class, Dto
{
  public abstract Task<ActionResult<ICollection>> Get();
  public abstract Task<ActionResult> Get(string id);
  public abstract Task<IActionResult> Create(Dto _gv);
  public abstract Task<IActionResult> Update(T instance);
  public abstract Task<IActionResult> Delete(string id);
}