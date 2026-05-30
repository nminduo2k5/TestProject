using System.ComponentModel.DataAnnotations;
using server.Repositories;

namespace server.Models;

public class ChucVu : ChucVuDto, IEntityPostgre
{
  public static ChucVu Generate()
  {
    return new ChucVu()
    {
      TenChucVu = Guid.NewGuid().ToString(),
      TenVietTat = Guid.NewGuid().ToString()
    };
  }
  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();

  public ICollection<Khoa_GiangVien>? Khoa_GiangViens { get; set; }
}

public class ChucVuDto
{
  public string MaChucVu { get; set; } = null!;
  public string TenChucVu { get; set; } = null!;
  public string TenVietTat { get; set; } = null!;
}