using System.ComponentModel.DataAnnotations;
using System.Net.Mail;
using Microsoft.EntityFrameworkCore;
using server.Repositories;

namespace server.Models;

public class LopHocPhan : LopHocPhanDto, IEntityPostgre
{
    static string GenerateRandomName(int length)
    {
        Random _random = new();
        const string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ";
        return new string([.. Enumerable
            .Repeat(chars, length)
            .Select(s => s[_random.Next(s.Length)])
        ]);
    }
    public static LopHocPhan Generate(string hocKi, string hocPhan, string namBd, Guid hocPhanId, Guid hocKiId, Guid? giangVienId)
    {
        Random random = new();
        string name = GenerateRandomName(random.Next(5, 20));
        return new LopHocPhan()
        {
            MaLop = $"{hocPhan}_{hocKi}_{namBd}_{random.Next()}", // HP_KI_Năm bd
            TenLop = name,
            SoLuongSinhVien = (uint)random.Next(20, 100),
            HocPhanId = hocPhanId,
            HocKiId = hocKiId,
            GiangVienId = giangVienId
        };
    }
    public static LopHocPhan Generate(GiangVien? giangVien, HocPhan hocPhan, HocKi hocKi, int index)
    {
        Random random = new();
        return new LopHocPhan()
        {
            MaLop = $"{hocPhan.MaHocPhan}-{index.ToString().PadLeft(2, '0')}", // HP_KI_Năm bd
            TenLop = $"{hocPhan.TenHocPhan} (N{index.ToString().PadLeft(2, '0')})",
            SoLuongSinhVien = (uint)random.Next(40, 100),
            HocPhanId = hocPhan.Id,
            HocKiId = hocKi.Id,
            GiangVienId = giangVien?.Id
        };
    }

    public static string IsValid(AppDbContext context, CreateLopHocPhanDto input)
    {
        if (string.IsNullOrWhiteSpace(input.MaLop)) return "Mã lớp không được để trống";
        if (string.IsNullOrWhiteSpace(input.TenLop)) return "Tên lớp không được để trống";
        if (input.SoLuongSinhVien <= 0) return "Số lượng sinh viên phải lớn hơn 0";

        return string.Empty;
    }

    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    public HocPhan? HocPhan { get; set; }
    public HocKi? HocKi { get; set; }
    public GiangVien? GiangVien { get; set; }
}
// public enum TrangThaiLop { DangMo, DaDong, KetThuc }
public class LopHocPhanDto
{
    public string MaLop { get; set; } = null!;
    public string TenLop { get; set; } = null!;
    public uint SoLuongSinhVien { get; set; } = 0!;
    public Guid HocPhanId { get; set; }
    public Guid HocKiId { get; set; }
    public Guid? GiangVienId { get; set; }
}


public class CreateLopHocPhanDto : LopHocPhanDto
{
    public LopHocPhanDto? LopHocPhan { get; set; }
}

public class UpdateLopHocPhanDto
{
    public uint SoLuongSinhVien { get; set; } = 0!;
    public Guid HocPhanId { get; set; }
    public Guid HocKiId { get; set; }
    public Guid? GiangVienId { get; set; }
    public Guid Id { get; set; }
}

public class PhanCongGiangVienDto
{
    public Guid LopHocPhanId { get; set; }
    public Guid GiangVienId { get; set; }
}