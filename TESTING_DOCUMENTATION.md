# Tài Liệu Kiểm Thử Chức Năng: Phân Công Giảng Viên

## 1. CHỨC NĂNG ĐƯỢC CHỌN
**Tên chức năng:** Phân công giảng viên cho lớp học phần  
**Module:** LopHocPhanPage - PhanCongGiangVienModal  
**Loại chức năng:** Feature quản lý tài nguyên giảng dạy

---

## 2. YÊU CẦU CHƯA RÕ RÀNG → YÊU CẦU KIỂM THỬ ĐƯỢC

### Yêu cầu ban đầu (Chưa rõ ràng):
❌ "Hệ thống cho phép gán giảng viên cho các lớp học phần"

### Yêu cầu kiểm thử được (Rõ ràng):

**Yêu cầu chức năng (Functional Requirements):**

| Mã | Mô Tả Yêu Cầu | Tiêu Chí Chấp Nhận |
|----|----------------|-------------------|
| FR1 | Người dùng có thể tìm kiếm giảng viên theo mã hoặc tên | Tìm kiếm phải trả về kết quả chính xác (không phân biệt chữ hoa/thường) |
| FR2 | Hệ thống chỉ hiển thị giảng viên cùng khoa | Danh sách giảng viên được lọc theo `khoaId` của người dùng |
| FR3 | Người dùng có thể xem chi tiết giảng viên được chọn | Hiển thị: Mã GV, Tên, Khoa, Email |
| FR4 | Hệ thống gán một giảng viên cho nhiều lớp cùng lúc | Tất cả các lớp được chọn đều được gán giảng viên thành công |
| FR5 | Sau khi gán thành công, dữ liệu được tải lại | Modal đóng và danh sách lớp cập nhật giảng viên |

**Yêu cầu phi chức năng (Non-Functional Requirements):**

| Mã | Mô Tả Yêu Cầu | Tiêu Chí Chấp Nhận |
|----|----------------|-------------------|
| NFR1 | Tốc độ tìm kiếm | Kết quả trả về trong vòng < 500ms |
| NFR2 | Xử lý nhiều lớp | Có thể gán cho tối thiểu 10 lớp cùng lúc |
| NFR3 | Hiển thị thông báo phản hồi | Hiển thị thông báo thành công với số lớp được gán |
| NFR4 | Xác nhận đầu vào | Hệ thống yêu cầu chọn giảng viên trước khi gán |

**Yêu cầu đặc biệt (Edge Cases):**

| Mã | Mô Tả Yêu Cầu | Tiêu Chí Chấp Nhận |
|----|----------------|-------------------|
| EC1 | Không có giảng viên nào được tìm thấy | Hiển thị danh sách trống, không có lỗi |
| EC2 | Người dùng không chọn giảng viên | Hệ thống hiển thị cảnh báo "Vui lòng chọn giảng viên!" |
| EC3 | Gán giảng viên khi có giảng viên cũ | Giảng viên mới thay thế giảng viên cũ |

---

## 3. BA TEST CASE

### Test Case 1: Gán giảng viên thành công cho một lớp

**ID:** TC_PHANCONG_001  
**Tiêu đề:** Gán một giảng viên cho một lớp học phần  
**Độ ưu tiên:** High  
**Loại:** Positive Test  

| Bước | Hành Động | Dữ Liệu Đầu Vào | Kết Quả Mong Đợi |
|-----|----------|-----------------|-----------------|
| 1 | Mở danh sách lớp học phần | Module LopHocPhanPage | Hiển thị bảng danh sách lớp |
| 2 | Chọn 1 lớp học phần | Chọn checkbox lớp "LHP001" | Lớp được highlight, xuất hiện nút "Phân công giảng viên" |
| 3 | Nhấn nút "Phân công giảng viên" | Click button | Modal "Phân công giảng viên" mở ra |
| 4 | Xem danh sách lớp được chọn | Danh sách lớp | Hiển thị: "LHP001", tên lớp, số SV |
| 5 | Tìm kiếm giảng viên | Nhập "GV001" vào ô tìm kiếm | Hiển thị danh sách giảng viên khớp với "GV001" |
| 6 | Chọn giảng viên | Click vào giảng viên "GV001 - Nguyễn Văn A" | Giảng viên được chọn, hiển thị chi tiết (Mã, Tên, Khoa, Email) |
| 7 | Nhấn nút "Xác nhận" | Click button Xác nhận | ✓ Thông báo success: "Đã phân công thành công 1 lớp cho Nguyễn Văn A!" |
| 8 | Kiểm tra dữ liệu | Query database | ✓ LopHocPhan.GiangVienId = GV001 |

