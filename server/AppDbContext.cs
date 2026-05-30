using Microsoft.EntityFrameworkCore;
using server.Models;

namespace server;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
  public DbSet<BangCap> BangCap { get; set; }
  public DbSet<ChucVu> ChucVu { get; set; }
  public DbSet<GiangVien> GiangVien { get; set; }
  public DbSet<Khoa> Khoa { get; set; }
  public DbSet<Khoa_GiangVien> Khoa_GiangVien { get; set; }
  public DbSet<HocKi> HocKi { get; set; }
  public DbSet<HocPhan> HocPhan { get; set; }
  public DbSet<DinhMucTien> DinhMucTien { get; set; }
  public DbSet<HeSoLop> HeSoLop { get; set; }
  public DbSet<LopHocPhan> LopHocPhan { get; set; }
  public DbSet<HeSoBangCap> HeSoBangCap { get; set; }

  protected override void OnModelCreating(ModelBuilder modelBuilder)
  {
    modelBuilder.Entity<BangCap>().HasIndex(b => b.MaBangCap).IsUnique();
    modelBuilder.Entity<BangCap>().HasIndex(b => b.TenBangCap).IsUnique();
    modelBuilder.Entity<BangCap>().HasIndex(b => b.TenVietTat).IsUnique();

    modelBuilder.Entity<ChucVu>().HasIndex(b => b.MaChucVu).IsUnique();
    modelBuilder.Entity<ChucVu>().HasIndex(b => b.TenChucVu).IsUnique();
    modelBuilder.Entity<ChucVu>().HasIndex(b => b.TenVietTat).IsUnique();

    modelBuilder.Entity<GiangVien>().HasIndex(b => b.MaGiangVien).IsUnique();
    modelBuilder.Entity<GiangVien>().HasIndex(b => b.SoDienThoai).IsUnique();
    modelBuilder.Entity<GiangVien>().HasOne(e => e.BangCap).WithMany(e => e.GiangViens).HasForeignKey(e => e.BangCapId);

    modelBuilder.Entity<Khoa>().HasIndex(b => b.MaKhoa).IsUnique();
    modelBuilder.Entity<Khoa>().HasIndex(b => b.TenKhoa).IsUnique();
    modelBuilder.Entity<Khoa>().HasIndex(b => b.TenVietTat).IsUnique();

    modelBuilder.Entity<HocKi>().HasIndex(b => b.TenKi).IsUnique();

    modelBuilder.Entity<Khoa_GiangVien>().HasIndex(k => new { k.KhoaId, k.GiangVienId }).IsUnique();
    modelBuilder.Entity<Khoa_GiangVien>().HasOne(e => e.GiangVien).WithMany(s => s.Khoa_GiangViens).HasForeignKey(e => e.GiangVienId);
    modelBuilder.Entity<Khoa_GiangVien>().HasOne(e => e.ChucVu).WithMany(c => c.Khoa_GiangViens).HasForeignKey(e => e.ChucVuId);
    modelBuilder.Entity<Khoa_GiangVien>().HasOne(e => e.Khoa).WithMany(k => k.Khoa_GiangViens).HasForeignKey(e => e.KhoaId);


    base.OnModelCreating(modelBuilder);

    //UC 2
    modelBuilder.Entity<HocKi>().HasIndex(b => new { b.TenKi, b.ThoiGianBatDau }).IsUnique();
    // modelBuilder.Entity<HocKi>().HasIndex(b => ).IsUnique();
    modelBuilder.Entity<HocKi>().HasIndex(b => b.ThoiGianKetThuc).IsUnique();

    // modelBuilder.Entity<TinChi>().HasIndex(b => b.LoaiTinChi).IsUnique();

    modelBuilder.Entity<HocPhan>().HasIndex(b => b.MaHocPhan).IsUnique();
    modelBuilder.Entity<HocPhan>().HasIndex(b => b.TenHocPhan).IsUnique();

    modelBuilder.Entity<LopHocPhan>().HasIndex(b => new { b.HocKiId, b.MaLop }).IsUnique();
    modelBuilder.Entity<LopHocPhan>().HasIndex(b => new { b.HocKiId, b.TenLop }).IsUnique();


    modelBuilder.Entity<HeSoLop>().HasIndex(b => new { b.SoHocSinhToiThieu, b.NamHoc }).IsUnique(true);

    modelBuilder.Entity<HeSoBangCap>().HasOne(i => i.BangCap).WithMany(b => b.HeSoBangCap).HasForeignKey(i => i.MaBangCap);
    modelBuilder.Entity<HeSoBangCap>().HasIndex(i => new { i.Nam, i.MaBangCap }).IsUnique(true);
  }
}