# 🎓 HỆ THỐNG QUẢN LÝ GIẢNG VIÊN, LỚP HỌC PHẦN & TÍNH TIỀN DẠY - DUONGUNIVERSITY

> **Hệ thống Quản lý Giảng dạy & Tính Thù lao Giảng viên (DuongUniversity)** là giải pháp phần mềm toàn diện hỗ trợ quản lý thông tin giảng viên, danh mục khoa/viện, học phần, lớp học phần, phân công giảng dạy, cấu hình định mức - hệ số quy đổi và tự động hóa quá trình tính toán thù lao giảng dạy kèm tính năng xuất báo cáo Excel chuyên nghiệp.

---

## 📋 MỤC LỤC

1. [Giới thiệu & Kiến trúc Hệ thống](#-giới-thiệu--kiến-trúc-hệ-thống)
2. [Các Tính Năng Chính](#-các-tính-năng-chính)
3. [Chi Tiết Các Lỗi Đã Khắc Phục & Tối Ưu](#-chi-tiết-các-lỗi-đã-khắc-phục--tối-ưu)
4. [Dữ Liệu Mẫu Phong Phú (DuongUniversity Seed Data)](#-dữ-liệu-mẫu-phong-phú-duonguniversity-seed-data)
5. [Công Nghệ Sử Dụng (Tech Stack)](#-công-nghệ-sử-dụng-tech-stack)
6. [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
7. [Mô Hình Dữ Liệu (Database Schema)](#-mô-hình-dữ-liệu-database-schema)
8. [Hướng Dẫn Cài Đặt & Khởi Chạy](#-hướng-dẫn-cài-đặt--khởi-chạy)
9. [Kiểm Thử Tự Động (Automated Testing)](#-kiểm-thử-tự-động-automated-testing)
10. [Tài Liệu Liên Quan](#-tài-liệu-liên-quan)

---

## 🌟 GIỚI THIỆU & KIẾN TRÚC HỆ THỐNG

Dự án **TestProject (DuongUniversity Management System)** được xây dựng với kiến trúc Client-Server hiện đại, đáp ứng các tiêu chí minh bạch, chính xác và hiệu quả trong công tác quản lý đào tạo đại học.

- **Frontend (Client):** Xây dựng bằng React 19 + Vite 6 + Ant Design v5 + Tailwind CSS v4, cung cấp giao diện người dùng tương tác cao, mượt mà và trực quan.
- **Backend (Server):** Xây dựng trên nền .NET 9 Web API (C#) + Entity Framework Core 9 + PostgreSQL Database Engine, cung cấp hệ thống RESTful API mạnh mẽ với Swagger UI.
- **Testing:** Tích hợp bộ kiểm thử tự động toàn diện với Selenium WebDriver (NUnit 4) áp dụng mô hình Page Object Model (POM) và API Automation Tests.

---

## ⚙️ CÁC TÍNH NĂNG CHÍNH

### 1. 👨‍🏫 Quản lý Giảng viên & Tổ chức
- Quản lý danh sách giảng viên (mã GV, họ tên, email, sđt, khoa/bộ môn).
- Quản lý danh mục Bằng cấp (Cử nhân, Thạc sĩ, Tiến sĩ, Phó Giáo sư, Giáo sư...) và Chức vụ (Hiệu trưởng, Trưởng khoa, Phó Trưởng khoa, Trưởng bộ môn, Giảng viên chính...).
- Phân quyền/gán giảng viên vào các Khoa/Viện tương ứng.

### 2. 📚 Quản lý Học kỳ & Học phần
- Quản lý thông tin Học kỳ (Tên kỳ, thời gian bắt đầu, thời gian kết thúc).
- Quản lý danh mục Học phần (Mã HP, tên học phần, số tín chỉ, số tiết lý thuyết/thực hành, hệ số học phần).
- Quản lý Lớp học phần theo từng học kỳ (mã lớp, sĩ số sinh viên, trạng thái).

### 3. 🎯 Phân công Giảng dạy (Lớp Học Phần)
- Lọc danh sách lớp học phần theo Khoa, Học kỳ, Năm học và Trạng thái phân công.
- Phân công giảng viên cho một hoặc nhiều lớp học phần đồng thời.
- **Validation & Ràng buộc:** Chỉ cho phép phân công giảng viên thuộc cùng Khoa và khi học kỳ chưa bắt đầu.

### 4. 💰 Cấu hình Hệ số & Tính Tiền Dạy (`/tinh-tien-day`, `/dinh-muc-tien`, `/he-so-tinh-tien`)
- **[Thiết lập định mức tiền theo tiết](http://localhost:5173/dinh-muc-tien):** Cấu hình đơn giá 1 tiết chuẩn (VNĐ), lưu vết lịch sử cập nhật và lý do điều chỉnh.
- **[Hệ số tính tiền](http://localhost:5173/he-so-tinh-tien):** Quản lý **Hệ số quy mô lớp (HeSoLop)** theo số sinh viên và năm học; quản lý **Hệ số bằng cấp (HeSoBangCap)** theo trình độ chuyên môn và năm áp dụng.
- **[Thống kê tiền dạy](http://localhost:5173/tinh-tien-day):** Tự động tính toán tổng số tiền thù lao giảng dạy cho giảng viên theo công thức chuẩn:
  $$\text{Số tiết quy đổi} = \text{Số tiết thực tế} \times (\text{Hệ số học phần} + \text{Hệ số quy mô lớp})$$
  $$\text{Tiền dạy lớp} = \text{Số tiết quy đổi} \times \text{Hệ số bằng cấp} \times \text{Định mức tiền chuẩn}$$
- Đã bổ sung tính năng chọn **"Tất cả học kỳ"** để tính tổng thù lao cả năm học, xem Modal chi tiết các lớp dạy và xuất báo cáo file Excel (`.xlsx`).

### 5. 📊 Thống kê Lớp Học Phần (`/thong-ke-so-lop`)
- Thống kê tổng số lớp mở, tổng số sinh viên, số sinh viên trung bình/lớp và tổng số học phần.
- Lọc dữ liệu linh hoạt theo **Khoa, Năm học, Kỳ học**.
- Nút **"Thống kê"** cập nhật dữ liệu tự động từ backend API.
- Nút **"Xuất báo cáo"** xuất bảng dữ liệu thống kê theo học phần ra file Excel (`.xlsx`).

---

## 🛠 CHI TIẾT CÁC LỖI ĐÃ KHẮC PHỤC & TỐI ƯU

| Trang / Module | Lỗi Phát Hiện | Nguyên Nhân | Giải Pháp Khắc Phục |
| :--- | :--- | :--- | :--- |
| **Thống kê tiền dạy** (`/tinh-tien-day`) | Giảng viên dạy nhiều lớp bị tính thiếu tổng tiền ở bảng chính | Lặp danh sách nhưng chỉ tính `tienDay` của duy nhất 1 lớp đầu tiên | Đã sửa `useMemo` trong [`TienDayGiangVien.jsx`](file:///k:/TestProject/client/src/Pages/TinhTienDay/TienDayGiangVien.jsx) để cộng dồn chính xác `tienDay += tienDayCuaLop` |
| **Thống kê tiền dạy** (`/tinh-tien-day`) | File Excel xuất ra bị nhầm Mã giảng viên thành chuỗi Guid ID | Mapping nhầm thuộc tính `id` thay vì `maGiangVien` | Chuẩn hóa bảng mapping xuất Excel sang tiêu đề tiếng Việt chuẩn |
| **Định mức tiền** (`/dinh-muc-tien`) | Cảnh báo / Crash khi CSDL chưa có dữ liệu định mức | Truy cập trực tiếp `data[0]` khi mảng rỗng và render thiếu fallback | Thêm kiểm tra an toàn `data && data.length > 0 ? [data[0]] : []` và sửa trùng `key` cột table |
| **Hệ số tính tiền** (`/he-so-tinh-tien`) | Xóa hệ số lớp bị load nhầm dữ liệu tất cả các năm | Callback sau khi xóa gọi API `GetHeSoLopHocPhan()` | Sửa gọi `GetHeSoLopHocPhanTheoNam({ nam: selectedNamHoc })` trong [`HeSoLop.jsx`](file:///k:/TestProject/client/src/Pages/TinhTienDay/HeSoLop.jsx) |
| **Thống kê lớp học phần** (`/thong-ke-so-lop`) | Nút **"Thống kê"** và **"Xuất báo cáo"** bấm không có phản hồi | Thiếu sự kiện `onClick` ở 2 nút bấm trong [`FilterSection.jsx`](file:///k:/TestProject/client/src/Pages/ThongKeLopPage/FilterSection.jsx) | Gán hàm `onClick={handleThongKe}` và `onClick={exportToExcel}` kèm hiệu ứng loading |
| **Thống kê lớp học phần** (`/thong-ke-so-lop`) | Thẻ chỉ số "Số học phần" hiển thị sai số liệu khi lọc theo Khoa | Lấy nhầm `filteredData[0]?.soLopHocPhan` trong [`OverallStats.jsx`](file:///k:/TestProject/client/src/Pages/ThongKeLopPage/OverallStats.jsx) | Sửa lại thành `filteredData.length` đếm chính xác số học phần thuộc Khoa đó |

---

## ⚽ DỮ LIỆU MẪU PHONG PHÚ (DUONGUNIVERSITY SEED DATA)

Hệ thống đã tích hợp bộ API Seed dữ liệu mẫu **DuongUniversity** tại endpoint: `GET/POST http://localhost:5249/Test/seed-rich-data`

### 📊 Thống kê quy mô CSDL:
- **Tên trường:** `DuongUniversity`
- **Tổng số Lớp học phần:** **423 lớp** (năm học 2024, 2025, 2026)
- **Số tín chỉ học phần:** **Chỉ từ 2 hoặc 3 tín chỉ** (Chuẩn 30 - 45 tiết giảng dạy)
- **Tỷ lệ Giới tính:** **Cân bằng 50% Nam / 50% Nữ** (22 Giảng viên tiêu biểu Nam & Nữ)
- **Tổng số Học phần:** **19 môn học**
- **Tổng số Học kỳ:** **5 học kỳ** (từ 2024 đến 2027)

### 🌟 Danh sách Giảng viên tiêu biểu (Nam & Nữ):
1. 👨‍🏫 **GS.TS. Nguyễn Minh Dương** (`DU_DUONG_01`) - *Hiệu trưởng DuongUniversity / Khoa CNTT*
2. ⚽ **GS.TS. Lionel Messi** (`DU_MESSI_10`) - *Trưởng Khoa Thể thao & Thể chất*
3. ⚽ **GS.TS. Cristiano Ronaldo** (`DU_CR7_07`) - *Phó Trưởng Khoa Thể thao & Thể chất*
4. 👩‍🏫 **GS.TS. Alex Morgan** (`DU_MORGAN_13`) - *Giảng viên chính Khoa Thể thao*
5. ⚽ **PGS.TS. Neymar Jr** (`DU_NEYMAR_11`) - *Trưởng Bộ môn Kỹ thuật Phần mềm*
6. 👩‍🏫 **PGS.TS. Marta Vieira** (`DU_MARTA_10`) - *Trưởng Bộ môn Thể thao*
7. ⚽ **TS. Kylian Mbappé** (`DU_MBAPPE_09`) - *Giảng viên chính Khoa CNTT*
8. 👩‍🏫 **TS. Aitana Bonmatí** (`DU_BONMATI_14`) - *Giảng viên chính Khoa KTPM*
9. ⚽ **GS.TS. Luka Modrić** (`DU_MODRIC_10`) - *Trưởng Khoa Trí tuệ Nhân tạo*
10. 👩‍🏫 **GS.TS. Sam Kerr** (`DU_KERR_20`) - *Phó Trưởng Khoa CNTT*
11. ⚽ **PGS.TS. Kevin De Bruyne** (`DU_KDB_17`), 👩‍🏫 **PGS.TS. Megan Rapinoe**, ⚽ **TS. Erling Haaland**, 👩‍🏫 **TS. Alexia Putellas**, ⚽ **GS.TS. Ronaldinho Gaúcho**, 👩‍🏫 **ThS. Lucy Bronze**, ⚽ **GS.TS. Zinedine Zidane**, 👩‍🏫 **PGS.TS. Nguyễn Thị Mai**...

---

## 🛠 CÔNG NGHỆ SỬ DỤNG (TECH STACK)

### **Backend**
- **Framework:** .NET 9.0 Web API (C#)
- **ORM:** Entity Framework Core 9.0
- **Database:** PostgreSQL (Npgsql 9.0)
- **Documentation:** OpenAPI / Swagger UI
- **JSON Serialization:** Newtonsoft.Json

### **Frontend**
- **Framework:** React 19 + Vite 6
- **UI Components:** Ant Design (antd v5)
- **Styling:** Tailwind CSS v4
- **Icons:** Lucide React, FontAwesome Icons
- **HTTP Client:** Axios
- **Data Visualization:** Recharts
- **Excel Export:** XLSX (`0.18.5`), FileSaver (`2.0.5`)

### **Automated Testing**
- **UI Test Framework:** NUnit 4 + Selenium WebDriver 4.33 (MSEdgeDriver)
- **API Test Framework:** NUnit 4 (.NET 9.0)
- **Design Pattern:** Page Object Model (POM)

---

## 📁 CẤU TRÚC DỰ ÁN

```text
TestProject/
├── server/                     # Backend API (.NET 9)
│   ├── Controllers/            # API Controllers (GiangVien, LopHocPhan, TinhTienDay, Test...)
│   ├── Models/                 # EF Core Entities (GiangVien, LopHocPhan, DinhMucTien...)
│   ├── Repositories/           # Data Repositories & Business Logic
│   ├── AppDbContext.cs         # Database Context configuration
│   ├── Program.cs              # Application Entry & Services DI
│   └── create_tables.sql       # Script khởi tạo CSDL PostgreSQL
│
├── client/                     # Frontend App (React 19 + Vite 6)
│   ├── src/
│   │   ├── api/                # Axios API Service Modules (tinhTienDay, lhpThongKeApi...)
│   │   ├── components/         # Reusable UI Components
│   │   ├── Pages/              # Các trang chức năng
│   │   │   ├── TinhTienDay/    # TienDayGiangVien, DinhMucTien, HeSoLop
│   │   │   ├── ThongKeLopPage/ # Index, FilterSection, OverallStats, DataTable, context
│   │   │   ├── LopHocPhanPage/ # Trang quản lý & phân công lớp học phần
│   │   │   └── GiangVienPage/  # Trang quản lý danh sách giảng viên
│   │   └── App.jsx             # React Router Setup (Routes configuration)
│   ├── package.json            # Dependencies & npm scripts
│   └── vite.config.js          # Config Vite Server
│
├── tests/                      # Bộ Kiểm Thử Tự Động
│   ├── APITests/               # Integration & Unit Tests cho REST API
│   └── UITests/                # Automation Tests Selenium cho UI Frontend
│       ├── Drivers/            # WebDriver Factory (Edge / Chrome)
│       └── Pages/              # Page Object Model pattern
│
├── document/                   # Tài liệu thiết kế & phân tích hệ thống
├── HUONG_DAN_PHAN_CONG.md      # Hướng dẫn chi tiết & Troubleshooting Phân công GV
├── TESTING_DOCUMENTATION.md    # Danh sách Test Cases & Tiêu chuẩn Kiểm thử
├── VI_TRI_KIEM_THU.md          # Chi tiết các kịch bản test chức năng
└── README.md                   # File hướng dẫn tổng quan dự án
```

---

## 🗄 MÔ HÌNH DỮ LIỆU (DATABASE SCHEMA)

Các bảng chính trong CSDL PostgreSQL (`productsdb`):
- **`BangCap`**: Mã bằng cấp (`DEG_GS`, `DEG_TS`...), tên bằng cấp, tên viết tắt.
- **`ChucVu`**: Mã chức vụ (`POS_HT`, `POS_TK`...), tên chức vụ, tên viết tắt.
- **`GiangVien`**: Mã GV, họ tên, ngày sinh (`SinhNhat`), email (`Mail`), sđt, giới tính, bằng cấp ID.
- **`Khoa`**: Mã khoa, tên khoa, tên viết tắt, vị trí, mô tả.
- **`Khoa_GiangVien`**: Bảng trung gian gán Giảng viên thuộc Khoa và Chức vụ.
- **`HocKi`**: Tên học kỳ, thời gian bắt đầu, thời gian kết thúc.
- **`HocPhan`**: Mã học phần, tên học phần, số tín chỉ, số tiết, hệ số học phần, khoa ID.
- **`LopHocPhan`**: Mã lớp, tên lớp, học kỳ ID, học phần ID, giảng viên ID (nullable), sĩ số sinh viên (`SoLuongSinhVien`).
- **`HeSoLop`**: Số sinh viên tối thiểu (`SoHocSinhToiThieu`), hệ số quy đổi, năm học.
- **`HeSoBangCap`**: Hệ số quy đổi thù lao theo bằng cấp và năm áp dụng (`Nam`).
- **`DinhMucTien`**: Định mức tiền thù lao trên một tiết dạy chuẩn (`SoTien`), ngày cập nhật, lý do.

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY

### 1. Yêu cầu Tiền đề (Prerequisites)
- **.NET SDK:** 9.0 trở lên.
- **Node.js:** Node v18.x hoặc v20.x trở lên (kèm `npm`).
- **PostgreSQL:** Đã khởi chạy dịch vụ PostgreSQL server ở `localhost:5432` với database `productsdb`.

### 2. Cấu hình Cơ sở dữ liệu
1. Kiểm tra chuỗi kết nối trong [appsettings.json](file:///k:/TestProject/server/appsettings.json):
   ```json
   "ConnectionStrings": {
     "DefaultConnection": "Host=localhost;Port=5432;Database=productsdb;Username=postgres;Password=admin"
   }
   ```
2. Tạo bảng bằng script SQL [create_tables.sql](file:///k:/TestProject/server/create_tables.sql) hoặc EF Core Migration.

### 3. Khởi chạy Backend API
Mở Terminal 1:
```bash
cd server
dotnet restore
dotnet run
```
Backend API khởi chạy tại: `http://localhost:5249` (Swagger UI: `http://localhost:5249/swagger`).

### 4. Khởi chạy Frontend Application
Mở Terminal 2:
```bash
cd client
npm install
npm run dev
```
Ứng dụng Web sẽ khả dụng tại: `http://localhost:5173`.

### 5. Nạp dữ liệu mẫu DuongUniversity (Optional)
Nếu muốn tái khởi tạo lại dữ liệu mẫu 435 lớp học phần với Lionel Messi, Ronaldo, Neymar Jr...:
```bash
# Gọi API Seed bằng Curl hoặc PowerShell
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:5249/Test/seed-rich-data'"
```

---

## 🧪 KIỂM THỬ TỰ ĐỘNG (AUTOMATED TESTING)

### 1. Chạy UI Tests (Selenium WebDriver)
```bash
cd tests/UITests
dotnet test
```

### 2. Chạy API Tests
```bash
cd tests/APITests
dotnet test
```

---

## 📄 TÀI LIỆU LIÊN QUAN

- 📖 [HUONG_DAN_PHAN_CONG.md](file:///k:/TestProject/HUONG_DAN_PHAN_CONG.md): Hướng dẫn thao tác & debug tính năng phân công giảng viên.
- 📖 [TESTING_DOCUMENTATION.md](file:///k:/TestProject/TESTING_DOCUMENTATION.md): Tài liệu đặc tả yêu cầu kiểm thử & danh sách Test Cases.
- 📖 [VI_TRI_KIEM_THU.md](file:///k:/TestProject/VI_TRI_KIEM_THU.md): Tổng hợp kết quả và vị trí các kịch bản kiểm thử.

---

*Hệ thống được phát triển với tiêu chuẩn mã nguồn sạch, kiến trúc mô-đun hóa dễ mở rộng và bảo trì.*

