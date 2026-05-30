using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Npgsql;
using System.Collections;
using server.Models;
using server.Repositories;
using Microsoft.AspNetCore.Http.HttpResults;

namespace server.Controllers;

[ApiController]
[Route("[controller]")]
public class LopHocPhanController(AppDbContext context, IConfiguration configuration) : ControllerBase
{
   readonly AppDbContext _ct = context;
   readonly string _connection = configuration.GetConnectionString("DefaultConnection")!;

   // Thống kê lớp học phần đang mở
   [HttpGet("thong-ke-lop-hoc-phan-dang-mo")]
   public async Task<ActionResult> ThongKeLopDangMo()
   {
      var dangMoList = await _ct.LopHocPhan
          // .Where(l => l.TrangThai.ToString() == "DangMo")
          .Include(l => l.HocPhan)
          .Include(l => l.HocKi)
          .ToListAsync();

      return Ok(dangMoList);
   }

   // Lấy tất cả lớp học phần
   [HttpGet]
   public async Task<ActionResult<ICollection>> Get()
   {
      using var conn = new NpgsqlConnection(_connection);
      await conn.OpenAsync();

      string query = """
      SELECT 
            lhp."Id",
            lhp."MaLop",
            lhp."TenLop",
            lhp."SoLuongSinhVien",
            hp."Id" hocPhanId,
            hp."MaHocPhan",
            hp."TenHocPhan",
            hp."SoTinChi",
            hp."SoTiet",
            k."Id" khoaId,
            k."MaKhoa",
            k."TenKhoa",
            k."TenVietTat",
            lhp."GiangVienId",
            gv."TenGiangVien",
            hk."Id" hocKiId,
            hk."ThoiGianBatDau",
            hk."ThoiGianKetThuc"
      FROM "LopHocPhan" lhp
      LEFT JOIN "GiangVien" gv ON gv."Id" = lhp."GiangVienId"
      INNER JOIN "HocPhan" hp ON hp."Id" = lhp."HocPhanId"
      INNER JOIN "Khoa" k ON k."Id" = hp."KhoaId"
      INNER JOIN "HocKi" hk ON hk."Id" = lhp."HocKiId"
      ORDER BY hk."ThoiGianBatDau" DESC;
""";
      List<object> nam = [];
      using var cmd = new NpgsqlCommand(query, conn);
      using var reader = cmd.ExecuteReader();
      while (reader.Read())
      {
         Guid? GiangVienId = reader.IsDBNull(13) ? null : reader.GetGuid(13);
         string? TenGiangVien = reader.IsDBNull(14) ? null : reader.GetString(14);

         nam.Add(new
         {
            Id = reader.GetGuid(0),
            MaLop = reader.GetString(1),
            TenLop = reader.GetString(2),
            SoLuongSinhVien = reader.GetInt32(3),
            HocPhanId = reader.GetGuid(4),
            MaHocPhan = reader.GetString(5),
            TenHocPhan = reader.GetString(6),
            SoTinChi = reader.GetInt32(7),
            SoTiet = reader.GetInt32(8),
            KhoaId = reader.GetGuid(9),
            MaKhoa = reader.GetString(10),
            TenKhoa = reader.GetString(11),
            TenVietTat = reader.GetString(12),
            GiangVienId,
            TenGiangVien,
            HocKiId = reader.GetGuid(15),
            ThoiGianBatDau = reader.GetDateTime(16),
            ThoiGianKetThuc = reader.GetDateTime(17)
         });
      }

      return Ok(nam);
   }

   // Sửa thông tin lớp học phần
   [HttpPut("sua-thong-tin")]
   public async Task<IActionResult> SuaThongTin([FromBody] UpdateLopHocPhanDto dto)
   {
      var lop = await _ct.LopHocPhan.FindAsync(dto.Id);
      if (lop == null) return NotFound();

      lop.SoLuongSinhVien = dto.SoLuongSinhVien;
      lop.HocKiId = dto.HocKiId;
      lop.HocPhanId = dto.HocPhanId;

      await _ct.SaveChangesAsync();

      return Ok(lop);
   }

   [HttpPost("cap-nhat-trang-thai/{id}")]
   public async Task<IActionResult> CapNhatTrangThai(Guid id)
   {
      var lop = await _ct.LopHocPhan.Include(l => l.HocKi).FirstOrDefaultAsync(l => l.Id == id);
      if (lop == null) return NotFound();

      // lop.TrangThai = LopHocPhanDto.XacDinhTrangThai(lop);
      await _ct.SaveChangesAsync();

      return Ok(lop);
   }

   // Thêm lớp học phần mới
   [HttpPost("them-hoc-phan")]
   public async Task<IActionResult> Create(LopHocPhanInput dto)
   {
      var hocKi = await _ct.HocKi.FindAsync(dto.HocKiId);
      if (hocKi == null) return BadRequest("Học kỳ không tồn tại");

      var hocPhan = await _ct.HocPhan.FindAsync(dto.HocPhanId);
      if (hocPhan == null) return BadRequest("Học phần không tồn tại");

      // var exists = await _ct.LopHocPhan.AnyAsync(l => l.MaLop == dto.MaLop);
      // if (exists) return BadRequest("Mã lớp đã tồn tại");

      int hocPhanCount = await _ct.LopHocPhan.CountAsync(l => l.HocPhanId == dto.HocPhanId && l.HocKiId == dto.HocKiId);

      var lop = new LopHocPhan
      {
         MaLop = $"{hocPhan.MaHocPhan}_{(hocPhanCount + 1).ToString().PadLeft(2, '0')}",
         TenLop = $"{hocPhan.TenHocPhan} (N{(hocPhanCount + 1).ToString().PadLeft(2, '0')})",
         SoLuongSinhVien = dto.SoLuongSinhVien,
         HocKiId = dto.HocKiId,
         HocPhanId = dto.HocPhanId,
         GiangVienId = dto.GiangVienId
      };
      // lop.TrangThai = LopHocPhanDto.XacDinhTrangThai(lop);

      _ct.LopHocPhan.Add(lop);
      await _ct.SaveChangesAsync();

      return Ok(lop);
   }

   // Xoá lớp học phần
   [HttpDelete("xoa/{id}")]
   public async Task<IActionResult> XoaLopHocPhan(Guid id)
   {
      var lop = await _ct.LopHocPhan.FindAsync(id);
      if (lop == null) return NotFound();
      _ct.LopHocPhan.Remove(lop);
      await _ct.SaveChangesAsync();

      return Ok();
   }

   // Phân công giảng viên giảng dạy
   [HttpPost("phan-cong-giang-vien")]
   public async Task<IActionResult> PhanCongGiangVien([FromBody] PhanCongGiangVienDto dto)
   {
      var lop = await _ct.LopHocPhan.FindAsync(dto.LopHocPhanId);
      if (lop == null) return NotFound("Lớp học phần không tồn tại");

      var giangVien = await _ct.GiangVien.FindAsync(dto.GiangVienId);
      if (giangVien == null) return NotFound("Giảng viên không tồn tại");

      lop.GiangVienId = dto.GiangVienId;
      await _ct.SaveChangesAsync();

      return Ok(lop);
   }
}

public class LopHocPhanInput
{
   public uint SoLuongSinhVien { get; set; } = 0!;
   public Guid HocPhanId { get; set; }
   public Guid HocKiId { get; set; }
   public Guid? GiangVienId { get; set; }
}