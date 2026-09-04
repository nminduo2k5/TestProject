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

  [HttpGet("seed-rich-data")]
  [HttpPost("seed-rich-data")]
  public async Task<ActionResult> SeedRichData()
  {
    // Clear existing data in correct FK order
    _ct.LopHocPhan.RemoveRange(await _ct.LopHocPhan.ToListAsync());
    _ct.HocPhan.RemoveRange(await _ct.HocPhan.ToListAsync());
    _ct.HocKi.RemoveRange(await _ct.HocKi.ToListAsync());
    _ct.Khoa_GiangVien.RemoveRange(await _ct.Khoa_GiangVien.ToListAsync());
    _ct.GiangVien.RemoveRange(await _ct.GiangVien.ToListAsync());
    _ct.BangCap.RemoveRange(await _ct.BangCap.ToListAsync());
    _ct.ChucVu.RemoveRange(await _ct.ChucVu.ToListAsync());
    _ct.Khoa.RemoveRange(await _ct.Khoa.ToListAsync());
    _ct.DinhMucTien.RemoveRange(await _ct.DinhMucTien.ToListAsync());
    _ct.HeSoBangCap.RemoveRange(await _ct.HeSoBangCap.ToListAsync());
    _ct.HeSoLop.RemoveRange(await _ct.HeSoLop.ToListAsync());
    await _ct.SaveChangesAsync();

    // 1. Khoa
    List<Khoa> khoas = [
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_CNTT", TenKhoa = "Khoa Công nghệ thông tin - DuongUniversity", TenVietTat = "DU-CNTT", ViTri = "Tầng 5 Tòa A", MoTa = "Đào tạo CNTT & Khoa học máy tính đỉnh cao" },
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_KTPM", TenKhoa = "Khoa Kỹ thuật phần mềm - DuongUniversity", TenVietTat = "DU-KTPM", ViTri = "Tầng 6 Tòa A", MoTa = "Chuyên ngành Phát triển & Kiểm thử phần mềm" },
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_AI", TenKhoa = "Khoa Trí tuệ nhân tạo - DuongUniversity", TenVietTat = "DU-AI", ViTri = "Tầng 4 Tòa A", MoTa = "Nghiên cứu AI, Machine Learning & Big Data" },
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_SPORT", TenKhoa = "Khoa Thể thao & Thể chất - DuongUniversity", TenVietTat = "DU-SPORT", ViTri = "Tầng 1 Tòa Thể thao", MoTa = "Đào tạo thể thao đỉnh cao & Huấn luyện viên" },
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_KT", TenKhoa = "Khoa Kinh tế & Quản trị - DuongUniversity", TenVietTat = "DU-KT", ViTri = "Tầng 3 Tòa C", MoTa = "Kinh tế số & Quản trị thương hiệu" },
      new() { Id = Guid.NewGuid(), MaKhoa = "DU_FAC_NN", TenKhoa = "Khoa Ngoại ngữ & Truyền thông - DuongUniversity", TenVietTat = "DU-NN", ViTri = "Tầng 1 Tòa D", MoTa = "Tiếng Anh thương mại & Truyền thông đa phương tiện" }
    ];
    await _ct.Khoa.AddRangeAsync(khoas);

    // 2. BangCap
    List<BangCap> bangCaps = [
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_GS", TenBangCap = "Giáo sư", TenVietTat = "GS" },
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_PGS", TenBangCap = "Phó Giáo sư", TenVietTat = "PGS" },
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_TS", TenBangCap = "Tiến sĩ", TenVietTat = "TS" },
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_THS", TenBangCap = "Thạc sĩ", TenVietTat = "ThS" },
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_CN", TenBangCap = "Cử nhân", TenVietTat = "CN" },
      new() { Id = Guid.NewGuid(), MaBangCap = "DEG_KS", TenBangCap = "Kỹ sư", TenVietTat = "KS" }
    ];
    await _ct.BangCap.AddRangeAsync(bangCaps);

    // 3. ChucVu
    List<ChucVu> chucVus = [
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_HT", TenChucVu = "Hiệu trưởng", TenVietTat = "HT" },
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_TK", TenChucVu = "Trưởng khoa", TenVietTat = "TK" },
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_PTK", TenChucVu = "Phó Trưởng khoa", TenVietTat = "PTK" },
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_TBM", TenChucVu = "Trưởng bộ môn", TenVietTat = "TBM" },
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_GVC", TenChucVu = "Giảng viên chính", TenVietTat = "GVC" },
      new() { Id = Guid.NewGuid(), MaChucVu = "POS_GV", TenChucVu = "Giảng viên", TenVietTat = "GV" }
    ];
    await _ct.ChucVu.AddRangeAsync(chucVus);
    await _ct.SaveChangesAsync();

    // 4. DinhMucTien
    List<DinhMucTien> dinhMucs = [
      new() { Id = Guid.NewGuid(), SoTien = 250000, NgayCapNhat = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc), LyDo = "Định mức thù lao tiết dạy mới DuongUniversity 2026" },
      new() { Id = Guid.NewGuid(), SoTien = 200000, NgayCapNhat = new DateTime(2025, 9, 1, 0, 0, 0, DateTimeKind.Utc), LyDo = "Cập nhật định mức năm học 2025-2026" },
      new() { Id = Guid.NewGuid(), SoTien = 180000, NgayCapNhat = new DateTime(2024, 9, 1, 0, 0, 0, DateTimeKind.Utc), LyDo = "Định mức năm học 2024-2025" },
      new() { Id = Guid.NewGuid(), SoTien = 150000, NgayCapNhat = new DateTime(2024, 1, 1, 0, 0, 0, DateTimeKind.Utc), LyDo = "Định mức khởi tạo ban đầu DuongUniversity" }
    ];
    await _ct.DinhMucTien.AddRangeAsync(dinhMucs);

    // 5. HeSoBangCap (2024, 2025, 2026)
    uint[] nams = [2024, 2025, 2026];
    List<HeSoBangCap> heSoBangCaps = [];
    foreach (var nam in nams)
    {
      foreach (var bc in bangCaps)
      {
        double hs = bc.TenVietTat switch
        {
          "GS" => 2.5,
          "PGS" => 2.0,
          "TS" => 1.6,
          "ThS" => 1.3,
          _ => 1.0
        };
        heSoBangCaps.Add(new HeSoBangCap { Id = Guid.NewGuid(), MaBangCap = bc.Id, Nam = nam, HeSo = hs });
      }
    }
    await _ct.HeSoBangCap.AddRangeAsync(heSoBangCaps);

    // 6. HeSoLop (2024, 2025, 2026)
    List<HeSoLop> heSoLops = [];
    foreach (var nam in nams)
    {
      heSoLops.Add(new HeSoLop { Id = Guid.NewGuid(), NamHoc = nam, SoHocSinhToiThieu = 20, HeSo = -0.2 });
      heSoLops.Add(new HeSoLop { Id = Guid.NewGuid(), NamHoc = nam, SoHocSinhToiThieu = 50, HeSo = 0.0 });
      heSoLops.Add(new HeSoLop { Id = Guid.NewGuid(), NamHoc = nam, SoHocSinhToiThieu = 70, HeSo = 0.20 });
      heSoLops.Add(new HeSoLop { Id = Guid.NewGuid(), NamHoc = nam, SoHocSinhToiThieu = 100, HeSo = 0.40 });
      heSoLops.Add(new HeSoLop { Id = Guid.NewGuid(), NamHoc = nam, SoHocSinhToiThieu = 150, HeSo = 0.60 });
    }
    await _ct.HeSoLop.AddRangeAsync(heSoLops);

    // 7. HocKi
    List<HocKi> hocKis = [
      new() { Id = Guid.NewGuid(), TenKi = "Học kỳ 1 (2024-2025)", ThoiGianBatDau = new DateTime(2024, 9, 1, 0, 0, 0, DateTimeKind.Utc), ThoiGianKetThuc = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc) },
      new() { Id = Guid.NewGuid(), TenKi = "Học kỳ 2 (2024-2025)", ThoiGianBatDau = new DateTime(2025, 2, 1, 0, 0, 0, DateTimeKind.Utc), ThoiGianKetThuc = new DateTime(2025, 6, 15, 0, 0, 0, DateTimeKind.Utc) },
      new() { Id = Guid.NewGuid(), TenKi = "Học kỳ 1 (2025-2026)", ThoiGianBatDau = new DateTime(2025, 9, 1, 0, 0, 0, DateTimeKind.Utc), ThoiGianKetThuc = new DateTime(2026, 1, 15, 0, 0, 0, DateTimeKind.Utc) },
      new() { Id = Guid.NewGuid(), TenKi = "Học kỳ 2 (2025-2026)", ThoiGianBatDau = new DateTime(2026, 2, 1, 0, 0, 0, DateTimeKind.Utc), ThoiGianKetThuc = new DateTime(2026, 6, 15, 0, 0, 0, DateTimeKind.Utc) },
      new() { Id = Guid.NewGuid(), TenKi = "Học kỳ 1 (2026-2027)", ThoiGianBatDau = new DateTime(2026, 9, 1, 0, 0, 0, DateTimeKind.Utc), ThoiGianKetThuc = new DateTime(2027, 1, 15, 0, 0, 0, DateTimeKind.Utc) }
    ];
    await _ct.HocKi.AddRangeAsync(hocKis);
    await _ct.SaveChangesAsync();

    // 8. GiangVien & Khoa_GiangVien (Các huyền thoại & giảng viên DuongUniversity - Cân bằng Nam & Nữ)
    var teacherData = new (string Ten, string Ma, string BC, string KhoaMa, string CV, int GioiTinh)[] {
      // Nam (GioiTinh = 0)
      ("GS.TS. Nguyễn Minh Dương", "DU_DUONG_01", "DEG_GS", "DU_FAC_CNTT", "POS_HT", 0),
      ("GS.TS. Lionel Messi", "DU_MESSI_10", "DEG_GS", "DU_FAC_SPORT", "POS_TK", 0),
      ("GS.TS. Cristiano Ronaldo", "DU_CR7_07", "DEG_GS", "DU_FAC_SPORT", "POS_PTK", 0),
      ("PGS.TS. Neymar Jr", "DU_NEYMAR_11", "DEG_PGS", "DU_FAC_KTPM", "POS_TBM", 0),
      ("TS. Kylian Mbappé", "DU_MBAPPE_09", "DEG_TS", "DU_FAC_CNTT", "POS_GVC", 0),
      ("GS.TS. Luka Modrić", "DU_MODRIC_10", "DEG_GS", "DU_FAC_AI", "POS_TK", 0),
      ("PGS.TS. Kevin De Bruyne", "DU_KDB_17", "DEG_PGS", "DU_FAC_AI", "POS_TBM", 0),
      ("TS. Erling Haaland", "DU_HAALAND_09", "DEG_TS", "DU_FAC_CNTT", "POS_GV", 0),
      ("GS.TS. Ronaldinho Gaúcho", "DU_R10_10", "DEG_GS", "DU_FAC_SPORT", "POS_GVC", 0),
      ("GS.TS. Zinedine Zidane", "DU_ZIZOU_05", "DEG_GS", "DU_FAC_KT", "POS_TK", 0),
      ("PGS.TS. Andrés Iniesta", "DU_INIESTA_08", "DEG_PGS", "DU_FAC_KTPM", "POS_TK", 0),
      ("ThS. Xavi Hernández", "DU_XAVI_06", "DEG_THS", "DU_FAC_KTPM", "POS_GV", 0),

      // Nữ (GioiTinh = 1)
      ("GS.TS. Alex Morgan", "DU_MORGAN_13", "DEG_GS", "DU_FAC_SPORT", "POS_GVC", 1),
      ("PGS.TS. Marta Vieira", "DU_MARTA_10", "DEG_PGS", "DU_FAC_SPORT", "POS_TBM", 1),
      ("TS. Aitana Bonmatí", "DU_BONMATI_14", "DEG_TS", "DU_FAC_KTPM", "POS_GVC", 1),
      ("GS.TS. Sam Kerr", "DU_KERR_20", "DEG_GS", "DU_FAC_CNTT", "POS_PTK", 1),
      ("PGS.TS. Megan Rapinoe", "DU_RAPINOE_15", "DEG_PGS", "DU_FAC_NN", "POS_TK", 1),
      ("TS. Alexia Putellas", "DU_PUTELLAS_11", "DEG_TS", "DU_FAC_AI", "POS_GVC", 1),
      ("ThS. Lucy Bronze", "DU_BRONZE_02", "DEG_THS", "DU_FAC_AI", "POS_GV", 1),
      ("PGS.TS. Nguyễn Thị Mai", "DU_MAI_01", "DEG_PGS", "DU_FAC_KT", "POS_PTK", 1),
      ("TS. Trần Thu Hà", "DU_HA_02", "DEG_TS", "DU_FAC_KT", "POS_GV", 1),
      ("ThS. Phạm Hoàng Yến", "DU_YEN_03", "DEG_THS", "DU_FAC_NN", "POS_GV", 1)
    };

    List<GiangVien> giangViens = [];
    List<Khoa_GiangVien> kgvs = [];

    foreach (var (ten, ma, bcMa, khoaMa, cvMa, gioiTinh) in teacherData)
    {
      var bc = bangCaps.First(b => b.MaBangCap == bcMa);
      var k = khoas.First(f => f.MaKhoa == khoaMa);
      var cv = chucVus.First(c => c.MaChucVu == cvMa);

      var gv = new GiangVien
      {
        Id = Guid.NewGuid(),
        MaGiangVien = ma,
        TenGiangVien = ten,
        GioiTinh = gioiTinh,
        SinhNhat = new DateTime(1988, 6, 24, 0, 0, 0, DateTimeKind.Utc),
        Mail = $"{ma.ToLower()}@duonguniversity.edu.vn",
        SoDienThoai = $"09{Random.Shared.Next(10000000, 99999999)}",
        BangCapId = bc.Id
      };
      giangViens.Add(gv);

      kgvs.Add(new Khoa_GiangVien
      {
        Id = Guid.NewGuid(),
        GiangVienId = gv.Id,
        KhoaId = k.Id,
        ChucVuId = cv.Id
      });
    }

    await _ct.GiangVien.AddRangeAsync(giangViens);
    await _ct.Khoa_GiangVien.AddRangeAsync(kgvs);
    await _ct.SaveChangesAsync();

    // 9. HocPhan (Học phần phong phú cho DuongUniversity)
    var hocPhanData = new (string Ten, string Ma, uint SoTiet, uint SoTinChi, float HeSo, string KhoaMa)[] {
      ("Lập trình Hướng đối tượng (OOP)", "DU_HP_OOP", 45, 3, 1.2f, "DU_FAC_CNTT"),
      ("Cấu trúc dữ liệu & Giải thuật", "DU_HP_DSA", 45, 3, 1.5f, "DU_FAC_CNTT"),
      ("Trí tuệ nhân tạo & Machine Learning", "DU_HP_AI", 45, 3, 2.0f, "DU_FAC_CNTT"),
      ("Bảo mật & An toàn thông tin", "DU_HP_SEC", 30, 2, 1.4f, "DU_FAC_CNTT"),

      ("Phát triển Web Fullstack (React & .NET)", "DU_HP_WEB", 45, 3, 1.6f, "DU_FAC_KTPM"),
      ("Nhập môn Kỹ thuật phần mềm", "DU_HP_SE", 30, 2, 1.1f, "DU_FAC_KTPM"),
      ("Kiểm thử & Đảm bảo chất lượng phần mềm", "DU_HP_TEST", 45, 3, 1.3f, "DU_FAC_KTPM"),
      ("Kiến trúc phần mềm & Microservices", "DU_HP_ARCH", 45, 3, 1.8f, "DU_FAC_KTPM"),

      ("Hệ quản trị CSDL & Big Data Analytics", "DU_HP_BIGDATA", 45, 3, 1.8f, "DU_FAC_AI"),
      ("Deep Learning & Computer Vision", "DU_HP_DL", 45, 3, 2.0f, "DU_FAC_AI"),
      ("Khai phá dữ liệu (Data Mining)", "DU_HP_MINING", 30, 2, 1.5f, "DU_FAC_AI"),

      ("Chiến thuật bóng đá & Thể thao đại cương", "DU_HP_FOOTBALL", 45, 3, 2.0f, "DU_FAC_SPORT"),
      ("Kỹ thuật sút phạt & Đi bóng nghệ thuật", "DU_HP_SKILLS", 30, 2, 1.8f, "DU_FAC_SPORT"),
      ("Huấn luyện viên & Quản trị đội bóng", "DU_HP_COACH", 45, 3, 1.5f, "DU_FAC_SPORT"),

      ("Kinh tế vĩ mô & Vi mô hiện đại", "DU_HP_ECON", 30, 2, 1.0f, "DU_FAC_KT"),
      ("Quản trị tài chính & Đầu tư", "DU_HP_FIN", 45, 3, 1.3f, "DU_FAC_KT"),
      ("Marketing toàn cầu & Branding", "DU_HP_MKT", 45, 3, 1.4f, "DU_FAC_KT"),

      ("Tiếng Anh giao tiếp nâng cao", "DU_HP_ENG", 45, 3, 1.2f, "DU_FAC_NN"),
      ("Truyền thông đa phương tiện & PR", "DU_HP_PR", 30, 2, 1.3f, "DU_FAC_NN")
    };

    List<HocPhan> hocPhans = [];
    foreach (var (ten, ma, soTiet, stc, hs, khoaMa) in hocPhanData)
    {
      var k = khoas.First(f => f.MaKhoa == khoaMa);
      hocPhans.Add(new HocPhan
      {
        Id = Guid.NewGuid(),
        MaHocPhan = ma,
        TenHocPhan = ten,
        SoTiet = soTiet,
        SoTinChi = stc,
        HeSoHocPhan = hs,
        KhoaId = k.Id
      });
    }
    await _ct.HocPhan.AddRangeAsync(hocPhans);
    await _ct.SaveChangesAsync();

    // 10. LopHocPhan (Phân công giảng viên cho các kỳ 2024, 2025, 2026 - Tạo 350+ lớp học phần)
    List<LopHocPhan> lhpList = [];
    int classCounter = 1;

    foreach (var hk in hocKis)
    {
      foreach (var hp in hocPhans)
      {
        var facultyTeachers = kgvs.Where(k => k.KhoaId == hp.KhoaId).Select(k => k.GiangVienId).ToList();
        if (facultyTeachers.Count == 0) continue;

        // Generate 3 to 6 classes per subject per semester for DuongUniversity
        int numClasses = Random.Shared.Next(3, 7);
        for (int c = 1; c <= numClasses; c++)
        {
          var gvId = facultyTeachers[Random.Shared.Next(facultyTeachers.Count)];
          uint svCount = (uint)Random.Shared.Next(30, 140);

          lhpList.Add(new LopHocPhan
          {
            Id = Guid.NewGuid(),
            MaLop = $"{hp.MaHocPhan}_N{c:D2}_{classCounter++}",
            TenLop = $"{hp.TenHocPhan} (Nhóm {c:D2})",
            HocKiId = hk.Id,
            HocPhanId = hp.Id,
            GiangVienId = gvId,
            SoLuongSinhVien = svCount
          });
        }
      }
    }

    await _ct.LopHocPhan.AddRangeAsync(lhpList);
    await _ct.SaveChangesAsync();

    return Ok(new
    {
      Message = "Khởi tạo dữ liệu DuongUniversity siêu phong phú thành công!",
      Truong = "DuongUniversity",
      KhoaCount = khoas.Count,
      GiangVienCount = giangViens.Count,
      GiangVienTieuBieu = new[] { "Lionel Messi", "Cristiano Ronaldo", "Neymar Jr", "Kylian Mbappé", "Luka Modrić", "Nguyễn Minh Dương" },
      HocPhanCount = hocPhans.Count,
      HocKiCount = hocKis.Count,
      LopHocPhanCount = lhpList.Count,
      DinhMucCount = dinhMucs.Count
    });
  }

}