**Điều kiện tiên quyết:**
- Có ít nhất 1 lớp học phần trong hệ thống
- Có ít nhất 1 giảng viên cùng khoa
- User đã đăng nhập

---

### Test Case 2: Gán giảng viên cho nhiều lớp cùng lúc

**ID:** TC_PHANCONG_002  
**Tiêu đề:** Gán một giảng viên cho 5 lớp học phần cùng lúc  
**Độ ưu tiên:** High  
**Loại:** Positive Test  

| Bước | Hành Động | Dữ Liệu Đầu Vào | Kết Quả Mong Đợi |
|-----|----------|-----------------|-----------------|
| 1 | Mở danh sách lớp học phần | Module LopHocPhanPage | Hiển thị bảng danh sách lớp |
| 2 | Chọn 5 lớp học phần | Chọn checkbox: LHP001, LHP002, LHP003, LHP004, LHP005 | 5 lớp được highlight |
| 3 | Nhấn nút "Phân công giảng viên" | Click button | Modal mở ra với danh sách 5 lớp |
| 4 | Tìm kiếm giảng viên | Nhập "Nguyễn Văn A" | Hiển thị kết quả: "GV001 - Nguyễn Văn A" |
| 5 | Chọn giảng viên | Click vào giảng viên | Hiển thị chi tiết GV được chọn |
| 6 | Nhấn nút "Xác nhận" | Click button | ✓ Thông báo: "Đã phân công thành công 5 lớp cho Nguyễn Văn A!" |
| 7 | Kiểm tra dữ liệu | Query database | ✓ Tất cả 5 lớp có GiangVienId = GV001 |
| 8 | Kiểm tra danh sách cập nhật | Xem lại danh sách lớp | ✓ Tất cả 5 lớp hiển thị "Nguyễn Văn A" |

**Điều kiện tiên quyết:**
- Có ít nhất 5 lớp học phần trong hệ thống
- Có ít nhất 1 giảng viên cùng khoa
- User đã đăng nhập

---

### Test Case 3: Không chọn giảng viên khi cố gắng gán

**ID:** TC_PHANCONG_003  
**Tiêu đề:** Xác thực hệ thống khi user nhấn "Xác nhận" mà chưa chọn giảng viên  
**Độ ưu tiên:** Medium  
**Loại:** Negative Test  

| Bước | Hành Động | Dữ Liệu Đầu Vào | Kết Quả Mong Đợi |
|-----|----------|-----------------|-----------------|
| 1 | Mở danh sách lớp học phần | Module LopHocPhanPage | Hiển thị bảng danh sách lớp |
| 2 | Chọn 1 lớp học phần | Chọn checkbox | Lớp được highlight |
| 3 | Nhấn nút "Phân công giảng viên" | Click button | Modal mở ra |
| 4 | Xem danh sách lớp được chọn | Danh sách lớp | Hiển thị chính xác |
| 5 | KHÔNG tìm kiếm/chọn giảng viên | Để trống ô tìm kiếm | Ô tìm kiếm trống |
| 6 | Nhấn nút "Xác nhận" | Click button | ✓ Hiển thị cảnh báo: "Vui lòng chọn giảng viên!" |
| 7 | Kiểm tra modal | Modal vẫn mở | ✓ Modal không đóng, user có thể chọn lại |
| 8 | Kiểm tra dữ liệu | Query database | ✓ Không có bản ghi nào được cập nhật |

**Điều kiện tiên quyết:**
- Có ít nhất 1 lớp học phần trong hệ thống
- User đã đăng nhập

---

## 4. USER STORY

**ID:** US_PHANCONG_001

**Tiêu đề:**  
Là một Quản lý Khoa, tôi muốn có thể gán giảng viên cho một hoặc nhiều lớp học phần cùng lúc, để quản lý tài nguyên giảng dạy một cách hiệu quả.

