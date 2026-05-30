using System.ComponentModel.DataAnnotations;
using System.Net.Mail;
using Microsoft.EntityFrameworkCore;
using server.Repositories;

namespace server.Models;

public class GiangVien : GiangVienDto, IEntityPostgre
{
  static DateTime GenerateRandomDate()
  {
    Random rand = new();
    return new DateTime(1950 + rand.Next() % 60, rand.Next() % 12 + 1, rand.Next() % 28 + 1, 0, 0, 0, DateTimeKind.Utc);
  }
  static string GenerateRandomName(int length)
  {
    Random _random = new();
    const string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    return new string([..
      Enumerable
        .Repeat(chars, length)
        .Select(s => s[_random.Next(s.Length)])
    ]);
  }
  public static string GenerateRandomVietnamPhoneNumber()
  {
    var prefixes = new[] { "09", "03", "07", "08", "05" };
    var random = new Random();

    string prefix = prefixes[random.Next(prefixes.Length)];
    string number = random.Next(10000000, 99999999).ToString(); // 8 chữ số sau

    return prefix + number;
  }
  public static string GenerateRandomEmail(string name)
  {
    var random = new Random();
    var domains = new[] { "gmail.com", "yahoo.com", "outlook.com", "example.com" };
    var namePrefix = "user";
    string domain = domains[random.Next(domains.Length)];

    return $"{namePrefix}_{name}@{domain}";
  }

  static string GenerateRandomVietnameseName()
  {
    Random rand = new();

    string[] ho = { "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Đinh" };
    string[] tenDemNam = { "Văn", "Hữu", "Đức", "Quang", "Minh", "Gia", "Anh" };
    string[] tenDemNu = { "Thị", "Ngọc", "Thuỳ", "Bích", "Diệu", "Cẩm", "Mai" };
    string[] tenChinhNam = { "An", "Bình", "Dũng", "Khang", "Long", "Phong", "Nam", "Toàn", "Tuấn", "Hải", "Quốc" };
    string[] tenChinhNu = { "Lan", "Hoa", "Hương", "Nhung", "Yến", "Trang", "Linh", "Vy", "Thảo", "Nhi", "Ngân" };

    bool isMale = rand.NextDouble() < 0.7; // 70% nam, 30% nữ

    string hoTen = ho[rand.Next(ho.Length)] + " ";

    if (isMale)
      hoTen += tenDemNam[rand.Next(tenDemNam.Length)] + " " + tenChinhNam[rand.Next(tenChinhNam.Length)];
    else
      hoTen += tenDemNu[rand.Next(tenDemNu.Length)] + " " + tenChinhNu[rand.Next(tenChinhNu.Length)];

    return hoTen;
  }

  public static GiangVien Generate(Guid bangCapId, int count, string khoa)
  {
    Random random = new();
    string name = GenerateRandomVietnameseName();
    return new()
    {
      MaGiangVien = $"PU_{khoa}_{count}",
      TenGiangVien = name,
      GioiTinh = random.NextDouble() < 0.7 ? 1 : 0, // 70% nam (1), 30% nữ (0)
      SinhNhat = GenerateRandomDate(),
      SoDienThoai = GenerateRandomVietnamPhoneNumber(),
      Mail = GenerateRandomEmail(name),
      BangCapId = bangCapId
    };
  }

  public static string IsValid(AppDbContext context, CreateGiangVienDto input)
  {
    if (input.GiangVien is null) return "Nhập thiếu thông tin";
    List<string> values = [
      input.ChucVuId.ToString(),
      input.KhoaId.ToString(),
      input.GiangVien.BangCapId.ToString(),
      input.GiangVien.Mail.ToString(),
      input.GiangVien.SoDienThoai.ToString(),
      input.GiangVien.TenGiangVien.ToString(),
      input.GiangVien.SinhNhat.ToString()
    ];
    if (values.Any(string.IsNullOrEmpty)) return "Nhập thiếu thông tin";

    if (input.GiangVien.TenGiangVien.Any(i => i != ' ' && !char.IsLetter(i))) return "Tên giáo viên không được chứa số hoặc ký tự đặc biệt!";
    if (input.GiangVien.SoDienThoai.Length > 12 || input.GiangVien.SoDienThoai.Any(i => i != ' ' && !char.IsDigit(i))) return "Số điện thoại không đúng định dạng";
    if (context.GiangVien.Any(i => i.SoDienThoai == input.GiangVien.SoDienThoai)) return "Số điện thoại không đúng định dạng";
    if (input.GiangVien.GioiTinh > 2) return "Giới tính không hợp lệ!";
    if (DateTime.Now.Year - input.GiangVien.SinhNhat.Year < 18) return "Giáo viên nhỏ hơn 18 tuổi";
    if (!new EmailAddressAttribute().IsValid(input.GiangVien.Mail)) return "Email không đúng định dạng";

    ChucVu _cv = context.ChucVu.FirstOrDefault(i => i.Id == input.ChucVuId)!;
    if (_cv.MaChucVu != "DEG-3") return "";

    var result =
      (from kgv in context.Khoa_GiangVien
       join k in context.Khoa on kgv.KhoaId equals k.Id
       join c in context.ChucVu on kgv.ChucVuId equals c.Id
       where c.MaChucVu == "DEG-3" && kgv.KhoaId == input.KhoaId
       select new { }).ToList().Count;
    if (result > 0) return "";

    return "";
  }

  public static GiangVien FormatInput(AppDbContext context, CreateGiangVienDto input)
  {
    GiangVienDto _gv = input.GiangVien!;
    Khoa khoa = context.Khoa.FirstOrDefault(i => i.Id == input.KhoaId)!;
    return new()
    {
      MaGiangVien = $"PU_{khoa.TenVietTat}_{context.GiangVien.Count() + 1}",
      BangCapId = _gv.BangCapId,
      GioiTinh = _gv.GioiTinh,
      Mail = _gv.Mail,
      SinhNhat = _gv.SinhNhat,
      SoDienThoai = _gv.SoDienThoai,
      TenGiangVien = _gv.TenGiangVien
    };
  }
  [Key]
  public Guid Id { get; set; } = Guid.NewGuid();
  public BangCap? BangCap { get; set; }
  public ICollection<LopHocPhan>? LopHocPhans { get; set; }
  public ICollection<Khoa_GiangVien>? Khoa_GiangViens { get; set; }
}

public class GiangVienDto
{
  public string MaGiangVien { get; set; } = null!;
  public string TenGiangVien { get; set; } = null!;
  public int GioiTinh { get; set; }
  public DateTime SinhNhat { get; set; }
  public string SoDienThoai { get; set; } = null!;
  public string Mail { get; set; } = null!;
  public Guid BangCapId { get; set; }
}