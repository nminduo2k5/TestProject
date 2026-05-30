using System.ComponentModel.DataAnnotations;
using server.Repositories;

namespace server.Models;

public class Khoa : KhoaDto, IEntityPostgre
{
  public static Khoa Generate()
  {
    return new()
    {
      MaKhoa = Guid.NewGuid().ToString(),
      TenKhoa = Guid.NewGuid().ToString(),
      TenVietTat = Guid.NewGuid().ToString(),
      ViTri = Guid.NewGuid().ToString(),
      MoTa = Guid.NewGuid().ToString()
    };
  }
  public static Khoa FormatInput(AppDbContext context, KhoaDto input)
  {
    // Console.WriteLine($"FAC_{input.TenVietTat}");
    return new()
    {
      MaKhoa = $"FAC_{input.TenVietTat}",
      TenKhoa = input.TenKhoa,
      TenVietTat = input.TenVietTat,
      ViTri = input.ViTri,
      MoTa = input.MoTa
    };
  }

  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();

  public ICollection<Khoa_GiangVien>? Khoa_GiangViens { get; set; }
  public ICollection<HocPhan>? HocPhans { get; set; }
}

public class KhoaDto
{
  public string MaKhoa { get; set; } = null!;
  public string TenKhoa { get; set; } = null!;
  public string TenVietTat { get; set; } = null!;
  public string ViTri { get; set; } = null!;
  public string MoTa { get; set; } = null!;
}