**Mô Tả (Description):**  
Hệ thống cần cung cấp một giao diện cho phép quản lý khoa chọn nhiều lớp học phần và gán một giảng viên duy nhất cho tất cả các lớp đó, thay vì phải gán từng lớp một lần.

**Tiêu Chí Chấp Nhận (Acceptance Criteria):**

1. **AC1:** GIVEN người dùng đã chọn ít nhất 1 lớp học phần  
   WHEN người dùng nhấn nút "Phân công giảng viên"  
   THEN modal mở ra hiển thị danh sách lớp được chọn

2. **AC2:** GIVEN modal "Phân công giảng viên" đang mở  
   WHEN người dùng nhập tên hoặc mã giảng viên vào ô tìm kiếm  
   THEN hệ thống hiển thị danh sách giảng viên cùng khoa khớp với từ khóa tìm kiếm (không phân biệt chữ hoa/thường)

3. **AC3:** GIVEN hệ thống hiển thị danh sách giảng viên  
   WHEN người dùng chọn một giảng viên  
   THEN hệ thống hiển thị chi tiết giảng viên (Mã, Tên, Khoa, Email) trong một card thông tin

4. **AC4:** GIVEN giảng viên đã được chọn  
   WHEN người dùng nhấn nút "Xác nhận"  
   THEN hệ thống gán giảng viên đó cho tất cả các lớp đã chọn

5. **AC5:** GIVEN quá trình gán giảng viên hoàn tất thành công  
   WHEN hệ thống xử lý xong  
   THEN hệ thống hiển thị thông báo success với nội dung "Đã phân công thành công [số lớp] lớp cho [tên giảng viên]!"

6. **AC6:** GIVEN người dùng cố gắng gán giảng viên mà chưa chọn giảng viên nào  
   WHEN người dùng nhấn nút "Xác nhận"  
   THEN hệ thống hiển thị cảnh báo "Vui lòng chọn giảng viên!" và không đóng modal

**Ước Lượng (Estimation):** 5 điểm (Medium)

**Prioritize (Ưu Tiên):** High - Feature quan trọng cho quản lý khoa

**Dependencies:** 
- Quản lý giảng viên (Giảng viên phải tồn tại)
- Quản lý lớp học phần (Lớp học phần phải tồn tại)

---

## 5. KỊCH BẢN BDD (Behavior Driven Development)

