-- Script tạo database và bảng cho hệ thống quản lý giảng viên

-- Tạo bảng BangCap (Bằng cấp)
CREATE TABLE IF NOT EXISTS "BangCap" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaBangCap" VARCHAR(50) NOT NULL,
    "TenBangCap" VARCHAR(255) NOT NULL,
    "TenVietTat" VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_BangCap_MaBangCap" ON "BangCap" ("MaBangCap");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_BangCap_TenBangCap" ON "BangCap" ("TenBangCap");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_BangCap_TenVietTat" ON "BangCap" ("TenVietTat");

-- Tạo bảng ChucVu (Chức vụ)
CREATE TABLE IF NOT EXISTS "ChucVu" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaChucVu" VARCHAR(50) NOT NULL,
    "TenChucVu" VARCHAR(255) NOT NULL,
    "TenVietTat" VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_ChucVu_MaChucVu" ON "ChucVu" ("MaChucVu");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_ChucVu_TenChucVu" ON "ChucVu" ("TenChucVu");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_ChucVu_TenVietTat" ON "ChucVu" ("TenVietTat");

-- Tạo bảng Khoa
CREATE TABLE IF NOT EXISTS "Khoa" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaKhoa" VARCHAR(50) NOT NULL,
    "TenKhoa" VARCHAR(255) NOT NULL,
    "TenVietTat" VARCHAR(50) NOT NULL,
    "ViTri" VARCHAR(255) NOT NULL,
    "MoTa" TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Khoa_MaKhoa" ON "Khoa" ("MaKhoa");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_Khoa_TenKhoa" ON "Khoa" ("TenKhoa");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_Khoa_TenVietTat" ON "Khoa" ("TenVietTat");

