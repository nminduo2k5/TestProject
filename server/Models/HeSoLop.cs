using System.ComponentModel.DataAnnotations;

namespace server.Models;

public class HeSoLop
{
  public static HeSoLop Generate()
  {
    Random random = new();
    return new HeSoLop
    {
      HeSo = random.NextDouble() * 2 + 1, // Random value between 1.0 and 3.0
      SoHocSinhToiThieu = (uint)random.Next(0, 100), // Random value between 1 and 10
    };
  }

  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public uint SoHocSinhToiThieu { get; set; }
  public uint NamHoc { get; set; }
  public double HeSo { get; set; }
}