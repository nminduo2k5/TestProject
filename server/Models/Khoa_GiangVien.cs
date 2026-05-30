using System.ComponentModel.DataAnnotations;
using server.Repositories;

namespace server.Models;

public class Khoa_GiangVien : Khoa_GiangVienDto, IEntityPostgre
{
  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();

  public GiangVien? GiangVien { get; set; }
  public Khoa? Khoa { get; set; }
  public ChucVu? ChucVu { get; set; }
}

public class UpdateGiangVienDto
{
  public GiangVien? GiangVien { get; set; }
  public Guid KhoaId { get; set; }
  public Guid ChucVuId { get; set; }
}

public class CreateGiangVienDto
{
  public GiangVienDto? GiangVien { get; set; }
  public Guid KhoaId { get; set; }
  public Guid ChucVuId { get; set; }
}

public class Khoa_GiangVienDto
{
  public Guid GiangVienId { get; set; }
  public Guid KhoaId { get; set; }
  public Guid ChucVuId { get; set; }
}