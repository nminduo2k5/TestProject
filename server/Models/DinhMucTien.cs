using System.ComponentModel.DataAnnotations;

namespace server.Models;

public class DinhMucTien
{
  static DateTime GenerateRandomDate()
  {
    Random rand = new();
    return new DateTime(
      2000 + rand.Next(30),
      rand.Next() % 12 + 1,
      rand.Next() % 28 + 1,
      rand.Next(24),
      rand.Next(60), rand.Next(60), rand.Next(1000), DateTimeKind.Utc);
  }
  public static DinhMucTien Generate()
  {
    Random random = new();
    ulong soTien = (ulong)(random.Next() % 1000000 + 10000); // Random amount between 10,000 and 1,000,000
    return new DinhMucTien
    {
      SoTien = soTien,
      LyDo = Guid.NewGuid().ToString(),
      NgayCapNhat = GenerateRandomDate()
    };
  }

  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public ulong SoTien { get; set; }
  public DateTime NgayCapNhat { get; set; } = DateTime.UtcNow;
  public string? LyDo { get; set; }
}