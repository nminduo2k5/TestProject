# HƯỚNG DẪN TESTING HỆ THỐNG QUẢN LÝ GIẢNG VIÊN

## 📋 TỔNG QUAN

Hệ thống có **2 loại test**:
1. **API Tests** - Kiểm thử backend (Node.js + K6)
2. **UI Tests** - Kiểm thử giao diện (C# + Selenium)

---

## 🔧 CHUẨN BỊ

### Yêu cầu hệ thống

```bash
# 1. Node.js (v16+) - cho API Tests
node --version

# 2. K6 - công cụ load testing
# Tải từ: https://k6.io/docs/getting-started/installation/

# 3. .NET SDK 9.0 - cho UI Tests
dotnet --version

# 4. Visual Studio hoặc Visual Studio Code
```

### Cài đặt K6 (Windows)

```bash
# Dùng Chocolatey
choco install k6

# Hoặc tải trực tiếp từ: https://github.com/grafana/k6/releases
```

---

## 🧪 API TESTS (K6 + Node.js)

### Cấu trúc thư mục

```
tests/APITests/
├── bangCapTest.js           # Test Bằng cấp
├── giaoVienTest.js          # Test Giảng viên
├── hocKiTest.js             # Test Học kỳ
├── hocPhanTest.js           # Test Học phần
├── khoaTest.js              # Test Khoa
├── lopHocPhanTest.js        # Test Lớp học phần
├── lopHocPhanThongKeTest.js # Test Thống kê lớp
├── thietLapDinhMucTest.js   # Test Định mức tiền
├── thietLapHeSoBCTest.js    # Test Hệ số bằng cấp
├── thietLapHeSoLopTest.js   # Test Hệ số lớp
├── thongKeGVTest.js         # Test Thống kê GV
├── tinhTienDayTest.js       # Test Tính tiền dạy
└── checkIds.js              # Kiểm tra IDs
```

### Cách chạy API Tests

#### 1. Chạy test đơn lẻ

```bash
cd tests/APITests

# Test Bằng cấp
k6 run bangCapTest.js

# Test Giảng viên
k6 run giaoVienTest.js

# Test Học kỳ
k6 run hocKiTest.js
```

#### 2. Chạy tất cả tests

```bash
cd tests/APITests

# Chạy lần lượt
k6 run bangCapTest.js && k6 run giaoVienTest.js && k6 run hocKiTest.js

# Hoặc tạo script batch (Windows)
# Tạo file run_all_tests.bat
@echo off
k6 run bangCapTest.js
k6 run giaoVienTest.js
k6 run hocKiTest.js
k6 run hocPhanTest.js
k6 run khoaTest.js
k6 run lopHocPhanTest.js
k6 run lopHocPhanThongKeTest.js
k6 run thietLapDinhMucTest.js
k6 run thietLapHeSoBCTest.js
k6 run thietLapHeSoLopTest.js
k6 run thongKeGVTest.js
k6 run tinhTienDayTest.js
```

#### 3. Chạy với tùy chọn nâng cao

```bash
# Chạy với 100 users trong 60 giây
k6 run --vus 100 --duration 60s bangCapTest.js

# Chạy và xuất báo cáo JSON
k6 run --out json=results.json bangCapTest.js

# Chạy với tag
k6 run --tags "smoke" bangCapTest.js
```

### Cấu trúc file test K6

```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';

// Cấu hình test
export let options = {
  vus: 50,              // 50 users đồng thời
  duration: '25s',      // Chạy 25 giây
  thresholds: {
    http_req_duration: ['p(95)<1000'],  // 95% request < 1s
    http_req_failed: ['rate<0.01'],     // < 1% lỗi
  },
};

export default function () {
  // 1. GET - Lấy dữ liệu
  const getRes = http.get('http://localhost:5249/BangCap');
  check(getRes, {
    'Status 200': (r) => r.status === 200,
    'Có dữ liệu': (r) => r.body.length > 0,
  });

  // 2. POST - Tạo dữ liệu
  const payload = JSON.stringify({
    tenBangCap: `Bằng cấp ${Date.now()}`,
    tenVietTat: 'BC'
  });
  const postRes = http.post('http://localhost:5249/BangCap', payload, {
    headers: { 'Content-Type': 'application/json' }
  });
  check(postRes, {
    'POST Status 201': (r) => r.status === 201,
  });

  sleep(1); // Nghỉ 1 giây
}
```

### Ý nghĩa các chỉ số

| Chỉ số | Ý nghĩa |
|--------|---------|
| `vus` | Virtual Users - số lượng người dùng ảo |
| `duration` | Thời gian chạy test |
| `p(95)` | 95% request nhanh hơn giá trị này |
| `rate` | Tỷ lệ lỗi |
| `http_req_duration` | Thời gian response |

### Kết quả test

```
✓ GET /BangCap trả về 200
✓ POST /BangCap thành công
✓ PUT /BangCap cập nhật thành công
✓ DELETE /BangCap/:id thành công

checks.........................: 100% ✓ 200 ✗ 0
data_received..................: 45 kB
data_sent.......................: 12 kB
http_req_duration...............: avg=150ms p(95)=300ms p(99)=500ms
http_req_failed.................: 0.00%
http_reqs........................: 200
iteration_duration..............: avg=1.15s
iterations......................: 50
```

---

## 🎨 UI TESTS (Selenium + C#)

### Cấu trúc thư mục

```
tests/UITests/
├── Pages/
│   ├── BangCapPage.cs       # Page Object - Bằng cấp
│   └── KhoaPage.cs          # Page Object - Khoa
├── UC1_GVtest/
│   ├── BangCapUITests.cs    # Test cases - Bằng cấp
│   └── KhoaUITest.cs        # Test cases - Khoa
├── Drivers/
│   └── WebDriverFactory.cs  # Khởi tạo WebDriver
└── UITests.csproj
```

### Cách chạy UI Tests

#### 1. Mở project trong Visual Studio

```bash
cd tests
# Mở file Tests.sln
start Tests.sln
```

#### 2. Chạy test từ Visual Studio

- **Test Explorer**: View → Test Explorer (Ctrl + E, T)
- Click **"Run All Tests"** hoặc chọn test cụ thể

#### 3. Chạy từ command line

```bash
cd tests/UITests

# Chạy tất cả tests
dotnet test

# Chạy test cụ thể
dotnet test --filter "BangCapUITests"

# Chạy với verbose output
dotnet test --verbosity detailed

# Chạy và xuất báo cáo
dotnet test --logger "trx;LogFileName=TestResults.trx"
```

### Cấu trúc test UI

```csharp
using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Edge;
using UITests.Pages;

namespace UITests.Tests
{
  public class BangCapUITests
  {
    private IWebDriver? _driver;
    private BangCapPage? _page;

    [SetUp]  // Chạy trước mỗi test
    public void Setup()
    {
      var options = new EdgeOptions();
      _driver = new EdgeDriver(options);
      _driver.Navigate().GoToUrl("http://localhost:5173/bang-cap");
      _page = new BangCapPage(_driver);
    }

    [Test]  // Test case
    public void Test_Add_New_BangCap()
    {
      _page?.ClickAddButton();
      _page?.EnterBangCap("Bác sĩ", "BS");
      _page?.SubmitForm();
      
      Assert.That(_page?.IsMessageDisplayed("Thêm bằng cấp thành công!"), Is.True);
    }

    [TearDown]  // Chạy sau mỗi test
    public void TearDown()
    {
      _driver?.Quit();
    }
  }
}
```

### Page Object Pattern

```csharp
using OpenQA.Selenium;

namespace UITests.Pages
{
  public class BangCapPage
  {
    private IWebDriver _driver;

    // Locators
    private By _addButton = By.XPath("//button[contains(text(), 'Thêm')]");
    private By _nameInput = By.Id("tenBangCap");
    private By _submitButton = By.XPath("//button[contains(text(), 'Xác nhận')]");

    public BangCapPage(IWebDriver driver)
    {
      _driver = driver;
    }

    // Actions
    public void ClickAddButton()
    {
      _driver.FindElement(_addButton).Click();
    }

    public void EnterBangCap(string name, string abbrev)
    {
      _driver.FindElement(_nameInput).SendKeys(name);
      _driver.FindElement(By.Id("tenVietTat")).SendKeys(abbrev);
    }

    public void SubmitForm()
    {
      _driver.FindElement(_submitButton).Click();
    }

    public bool IsMessageDisplayed(string message)
    {
      try
      {
        var element = _driver.FindElement(By.XPath($"//*[contains(text(), '{message}')]"));
        return element.Displayed;
      }
      catch
      {
        return false;
      }
    }
  }
}
```

### Các loại test UI

| Loại | Mục đích | Ví dụ |
|------|---------|-------|
| **Smoke Test** | Kiểm tra chức năng cơ bản | Thêm, sửa, xóa |
| **Functional Test** | Kiểm tra chi tiết chức năng | Validation, error handling |
| **Regression Test** | Kiểm tra lỗi cũ không tái diễn | Sau khi fix bug |
| **Integration Test** | Kiểm tra tương tác giữa modules | Form → API → Database |

---

## 📊 CHẠY TEST TOÀN BỘ

### Quy trình testing hoàn chỉnh

```bash
# 1. Khởi động backend
cd server
dotnet run

# 2. Khởi động frontend (terminal mới)
cd client
npm run dev

# 3. Chạy API Tests (terminal mới)
cd tests/APITests
k6 run bangCapTest.js
k6 run giaoVienTest.js
k6 run hocKiTest.js
# ... chạy tất cả tests

# 4. Chạy UI Tests (terminal mới)
cd tests/UITests
dotnet test
```

### Tạo script tự động (Windows)

**File: run_all_tests.bat**

```batch
@echo off
echo ===== STARTING BACKEND =====
start cmd /k "cd server && dotnet run"

echo ===== STARTING FRONTEND =====
start cmd /k "cd client && npm run dev"

timeout /t 5

echo ===== RUNNING API TESTS =====
cd tests/APITests
k6 run bangCapTest.js
k6 run giaoVienTest.js
k6 run hocKiTest.js

echo ===== RUNNING UI TESTS =====
cd ../UITests
dotnet test

echo ===== ALL TESTS COMPLETED =====
pause
```

---

## 🐛 TROUBLESHOOTING

### API Tests

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|----------|
| `Connection refused` | Backend không chạy | Khởi động backend: `dotnet run` |
| `404 Not Found` | URL sai | Kiểm tra BASE_URL trong test |
| `Timeout` | Request quá lâu | Tăng timeout hoặc kiểm tra server |
| `JSON parse error` | Response không phải JSON | Kiểm tra API response |

### UI Tests

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|----------|
| `Element not found` | Locator sai | Kiểm tra XPath/CSS selector |
| `Timeout` | Element không load | Tăng implicit wait |
| `Stale element` | Element bị refresh | Tìm lại element sau refresh |
| `Browser not found` | Driver không cài | Cài Edge/Chrome driver |

### Kiểm tra kết nối

```bash
# Kiểm tra backend
curl http://localhost:5249/Test

# Kiểm tra frontend
curl http://localhost:5173

# Kiểm tra database
psql -U postgres -d productsdb -c "SELECT COUNT(*) FROM \"BangCap\";"
```

---

## 📈 BEST PRACTICES

### API Testing

✅ **Nên làm:**
- Test cả happy path và error cases
- Kiểm tra status code, headers, body
- Sử dụng data ngẫu nhiên để tránh conflict
- Cleanup dữ liệu sau test

❌ **Không nên làm:**
- Hardcode dữ liệu
- Phụ thuộc vào thứ tự test
- Bỏ qua error handling
- Test quá lâu (> 30s)

### UI Testing

✅ **Nên làm:**
- Sử dụng Page Object Pattern
- Chờ element load trước khi interact
- Kiểm tra message/notification
- Cleanup browser sau test

❌ **Không nên làm:**
- Hardcode locators
- Chạy test quá nhanh
- Bỏ qua implicit wait
- Test quá nhiều trong 1 test case

---

## 📝 VIẾT TEST MỚI

### Template API Test

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '10s',
};

