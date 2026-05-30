using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using server.Models;
using ZstdSharp.Unsafe;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class TestController(AppDbContext context) : ControllerBase
{
  readonly AppDbContext _ct = context;
  [HttpDelete]
  public async Task<ActionResult> Delete()
  {
    _ct.DinhMucTien.RemoveRange(await _ct.DinhMucTien.ToListAsync());
    _ct.HeSoBangCap.RemoveRange(await _ct.HeSoBangCap.ToListAsync());
    _ct.HeSoLop.RemoveRange(await _ct.HeSoLop.ToListAsync());
    _ct.Khoa_GiangVien.RemoveRange(await _ct.Khoa_GiangVien.ToListAsync());
    _ct.GiangVien.RemoveRange(await _ct.GiangVien.ToListAsync());
    _ct.BangCap.RemoveRange(await _ct.BangCap.ToListAsync());
    _ct.ChucVu.RemoveRange(await _ct.ChucVu.ToListAsync());
    _ct.HocPhan.RemoveRange(await _ct.HocPhan.ToListAsync());
    _ct.LopHocPhan.RemoveRange(await _ct.LopHocPhan.ToListAsync());
    _ct.HocKi.RemoveRange(await _ct.HocKi.ToListAsync());
    _ct.Khoa.RemoveRange(await _ct.Khoa.ToListAsync());
    _ct.HocKi.RemoveRange(await _ct.HocKi.ToListAsync());

    await _ct.SaveChangesAsync();

    return Ok();
  }

  [HttpGet("add-khoa-bangcap-chucvu")]
  public async Task<ActionResult> DD()
  {
    _ct.BangCap.RemoveRange(await _ct.BangCap.ToListAsync());
    _ct.ChucVu.RemoveRange(await _ct.ChucVu.ToListAsync());
    _ct.Khoa.RemoveRange(await _ct.Khoa.ToListAsync());
    await _ct.SaveChangesAsync();

    List<Khoa> _khoa = [
        new () { MaKhoa = "FAC_CNTT", TenKhoa = "Khoa Công nghệ thông tin", TenVietTat = "CNTT", ViTri = "Tầng 5, Tòa A", MoTa = "Đào tạo và nghiên cứu về công nghệ thông tin." },
        new () { MaKhoa = "FAC_KTPM", TenKhoa = "Khoa Kỹ thuật phần mềm", TenVietTat = "KTPM", ViTri = "Tầng 6, Tòa A", MoTa = "Chuyên ngành lập trình, kiểm thử và quản lý dự án phần mềm." },
        new () { MaKhoa = "FAC_HTTT", TenKhoa = "Khoa Hệ thống thông tin", TenVietTat = "HTTT", ViTri = "Tầng 4, Tòa A", MoTa = "Tập trung vào phân tích và thiết kế hệ thống thông tin." },
        new () { MaKhoa = "FAC_ATTT", TenKhoa = "Khoa An toàn thông tin", TenVietTat = "ATTT", ViTri = "Tầng 3, Tòa A", MoTa = "Đào tạo chuyên sâu về bảo mật và an toàn hệ thống." },
        new () { MaKhoa = "FAC_KHMT", TenKhoa = "Khoa Khoa học máy tính", TenVietTat = "KHMT", ViTri = "Tầng 2, Tòa A", MoTa = "Nghiên cứu lý thuyết và ứng dụng của khoa học máy tính." },
        new () { MaKhoa = "FAC_Đ-ĐT", TenKhoa = "Khoa Kỹ thuật điện - điện tử", TenVietTat = "Đ-ĐT", ViTri = "Tầng 1, Tòa B", MoTa = "Đào tạo kỹ sư điện và điện tử ứng dụng." },
        new () { MaKhoa = "FAC_CK", TenKhoa = "Khoa Cơ khí", TenVietTat = "CK", ViTri = "Tầng 2, Tòa B", MoTa = "Giảng dạy các ngành cơ khí chế tạo và cơ điện tử." },
        new () { MaKhoa = "FAC_XD", TenKhoa = "Khoa Xây dựng", TenVietTat = "XD", ViTri = "Tầng 3, Tòa B", MoTa = "Đào tạo kỹ sư xây dựng dân dụng và công nghiệp." },
        new () { MaKhoa = "FAC_KTr", TenKhoa = "Khoa Kiến trúc", TenVietTat = "KTr", ViTri = "Tầng 4, Tòa B", MoTa = "Chuyên ngành thiết kế và quy hoạch kiến trúc." },
        new () { MaKhoa = "FAC_TTH", TenKhoa = "Khoa Toán - Tin học", TenVietTat = "TTH", ViTri = "Tầng 5, Tòa B", MoTa = "Đào tạo các ngành toán ứng dụng và tin học." },
        new () { MaKhoa = "FAC_VLKT", TenKhoa = "Khoa Vật lý kỹ thuật", TenVietTat = "VLKT", ViTri = "Tầng 6, Tòa B", MoTa = "Ứng dụng vật lý trong các lĩnh vực kỹ thuật." },
        new () { MaKhoa = "FAC_HH", TenKhoa = "Khoa Hóa học", TenVietTat = "HH", ViTri = "Tầng 7, Tòa B", MoTa = "Nghiên cứu hóa học và ứng dụng trong công nghiệp." },
        new () { MaKhoa = "FAC_SH", TenKhoa = "Khoa Sinh học", TenVietTat = "SH", ViTri = "Tầng 8, Tòa B", MoTa = "Giảng dạy các chuyên ngành về sinh học và công nghệ sinh học." },
        new () { MaKhoa = "FAC_MT", TenKhoa = "Khoa Môi trường", TenVietTat = "MT", ViTri = "Tầng 9, Tòa B", MoTa = "Đào tạo kỹ sư môi trường và quản lý tài nguyên thiên nhiên." },
        new () { MaKhoa = "FAC_KT", TenKhoa = "Khoa Kinh tế", TenVietTat = "KT", ViTri = "Tầng 1, Tòa C", MoTa = "Đào tạo cử nhân kinh tế học và kinh tế phát triển." },
        new () { MaKhoa = "FAC_TCNH", TenKhoa = "Khoa Tài chính - Ngân hàng", TenVietTat = "TCNH", ViTri = "Tầng 2, Tòa C", MoTa = "Giảng dạy các chuyên ngành tài chính, ngân hàng, đầu tư." },
        new () { MaKhoa = "FAC_QTKD", TenKhoa = "Khoa Quản trị kinh doanh", TenVietTat = "QTKD", ViTri = "Tầng 3, Tòa C", MoTa = "Đào tạo kỹ năng quản lý và điều hành doanh nghiệp." },
        new () { MaKhoa = "FAC_MKT", TenKhoa = "Khoa Marketing", TenVietTat = "MKT", ViTri = "Tầng 4, Tòa C", MoTa = "Chuyên ngành tiếp thị, truyền thông và thương hiệu." },
        new () { MaKhoa = "FAC_KTKT", TenKhoa = "Khoa Kế toán - Kiểm toán", TenVietTat = "KTKT", ViTri = "Tầng 5, Tòa C", MoTa = "Đào tạo cử nhân kế toán, kiểm toán và thuế." },
        new () { MaKhoa = "FAC_L", TenKhoa = "Khoa Luật", TenVietTat = "L", ViTri = "Tầng 6, Tòa C", MoTa = "Giảng dạy luật dân sự, hình sự, hành chính và thương mại." }
    ];


    var formatedKhoa = _khoa.Select((item, i) =>
      Khoa.FormatInput(_ct, new()
      {
        TenKhoa = item.TenKhoa,
        TenVietTat = item.TenVietTat,
        ViTri = item.ViTri,
        MoTa = item.MoTa
      }));
    Console.WriteLine(string.Join('\n', formatedKhoa.Select(i => i.MaKhoa)));

    List<BangCap> _bangCap = [
        new (){ MaBangCap = "DEG_1", TenBangCap = "Giáo sư", TenVietTat = "GS", },
        new (){ MaBangCap = "DEG_2", TenBangCap = "Phó Giáo sư", TenVietTat = "PGS", },
        new (){ MaBangCap = "DEG_3", TenBangCap = "Tiến sĩ", TenVietTat = "TS", },
        new (){ MaBangCap = "DEG_4", TenBangCap = "Thạc sĩ", TenVietTat = "ThS", },
        new (){ MaBangCap = "DEG_5", TenBangCap = "Cử nhân", TenVietTat = "CN", },
        new (){ MaBangCap = "DEG_6", TenBangCap = "Kỹ sư", TenVietTat = "KS", },
        // new (){ MaBangCap = "DEG_4", TenBangCap = "Tiến sĩ khoa học", TenVietTat = "TSKH", },
        // new (){ MaBangCap = "DEG_8", TenBangCap = "Bác sĩ", TenVietTat = "BS", },
        // new (){ MaBangCap = "DEG_9", TenBangCap = "Dược sĩ", TenVietTat = "DS", },
        // new (){ MaBangCap = "DEG_10", TenBangCap = "Giáo viên", TenVietTat = "GV",  }
    ];
    var formatedBangCap = _bangCap.Select((item, i) =>
      BangCap.FormatInput(i + 1, new() { TenBangCap = item.TenBangCap, TenVietTat = item.TenVietTat }));

    List<ChucVu> _chucVu = [
      new () { MaChucVu = "DEG-1", TenChucVu = "Hiệu trưởng", TenVietTat = "HT" },
      new () { MaChucVu = "DEG-2", TenChucVu = "Phó Hiệu trưởng", TenVietTat = "PHT" },
      new () { MaChucVu = "DEG-3", TenChucVu = "Trưởng khoa", TenVietTat = "TK" },
      new () { MaChucVu = "DEG-4", TenChucVu = "Phó Trưởng khoa", TenVietTat = "PTK" },
      new () { MaChucVu = "DEG-5", TenChucVu = "Trưởng bộ môn", TenVietTat = "TBM" },
      new () { MaChucVu = "DEG-6", TenChucVu = "Phó Trưởng bộ môn", TenVietTat = "PTBM" },
      new () { MaChucVu = "DEG-7", TenChucVu = "Chủ nhiệm chương trình", TenVietTat = "CNCTr" },
      new () { MaChucVu = "DEG-8", TenChucVu = "Thư ký khoa", TenVietTat = "TKhK" },
      new () { MaChucVu = "DEG-9", TenChucVu = "Giảng viên chính", TenVietTat = "GVC" },
      new () { MaChucVu = "DEG-10", TenChucVu = "Giảng viên", TenVietTat = "GV" },
      new () { MaChucVu = "DEG-11", TenChucVu = "Trợ giảng", TenVietTat = "TG" },
      new () { MaChucVu = "DEG-12", TenChucVu = "Nghiên cứu viên", TenVietTat = "NCV" },
      new () { MaChucVu = "DEG-13", TenChucVu = "Thư ký khoa học", TenVietTat = "TKKH" },
      new () { MaChucVu = "DEG-14", TenChucVu = "Trưởng phòng đào tạo", TenVietTat = "TPĐT" },
      new () { MaChucVu = "DEG-15", TenChucVu = "Cán bộ quản lý đào tạo", TenVietTat = "CBQLĐT" }
    ];

    try
    {
      await _ct.Khoa.AddRangeAsync(formatedKhoa);
      await _ct.BangCap.AddRangeAsync(formatedBangCap);
      await _ct.ChucVu.AddRangeAsync(_chucVu);
      await _ct.SaveChangesAsync();
    }
    catch (Exception) { throw; }
    return Ok();
  }

  [HttpGet("add-giang-vien")]
  public async Task<ActionResult> AddGV()
  {
    List<BangCap> _bangCap = await _ct.BangCap.ToListAsync();
    List<ChucVu> _ChucVu = await _ct.ChucVu.ToListAsync();
    List<Khoa> _Khoa = await _ct.Khoa.ToListAsync();
    var random = new Random();
    int gv_ = await _ct.GiangVien.CountAsync();
    for (int i = 0; i < 100; ++i)
    {
      try
      {
        Khoa k = _Khoa[random.Next(_Khoa.Count)];
        GiangVien giangVien = GiangVien.Generate(_bangCap[random.Next(_bangCap.Count)].Id, i + 1 + gv_, k.TenVietTat);
        Khoa_GiangVien kgv = new()
        {
          ChucVuId = _ChucVu[random.Next(_ChucVu.Count)].Id,
          GiangVienId = giangVien.Id,
          KhoaId = k.Id
        };

        await _ct.GiangVien.AddAsync(giangVien);
        await _ct.Khoa_GiangVien.AddAsync(kgv);
        await _ct.SaveChangesAsync();
      }
      catch (Exception e)
      {
        Console.WriteLine(e);
        return BadRequest();
      }

    }

    return Ok();
  }

  [HttpPost("add-hoc-phan")]
  public async Task<ActionResult> AddHocPhan()
  {
    List<Khoa> _Khoa = await _ct.Khoa.ToListAsync();
    if (_Khoa.Count == 0) return BadRequest("Chưa có Khoa nào, hãy thêm Khoa trước");

    var random = new Random();
    int hp_ = await _ct.HocPhan.CountAsync();
    for (int i = 0; i < 1000; ++i)
    {
      try
      {
        Khoa k = _Khoa[random.Next(_Khoa.Count)];
        HocPhan hocPhan = HocPhan.Generate(k);
        await _ct.HocPhan.AddAsync(hocPhan);
        await _ct.SaveChangesAsync();
      }
      catch (Exception e)
      {
        Console.WriteLine(e);
        return BadRequest();
      }
    }

    return Ok();
  }

  [HttpPost("add-hoc-ki")]
  public async Task<ActionResult> AddHocKi()
  {
    List<HocKi> hocKis = [];
    for (int i = 0; i < 200; ++i) hocKis.Add(HocKi.Generate());

    await _ct.HocKi.AddRangeAsync(hocKis);
    await _ct.SaveChangesAsync();
    return Ok();
  }

  [HttpPost("add-lop-hoc-phan")]
  public async Task<ActionResult> AddLopHocPhan()
  {
    List<HocPhan> hocPhans = await _ct.HocPhan.ToListAsync();
    List<HocKi> hocKis = await _ct.HocKi.ToListAsync();
    List<GiangVien> giangViens = await _ct.GiangVien.ToListAsync();

    if (hocPhans.Count == 0 || hocKis.Count == 0 || giangViens.Count == 0)
      return BadRequest("Chưa có Học phần, Học kỳ hoặc Giảng viên nào, hãy thêm chúng trước");

    var random = new Random();
    int lhp_ = await _ct.LopHocPhan.CountAsync();
    List<LopHocPhan> lopHocPhans = [];
    for (int i = 0; i < 10000; ++i)
    {
      try
      {
        HocPhan hp = hocPhans[random.Next(hocPhans.Count)];
        HocKi hk = hocKis[random.Next(hocKis.Count)];
        GiangVien? gv = random.NextDouble() > 0.5 ? giangViens[random.Next(giangViens.Count)] : null;

        LopHocPhan lopHocPhan = LopHocPhan.Generate(gv, hp, hk, lhp_ + i + 1);
        lopHocPhans.Add(lopHocPhan);
      }
      catch (Exception e)
      {
        Console.WriteLine(e);
        return BadRequest();
      }
    }
    await _ct.LopHocPhan.AddRangeAsync(lopHocPhans);
    await _ct.SaveChangesAsync();

    return Ok();
  }


  [HttpPost("add-he-so-cac-nam")]
  public ActionResult AddHeSo()
  {
    var namHoc =
      _ct.HocKi.GroupBy(i => i.ThoiGianBatDau.Year)
      .Select(c => new { c })
      .ToList();

    return Ok(namHoc);
  }

}