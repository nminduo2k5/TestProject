using System.ComponentModel.DataAnnotations;
using server.Controllers;
using server.Repositories;

namespace server.Models;

public class HocPhan : HocPhanDto, IEntityPostgre
{
  public static HocPhan GenerateSample(string tenHP, float heSoHP, Khoa khoa)
  {
    return new()
    {
      MaHocPhan = $"{khoa.MaKhoa}_{DateTime.Now.Ticks}",
      TenHocPhan = tenHP,
      HeSoHocPhan = heSoHP,
      Khoa = khoa,
    };
  }
  public static HocPhan Generate(Khoa khoa)
  {
    Random random = new();

    return new()
    {
      MaHocPhan = $"{khoa.MaKhoa}_{DateTime.Now.Ticks}",
      TenHocPhan = Guid.NewGuid().ToString().Substring(5, 15),
      HeSoHocPhan = (float)Math.Round(random.NextDouble() * 0.5 + 1.0, 2),
      SoTinChi = (uint)random.Next(1, 5),
      SoTiet = (uint)random.Next(15, 61),
      KhoaId = khoa.Id
    };
  }

  public static HocPhan FormatInput(AppDbContext context, HocPhanDto input)
  {
    if (string.IsNullOrWhiteSpace(input.TenHocPhan)) throw new Exception("Tên học phần không được để trống");
    if (input.HeSoHocPhan <= 0) throw new Exception("Hệ số học phần phải lớn hơn 0");


    if (input.KhoaId == Guid.Empty) throw new Exception("Không tìm thấy Khoa");
    var khoa = context.Khoa.FirstOrDefault(k => k.Id == input.KhoaId);
    if (khoa is null) throw new Exception("Không tìm thấy Khoa");

    var maKhoa = khoa!.MaKhoa.Length > 4 ? khoa.MaKhoa[4..] : khoa.MaKhoa;
    var count = context.HocPhan.Count(hp => hp.Khoa!.Id == input.KhoaId);
    var stt = count + 1;

    return new()
    {
      MaHocPhan = $"{maKhoa}_{stt}",
      TenHocPhan = input.TenHocPhan,
      HeSoHocPhan = input.HeSoHocPhan,
      SoTiet = input.SoTiet,
      SoTinChi = input.SoTinChi,
      KhoaId = khoa.Id
    };
  }
  public static HocPhan FormatInput(AppDbContext context, HocPhanInput input)
  {
    if (string.IsNullOrWhiteSpace(input.TenHocPhan))
      throw new Exception("Tên học phần không được để trống");
    if (input.HeSoHocPhan <= 0)
      throw new Exception("Hệ số học phần phải lớn hơn 0");

    var khoa = context.Khoa.FirstOrDefault(k => k.Id == input.KhoaId);
    //if (khoa == null) throw new Exception("Không tìm thấy Khoa");
    var maKhoa = khoa!.MaKhoa.Length > 4 ? khoa.MaKhoa[4..] : khoa.MaKhoa;

    var count = context.HocPhan.Count(hp => hp.Khoa!.Id == input.KhoaId);
    var stt = count + 1;

    return new()
    {
      MaHocPhan = $"{maKhoa}_{stt}",
      TenHocPhan = input.TenHocPhan,
      HeSoHocPhan = input.HeSoHocPhan,
      KhoaId = khoa.Id,
    };
  }

  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public Khoa? Khoa { get; set; }
  public ICollection<LopHocPhan>? LopHocPhans { get; set; }
}

public class HocPhanDto
{
  public string MaHocPhan { get; set; } = null!;
  public string TenHocPhan { get; set; } = null!;
  public float HeSoHocPhan { get; set; } = 0!;
  public uint SoTinChi { get; set; } = 0!;
  public uint SoTiet { get; set; } = 0!;
  public Guid KhoaId { get; set; }
}