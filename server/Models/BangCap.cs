using System.ComponentModel.DataAnnotations;
using server.Repositories;

namespace server.Models;

public class BangCap : BangCapDto, IEntityPostgre
{
  public static BangCap Generate()
  {
    return new BangCap()
    {
      TenBangCap = Guid.NewGuid().ToString(),
      TenVietTat = Guid.NewGuid().ToString()
    };
  }
  public static BangCap FormatInput(AppDbContext context, BangCapDto input)
  {
    return new()
    {
      MaBangCap = $"DEG_{context.BangCap.Count() + 1}",
      TenBangCap = input.TenBangCap,
      TenVietTat = input.TenVietTat
    };
  }
  public static BangCap FormatInput(int index, BangCapDto input)
  {
    return new()
    {
      MaBangCap = $"DEG_{index}",
      TenBangCap = input.TenBangCap,
      TenVietTat = input.TenVietTat
    };
  }

  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public ICollection<GiangVien>? GiangViens { get; set; }
}


public class BangCapDto
{
  public string MaBangCap { get; set; } = null!;
  public string TenBangCap { get; set; } = null!;
  public string TenVietTat { get; set; } = null!;

  public List<HeSoBangCap>? HeSoBangCap { get; set; }
}