```gherkin
# language: vi
Tính năng: Phân công giảng viên cho lớp học phần
  Mô tả: Quản lý khoa có thể gán giảng viên cho một hoặc nhiều lớp học phần
  Để: Quản lý tài nguyên giảng dạy một cách hiệu quả

  Bối Cảnh:
    Cho trước người dùng là quản lý khoa Công Nghệ Thông Tin
    Và hệ thống có 3 lớp học phần đang chờ gán giảng viên
      | Mã Lớp  | Tên Lớp              | Số SV | Khoa |
      | LHP001  | Lập Trình C++ - A1   | 30    | CNTT |
      | LHP002  | Lập Trình C++ - A2   | 32    | CNTT |
      | LHP003  | Lập Trình C++ - B1   | 28    | CNTT |
    Và hệ thống có danh sách giảng viên trong khoa CNTT
      | Mã GV  | Tên           | Khoa | Email              |
      | GV001  | Nguyễn Văn A  | CNTT | a.nguyen@uni.edu   |
      | GV002  | Trần Thị B    | CNTT | b.tran@uni.edu     |

  # Kịch bản 1: Phân công thành công
  Kịch Bản: Phân công một giảng viên cho nhiều lớp học phần
    Cho trước tôi ở trang danh sách lớp học phần
    Khi tôi chọn 3 lớp học phần (LHP001, LHP002, LHP003)
    Và tôi nhấn nút "Phân công giảng viên"
    Thì modal "Phân công giảng viên" mở ra
    Và modal hiển thị 3 lớp được chọn:
      | LHP001 - Lập Trình C++ - A1 - 30 SV  |
      | LHP002 - Lập Trình C++ - A2 - 32 SV  |
      | LHP003 - Lập Trình C++ - B1 - 28 SV  |
    
    Khi tôi nhập "Nguyễn Văn A" vào ô tìm kiếm giảng viên
    Thì hệ thống hiển thị 1 kết quả: "GV001 - Nguyễn Văn A"
    
    Khi tôi chọn giảng viên "GV001 - Nguyễn Văn A"
    Thì card thông tin giảng viên hiển thị:
      | Mã GV: GV001                      |
      | Tên: Nguyễn Văn A                |
      | Khoa: Công Nghệ Thông Tin        |
      | Email: a.nguyen@uni.edu          |
    
    Khi tôi nhấn nút "Xác nhận"
    Thì hệ thống gán giảng viên cho 3 lớp
    Và thông báo success hiển thị: "Đã phân công thành công 3 lớp cho Nguyễn Văn A!"
    Và modal đóng lại
    Và danh sách lớp cập nhật với giảng viên mới

  # Kịch bản 2: Phân công thất bại - Chưa chọn giảng viên
  Kịch Bản: Cảnh báo khi cố gắng gán mà chưa chọn giảng viên
    Cho trước tôi ở trang danh sách lớp học phần
    Khi tôi chọn 2 lớp học phần (LHP001, LHP002)
    Và tôi nhấn nút "Phân công giảng viên"
    Thì modal mở ra
    
    Khi tôi KHÔNG chọn giảng viên nào
    Và tôi nhấn nút "Xác nhận"
    Thì thông báo cảnh báo hiển thị: "Vui lòng chọn giảng viên!"
    Và modal vẫn mở
    Và dữ liệu không được lưu

  # Kịch bản 3: Tìm kiếm giảng viên
  Kịch Bản: Tìm kiếm giảng viên theo mã hoặc tên (không phân biệt chữ hoa/thường)
    Cho trước tôi ở modal "Phân công giảng viên"
    
    # Tìm theo mã giảng viên
    Khi tôi nhập "gv001" (chữ thường) vào ô tìm kiếm
    Thì hệ thống trả về: "GV001 - Nguyễn Văn A"
    
    Khi tôi xóa nội dung và nhập "GV002"
    Thì hệ thống trả về: "GV002 - Trần Thị B"
    
    # Tìm theo tên giảng viên
    Khi tôi xóa nội dung và nhập "Trần Thị" vào ô tìm kiếm
    Thì hệ thống trả về: "GV002 - Trần Thị B"
    
    # Tìm kiếm không có kết quả
    Khi tôi nhập "Hoàng Văn C" (giảng viên không tồn tại)
    Thì danh sách kết quả trống
    Và không có lỗi

  # Kịch bản 4: Cập nhật giảng viên
  Kịch Bản: Thay thế giảng viên cũ bằng giảng viên mới
    Cho trước lớp LHP001 hiện tại đã có giảng viên GV001 - Nguyễn Văn A
    Và tôi ở trang danh sách lớp học phần
    
    Khi tôi chọn lớp LHP001
    Và tôi nhấn nút "Phân công giảng viên"
    Và tôi chọn giảng viên GV002 - Trần Thị B
    Và tôi nhấn nút "Xác nhận"
    
    Thì hệ thống gán GV002 thay thế GV001
    Và thông báo success hiển thị: "Đã phân công thành công 1 lớp cho Trần Thị B!"
    Và danh sách lớp hiển thị "Trần Thị B" cho lớp LHP001
```

---

## 6. TÓML ƯỡM

**Chức Năng:** Phân Công Giảng Viên  
**Mục Đích:** Quản lý tài nguyên giảng dạy hiệu quả  
**Phạm Vi Test:** Tất cả các flow từ chọn lớp đến gán giảng viên thành công  

**Tóm Tắt Test Cases:**
- TC1: Gán thành công 1 giảng viên cho 1 lớp ✓
- TC2: Gán thành công 1 giảng viên cho 5 lớp ✓
- TC3: Xác thực khi chưa chọn giảng viên ✓

**Tóm Tắt BDD Scenarios:**
- Phân công 3 lớp cho 1 giảng viên ✓
- Cảnh báo khi chưa chọn giảng viên ✓
- Tìm kiếm giảng viên theo mã/tên ✓
- Cập nhật giảng viên cũ ✓
