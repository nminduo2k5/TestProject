using System.ComponentModel.DataAnnotations;
using server.Repositories;

namespace server.Models;

public class HocKi : HocKiDto, IEntityPostgre
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
  public static HocKi Generate()
  {
    DateTime start = GenerateRandomDate();
    DateTime end = start.AddMonths(6);
    return new HocKi()
    {
      TenKi = Guid.NewGuid().ToString(),
      ThoiGianBatDau = start,
      ThoiGianKetThuc = end
    };
  }
  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public ICollection<LopHocPhan>? LopHocPhan { get; set; }
}

public class HocKiDto
{
  public string TenKi { get; set; } = null!;
  public DateTime ThoiGianBatDau { get; set; }
  public DateTime ThoiGianKetThuc { get; set; }
}