const BASE_URL = 'http://localhost:5249/YourEndpoint';

export default function () {
  // Test GET
  const getRes = http.get(BASE_URL);
  check(getRes, {
    'GET returns 200': (r) => r.status === 200,
  });

  // Test POST
  const payload = JSON.stringify({
    field1: 'value1',
    field2: 'value2',
  });
  const postRes = http.post(BASE_URL, payload, {
    headers: { 'Content-Type': 'application/json' }
  });
  check(postRes, {
    'POST returns 201': (r) => r.status === 201,
  });

  sleep(1);
}
```

### Template UI Test

```csharp
[Test]
public void Test_New_Feature()
{
  // Arrange
  _page?.ClickButton("Thêm");
  
  // Act
  _page?.EnterData("value1", "value2");
  _page?.SubmitForm();
  
  // Assert
  Assert.That(_page?.IsMessageDisplayed("Thành công!"), Is.True);
}
```

---

## 🎯 KIỂM DANH SÁCH TEST

### API Tests
- [ ] bangCapTest.js
- [ ] giaoVienTest.js
- [ ] hocKiTest.js
- [ ] hocPhanTest.js
- [ ] khoaTest.js
- [ ] lopHocPhanTest.js
- [ ] lopHocPhanThongKeTest.js
- [ ] thietLapDinhMucTest.js
- [ ] thietLapHeSoBCTest.js
- [ ] thietLapHeSoLopTest.js
- [ ] thongKeGVTest.js
- [ ] tinhTienDayTest.js

### UI Tests
- [ ] BangCapUITests
- [ ] KhoaUITest

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra logs: `dotnet run` hoặc `npm run dev`
2. Kiểm tra database: `psql -U postgres -d productsdb`
3. Kiểm tra network: `curl http://localhost:5249/Test`
4. Xem file test để hiểu logic