-- Tạo bảng GiangVien (Giảng viên)
CREATE TABLE IF NOT EXISTS "GiangVien" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaGiangVien" VARCHAR(50) NOT NULL,
    "TenGiangVien" VARCHAR(255) NOT NULL,
    "GioiTinh" INTEGER NOT NULL,
    "SinhNhat" TIMESTAMP NOT NULL,
    "SoDienThoai" VARCHAR(20) NOT NULL,
    "Mail" VARCHAR(255) NOT NULL,
    "BangCapId" UUID NOT NULL,
    FOREIGN KEY ("BangCapId") REFERENCES "BangCap"("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_GiangVien_MaGiangVien" ON "GiangVien" ("MaGiangVien");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_GiangVien_SoDienThoai" ON "GiangVien" ("SoDienThoai");

-- Tạo bảng Khoa_GiangVien (Bảng trung gian)
CREATE TABLE IF NOT EXISTS "Khoa_GiangVien" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "GiangVienId" UUID NOT NULL,
    "KhoaId" UUID NOT NULL,
    "ChucVuId" UUID NOT NULL,
    FOREIGN KEY ("GiangVienId") REFERENCES "GiangVien"("Id") ON DELETE CASCADE,
    FOREIGN KEY ("KhoaId") REFERENCES "Khoa"("Id") ON DELETE CASCADE,
    FOREIGN KEY ("ChucVuId") REFERENCES "ChucVu"("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Khoa_GiangVien_KhoaId_GiangVienId" ON "Khoa_GiangVien" ("KhoaId", "GiangVienId");

-- Tạo bảng HocKi (Học kỳ)
CREATE TABLE IF NOT EXISTS "HocKi" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "TenKi" VARCHAR(100) NOT NULL,
    "ThoiGianBatDau" TIMESTAMP NOT NULL,
    "ThoiGianKetThuc" TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_HocKi_TenKi" ON "HocKi" ("TenKi");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_HocKi_TenKi_ThoiGianBatDau" ON "HocKi" ("TenKi", "ThoiGianBatDau");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_HocKi_ThoiGianKetThuc" ON "HocKi" ("ThoiGianKetThuc");

-- Tạo bảng HocPhan (Học phần)
CREATE TABLE IF NOT EXISTS "HocPhan" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaHocPhan" VARCHAR(50) NOT NULL,
    "TenHocPhan" VARCHAR(255) NOT NULL,
    "HeSoHocPhan" REAL NOT NULL,
    "SoTinChi" INTEGER NOT NULL DEFAULT 0,
    "SoTiet" INTEGER NOT NULL DEFAULT 0,
    "KhoaId" UUID NOT NULL,
    FOREIGN KEY ("KhoaId") REFERENCES "Khoa"("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_HocPhan_MaHocPhan" ON "HocPhan" ("MaHocPhan");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_HocPhan_TenHocPhan" ON "HocPhan" ("TenHocPhan");

-- Tạo bảng LopHocPhan (Lớp học phần)
CREATE TABLE IF NOT EXISTS "LopHocPhan" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "MaLop" VARCHAR(50) NOT NULL,
    "TenLop" VARCHAR(255) NOT NULL,
    "SoLuongSinhVien" INTEGER NOT NULL DEFAULT 0,
    "HocPhanId" UUID NOT NULL,
    "HocKiId" UUID NOT NULL,
    "GiangVienId" UUID,
    FOREIGN KEY ("HocPhanId") REFERENCES "HocPhan"("Id") ON DELETE CASCADE,
    FOREIGN KEY ("HocKiId") REFERENCES "HocKi"("Id") ON DELETE CASCADE,
    FOREIGN KEY ("GiangVienId") REFERENCES "GiangVien"("Id") ON DELETE SET NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_LopHocPhan_HocKiId_MaLop" ON "LopHocPhan" ("HocKiId", "MaLop");
CREATE UNIQUE INDEX IF NOT EXISTS "IX_LopHocPhan_HocKiId_TenLop" ON "LopHocPhan" ("HocKiId", "TenLop");

-- Tạo bảng DinhMucTien (Định mức tiền)
CREATE TABLE IF NOT EXISTS "DinhMucTien" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "SoTien" BIGINT NOT NULL,
    "NgayCapNhat" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "LyDo" TEXT
);

-- Tạo bảng HeSoLop (Hệ số lớp)
CREATE TABLE IF NOT EXISTS "HeSoLop" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "SoHocSinhToiThieu" INTEGER NOT NULL,
    "NamHoc" INTEGER NOT NULL,
    "HeSo" DOUBLE PRECISION NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_HeSoLop_SoHocSinhToiThieu_NamHoc" ON "HeSoLop" ("SoHocSinhToiThieu", "NamHoc");

-- Tạo bảng HeSoBangCap (Hệ số bằng cấp)
CREATE TABLE IF NOT EXISTS "HeSoBangCap" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "HeSo" DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    "Nam" INTEGER NOT NULL,
    "MaBangCap" UUID NOT NULL,
    FOREIGN KEY ("MaBangCap") REFERENCES "BangCap"("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_HeSoBangCap_Nam_MaBangCap" ON "HeSoBangCap" ("Nam", "MaBangCap");

-- Insert dữ liệu mẫu cho BangCap
INSERT INTO "BangCap" ("Id", "MaBangCap", "TenBangCap", "TenVietTat") VALUES
(gen_random_uuid(), 'DEG-1', 'Tiến sĩ', 'TS'),
(gen_random_uuid(), 'DEG-2', 'Thạc sĩ', 'ThS'),
(gen_random_uuid(), 'DEG-3', 'Cử nhân', 'CN'),
(gen_random_uuid(), 'DEG-4', 'Kỹ sư', 'KS')
ON CONFLICT DO NOTHING;

-- Insert dữ liệu mẫu cho ChucVu
INSERT INTO "ChucVu" ("Id", "MaChucVu", "TenChucVu", "TenVietTat") VALUES
(gen_random_uuid(), 'DEG-1', 'Trưởng khoa', 'TK'),
(gen_random_uuid(), 'DEG-2', 'Phó khoa', 'PK'),
(gen_random_uuid(), 'DEG-3', 'Giảng viên', 'GV'),
(gen_random_uuid(), 'DEG-4', 'Trợ giảng', 'TG')
ON CONFLICT DO NOTHING;

COMMIT;
