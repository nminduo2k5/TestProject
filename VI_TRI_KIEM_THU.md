# BẢN ĐỒ VÀ HƯỚNG DẪN CHẠY CÁC PHƯƠNG PHÁP KIỂM THỬ TRONG HỆ THỐNG

Tài liệu này cung cấp sơ đồ phân bổ chi tiết và hướng dẫn các bước thực tế để chạy 4 loại kiểm thử trong dự án **Quản lý Giảng viên & Lớp học phần**:
1. **Kiểm thử Hộp trắng (White-box Testing)**
2. **Kiểm thử Hộp đen (Black-box Testing)**
3. **Kiểm thử Tự động (Automated Testing)**
4. **Kiểm thử Nâng cao (Advanced Testing)**

---

## 🛠️ YÊU CẦU CHUẨN BỊ MÔI TRƯỜNG

Trước khi tiến hành chạy bất kỳ kiểm thử nào, hãy đảm bảo máy tính của bạn đã được cài đặt các công cụ sau:
1. **.NET SDK 9.0**: Dùng để chạy Backend và các dự án Test C# (`dotnet --version`).
2. **Node.js (v16+)**: Dùng cho Client và các scripts bổ trợ (`node --version`).
3. **K6 (Grafana)**: Công cụ chạy kiểm thử tải API (`k6 --version`).
   - Cài đặt trên Windows (sử dụng PowerShell):
     - Qua Chocolatey: `choco install k6`
     - Hoặc tải trực tiếp bản ZIP/MSI tại [K6 Releases](https://github.com/grafana/k6/releases).
4. **Microsoft Edge Browser & EdgeDriver**: Dùng cho UI testing với Selenium (mặc định EdgeDriver được quản lý tự động bởi Selenium hoặc gói cài sẵn trong dự án).

---

## 1. ⬜ KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)

### 📌 Vị trí trong dự án:
- **Mã nguồn kiểm thử**: [Test1.cs](file:///k:/ProjectTest/tests/APITests/Test1.cs) trong dự án test C# `APITests`.
- **Cấu hình dự án test**: [APITests.csproj](file:///k:/ProjectTest/tests/APITests/APITests.csproj).

### 🔍 Đặc điểm & Logic kiểm thử:
- **Bản chất**: Kiểm thử hộp trắng ở đây là **Unit Test (Kiểm thử đơn vị)** ở phía Backend. Nó kiểm tra trực tiếp cấu trúc mã nguồn và logic rẽ nhánh của controller [BangCapController.cs](file:///k:/ProjectTest/server/Controllers/BangCapController.cs) mà không cần chạy server thật hoặc kết nối Database thật.
- **Giải pháp giả lập**: Sử dụng **Entity Framework Core InMemory Database** để giả lập dữ liệu tạm thời trong RAM.
- **Các kịch bản bao phủ (Bao phủ nhánh logic rẽ nhánh - Branch Coverage):**
  - Trả về danh sách được sắp xếp độ dài mã bằng cấp (`Get_ReturnsAllBangCapOrderedCorrectly`).
  - Thêm mới thành công và tự động tạo mã tăng dần (`Create_ValidBangCap_ReturnsCreatedAtAction`).
  - Ràng buộc nhập thiếu thông tin, trống trường bắt buộc (`Create_MissingFields_ReturnsBadRequest`).
  - Trùng tên bằng cấp (`Create_DuplicateTenBangCap_ReturnsBadRequest`).
  - Trùng tên viết tắt (`Create_DuplicateTenVietTat_ReturnsBadRequest`).
  - Tên viết tắt vượt quá 10 ký tự (`Create_TenVietTatTooLong_ReturnsBadRequest`).

### 🚀 Cách chạy chi tiết:
Không cần khởi động Server/Client vì test chạy độc lập hoàn toàn trong memory.
1. Mở Terminal và di chuyển vào thư mục dự án test:
   ```powershell
   cd k:\ProjectTest\tests\APITests
   ```
2. Chạy lệnh thực thi các bài test C#:
   ```powershell
   dotnet test --filter "Test1"
   ```
   Hoặc chạy toàn bộ test trong thư mục này:
   ```powershell
   dotnet test
   ```

---

## 2. ⬛ KIỂM THỬ HỘP ĐEN (BLACK-BOX TESTING)

Kiểm thử hộp đen tập trung vào đầu vào, đầu ra, các chức năng nghiệp vụ và giao diện người dùng mà không cần biết chi tiết logic bên trong mã nguồn được viết như thế nào. Dự án hỗ trợ 2 hình thức kiểm thử hộp đen tự động:

### 2.1. Kiểm thử hộp đen API (Sử dụng K6)
- **Vị trí file test**: Các file kịch bản JS trong thư mục [tests/APITests/](file:///k:/ProjectTest/tests/APITests):
  - [bangCapTest.js](file:///k:/ProjectTest/tests/APITests/bangCapTest.js): Kiểm thử đầy đủ luồng CRUD Bằng cấp (GET -> POST -> PUT -> DELETE) qua HTTP Request.
  - [giaoVienTest.js](file:///k:/ProjectTest/tests/APITests/giaoVienTest.js): Kiểm thử API Giảng viên.
  - [khoaTest.js](file:///k:/ProjectTest/tests/APITests/khoaTest.js): Kiểm thử API Khoa.
  - [lopHocPhanTest.js](file:///k:/ProjectTest/tests/APITests/lopHocPhanTest.js): Kiểm thử API Lớp học phần.
  - ...và các API nghiệp vụ khác.

- **🚀 Cách chạy chi tiết**:
  1. **Khởi động Backend** (cần thiết vì K6 gọi API HTTP thật):
     ```powershell
     cd k:\ProjectTest\server
     dotnet run
     ```
     *(Backend sẽ khởi chạy tại cổng mặc định `http://localhost:5249`)*
  2. **Chạy K6 test** (Mở một Terminal mới):
     ```powershell
     cd k:\ProjectTest\tests\APITests
     k6 run bangCapTest.js
     ```

### 2.2. Kiểm thử hộp đen UI (Sử dụng Selenium WebDriver + NUnit)
- **Vị trí trong dự án**:
  - Thư mục kịch bản UI: [tests/UITests/UC1_GVtest/](file:///k:/ProjectTest/tests/UITests/UC1_GVtest/) chứa các kịch bản test như [BangCapUITests.cs](file:///k:/ProjectTest/tests/UITests/UC1_GVtest/BangCapUITests.cs) và [KhoaUITest.cs](file:///k:/ProjectTest/tests/UITests/UC1_GVtest/KhoaUITest.cs).
  - Thư mục định vị giao diện (Page Object Model): [tests/UITests/Pages/](file:///k:/ProjectTest/tests/UITests/Pages/) chứa [BangCapPage.cs](file:///k:/ProjectTest/tests/UITests/Pages/BangCapPage.cs) và [KhoaPage.cs](file:///k:/ProjectTest/tests/UITests/Pages/KhoaPage.cs).

- **🚀 Cách chạy chi tiết**:
  1. **Khởi động Backend & Frontend**:
     - **Backend (Terminal 1)**:
       ```powershell
       cd k:\ProjectTest\server
       dotnet run
       ```
     - **Frontend (Terminal 2)**:
       ```powershell
       cd k:\ProjectTest\client
       npm run dev
       ```
       *(Frontend chạy tại `http://localhost:5173`)*
  2. **Thực thi UI Test (Terminal 3)**:
     ```powershell
     cd k:\ProjectTest\tests\UITests
     dotnet test
     ```
     *(Hệ thống sẽ tự động mở trình duyệt Edge, giả lập click, nhập liệu, thực hiện thêm/sửa/xóa và tắt trình duyệt)*
     - Để chạy riêng một bộ test giao diện cụ thể (ví dụ Khoa):
       ```powershell
       dotnet test --filter "KhoaUITest"
       ```

---

## 3. 🤖 KIỂM THỬ TỰ ĐỘNG (AUTOMATED TESTING)

Toàn bộ các bài test hộp trắng, hộp đen API và hộp đen UI trong dự án đều được tự động hóa (Automated) để có thể chạy thông qua CI/CD hoặc các tệp lệnh kịch bản mà không cần con người thực hiện thao tác thủ công.

### 🚀 Cách chạy tự động hóa hàng loạt:

#### Cách 1: Chạy toàn bộ các bài test API K6 tự động
Chúng ta sử dụng tệp Batch có sẵn trong thư mục test API:
1. Đảm bảo server Backend đang chạy ở cổng `5249`.
2. Mở Terminal, di chuyển tới thư mục test API:
   ```powershell
   cd k:\ProjectTest\tests\APITests
   ```
3. Chạy file batch:
   ```powershell
   .\run_all_api_tests.bat
   ```
   *(Tệp này sẽ tự động thực thi tuần tự 12 kịch bản K6 và xuất kết quả ra màn hình)*

#### Cách 2: Tạo script tự động khởi chạy và test toàn bộ hệ thống
Để tối ưu hóa quy trình kiểm thử, bạn có thể tạo một file script `run_all_system_tests.bat` tại thư mục gốc của dự án (`k:\ProjectTest`) với nội dung sau:

```batch
@echo off
title He Thong Kiem Thu Tu Dong
echo ===========================================
echo 1. KHOI DONG BACKEND VA FRONTEND...
echo ===========================================
start cmd /k "cd server && dotnet run"
start cmd /k "cd client && npm run dev"

echo Cho 8 giay de server va client khoi dong hoan toan...
timeout /t 8

echo ===========================================
echo 2. CHAY KIEM THU HOP TRANG (UNIT TEST BACKEND)
echo ===========================================
cd tests\APITests
dotnet test --filter "Test1"
if %ERRORLEVEL% NEQ 0 (echo [LOI] Kiem thu hop trang that bai! && pause && exit)

echo ===========================================
echo 3. CHAY KIEM THU HOP DEN API (K6 PERFORMANCE)
echo ===========================================
call run_all_api_tests.bat

echo ===========================================
echo 4. CHAY KIEM THU HOP DEN UI (SELENIUM WEBDRIVER)
echo ===========================================
cd ..\UITests
dotnet test
if %ERRORLEVEL% NEQ 0 (echo [LOI] Kiem thu UI that bai! && pause && exit)

echo ===========================================
echo >>> TAT CA KIEM THU DA HOAN THANH VA THANH CONG <<<
echo ===========================================
pause
```

---

## 4. 📈 KIỂM THỬ NÂNG CAO (ADVANCED TESTING)

Kiểm thử nâng cao trong hệ thống bao gồm hai nội dung chính: **Kiểm thử hiệu năng/tải (Load/Performance Testing)** bằng K6 và áp dụng **mô hình thiết kế kiểm thử nâng cao (Page Object Model & Mocking)**.

### 4.1. Kiểm thử tải & hiệu năng (Load Testing với K6)
Thay vì chỉ kiểm tra tính đúng đắn của API, K6 giả lập hàng chục/hàng trăm người dùng ảo gửi yêu cầu đồng thời để đánh giá khả năng chịu tải và thời gian phản hồi của máy chủ dưới áp lực lớn.
- **Cấu hình nâng cao trong file test** (ví dụ [bangCapTest.js](file:///k:/ProjectTest/tests/APITests/bangCapTest.js)):
  - `vus: 50`: Giả lập 50 người dùng ảo truy cập đồng thời.
  - `duration: '25s'`: Duy trì việc gửi request liên tục trong 25 giây.
  - Ngưỡng đánh giá (Thresholds - nếu cấu hình): `http_req_duration: ['p(95)<1000']` (yêu cầu 95% số request phải hoàn thành dưới 1 giây) và `http_req_failed: ['rate<0.01']` (tỷ lệ lỗi nhỏ hơn 1%).

- **🚀 Các lệnh chạy nâng cao với K6**:
  - Chạy tăng cường với 100 người dùng trong 1 phút:
    ```powershell
    k6 run --vus 100 --duration 60s bangCapTest.js
    ```
  - Chạy và xuất báo cáo kết quả chi tiết định dạng JSON để phân tích:
    ```powershell
    k6 run --out json=results.json bangCapTest.js
    ```

### 4.2. Mô hình Page Object Model (POM) trong UI Test
- Dự án áp dụng mô hình POM giúp phân tách rõ rệt giữa:
  - **Kịch bản kiểm thử (Test logic)**: Chỉ chứa các bước kiểm thử và assert dữ liệu (ví dụ [BangCapUITests.cs](file:///k:/ProjectTest/tests/UITests/UC1_GVtest/BangCapUITests.cs)).
  - **Trang định vị (Page Objects)**: Định nghĩa các phần tử DOM (Xpath/ID) và các hành động tương tác với giao diện (ví dụ [BangCapPage.cs](file:///k:/ProjectTest/tests/UITests/Pages/BangCapPage.cs)).
- **Lợi ích**: Khi giao diện Client thay đổi (ví dụ đổi ID ô nhập, thay nút Xác nhận), lập trình viên chỉ cần cập nhật locator tại file Page Object mà không cần chỉnh sửa hàng chục kịch bản kiểm thử khác nhau.

### 4.3. Giả lập cơ sở dữ liệu (Database Isolation)
- Ở phần kiểm thử hộp trắng, việc sử dụng EF Core InMemory DB thay vì database PostgreSQL vật lý giúp loại bỏ rủi ro làm bẩn dữ liệu thật, tăng tốc độ chạy kiểm thử lên gấp nhiều lần và cho phép chạy song song nhiều tiến trình test cùng lúc mà không lo tranh chấp tài nguyên (race condition).

---

## 💡 TỔNG KẾT BẢNG LỆNH CHẠY NHANH

| Loại kiểm thử | Thư mục chạy | Lệnh thực thi | Yêu cầu dịch vụ kèm theo |
| :--- | :--- | :--- | :--- |
| **Hộp trắng (Unit Test)** | `tests/APITests` | `dotnet test --filter "Test1"` | Không cần dịch vụ nào |
| **Hộp đen API (K6)** | `tests/APITests` | `k6 run bangCapTest.js` | Backend đang chạy (`port 5249`) |
| **Hộp đen UI (Selenium)** | `tests/UITests` | `dotnet test` | Backend (`port 5249`) & Frontend (`port 5173`) |
| **Tự động hàng loạt (API)**| `tests/APITests` | `.\run_all_api_tests.bat` | Backend đang chạy (`port 5249`) |
| **Tải nâng cao (K6)** | `tests/APITests` | `k6 run --vus 100 --duration 60s bangCapTest.js` | Backend đang chạy (`port 5249`) |
