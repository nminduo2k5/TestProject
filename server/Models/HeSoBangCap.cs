using System.ComponentModel.DataAnnotations;

namespace server.Models;

public class HeSoBangCap
{
  [Key]
  public Guid Id { get; set; } = new();
  public double HeSo { get; set; } = 1.0;
  public uint Nam { get; set; }

  public Guid MaBangCap { get; set; }
  public BangCap? BangCap { get; set; }
}