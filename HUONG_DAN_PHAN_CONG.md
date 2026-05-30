# HƯỚNG DẪN SỬA LỖI PHÂN CÔNG GIẢNG VIÊN

## ✅ CÁC LỖI ĐÃ SỬA

### 1. **Lỗi filter giảng viên (PhanCongGiangVienModal.jsx)**
- ❌ Sai: `teacher.idKhoa` (field không tồn tại)
- ✅ Đúng: `teacher.khoaId`
- ❌ Sai: Tìm kiếm theo `teacher.id` (UUID)
- ✅ Đúng: Tìm kiếm theo `teacher.maGiangVien`

### 2. **Lỗi điều kiện disable button (FuntionBar.jsx)**
- ❌ Sai: `disabled={khoaId == 'all' || !selectedLopHocPhan?.length || filterLopHocPhan?.length}`
- ✅ Đúng: `disabled={khoaId == 'all' || !selectedLopHocPhan?.length}`

### 3. **Lỗi reset selection khi filter (FilterBar.jsx)**
- ❌ Sai: Mỗi lần thay đổi filter đều reset `selectedRows` về []
- ✅ Đúng: Bỏ các lệnh `{ type: 'updateSelectedRows', payload: [] }`

### 4. **Thiếu validation backend (LopHocPhanController.cs)**
- ✅ Thêm: Kiểm tra giảng viên có tồn tại trước khi phân công

## 🧪 CÁCH KIỂM TRA

### Bước 1: Khởi động lại ứng dụng
```bash
# Terminal 1 - Backend
cd server
dotnet run

# Terminal 2 - Frontend  
cd client
npm run dev
```

### Bước 2: Test phân công giảng viên

1. **Vào trang "Lớp học phần và phân công"**
   - Chọn tab thứ 2

2. **Chọn filter:**
   - Khoa: Chọn 1 khoa cụ thể (VD: "Công nghệ thông tin")
   - Năm học: Chọn năm hiện tại hoặc tương lai
   - Học kỳ: Chọn kỳ chưa bắt đầu
   - Trạng thái: Chọn "Chưa phân công"

3. **Chọn lớp:**
   - Tick chọn 1 hoặc nhiều lớp (checkbox phải enable)
   - Nút "Phân công giảng viên (n)" phải hiển thị số lớp đã chọn
   - Nút phải enable (không bị mờ)

4. **Phân công:**
   - Click nút "Phân công giảng viên"
   - Modal hiển thị danh sách lớp đã chọn
   - Nhập mã GV hoặc tên vào ô tìm kiếm
   - Chọn giảng viên từ dropdown
   - Thông tin giảng viên hiển thị đầy đủ
   - Click "Xác nhận phân công"
   - Thông báo thành công
   - Bảng tự động refresh

## ❓ TROUBLESHOOTING

### Vấn đề: Nút "Phân công giảng viên (0)" bị disable

**Nguyên nhân:**
1. Chưa chọn khoa cụ thể (đang ở "Tất cả khoa")
2. Chưa tick chọn lớp nào
3. Các lớp đã chọn đều đã có giảng viên
4. Học kỳ của lớp đã bắt đầu

**Giải pháp:**
- Chọn 1 khoa cụ thể (không phải "Tất cả khoa")
- Filter "Trạng thái" = "Chưa phân công"
- Chọn học kỳ chưa bắt đầu
- Tick chọn các lớp có checkbox enable

### Vấn đề: Không tìm thấy giảng viên

**Nguyên nhân:**
- Giảng viên không thuộc khoa đã chọn
- Dữ liệu giảng viên chưa load

**Giải pháp:**
- Kiểm tra giảng viên có thuộc khoa đã filter không
- Refresh trang và thử lại

### Vấn đề: Lỗi khi phân công

**Kiểm tra:**
1. Mở Developer Console (F12)
2. Xem tab Network khi click "Xác nhận"
3. Kiểm tra response từ API

**Lỗi thường gặp:**
- 404: Lớp hoặc giảng viên không tồn tại
- 500: Lỗi server (kiểm tra backend logs)

## 📊 ĐIỀU KIỆN CHECKBOX ENABLE

Checkbox chỉ enable khi:
```javascript
record.giangVienId == null  // Chưa có giảng viên
&& 
new Date(record.thoiGianBatDau) >= Date.now()  // Học kỳ chưa bắt đầu
```

## 🔍 DEBUG

Nếu vẫn không hoạt động, kiểm tra:

1. **Console logs:**
```javascript
// Trong PhanCongGiangVienModal.jsx
console.log('Khoa ID:', khoaId);
console.log('Giảng viên data:', giangVienData);
console.log('Selected lớp:', selectedLopHocPhan);
```

2. **Backend logs:**
```bash
# Xem logs khi gọi API
POST /LopHocPhan/phan-cong-giang-vien
```

3. **Database:**
```sql
-- Kiểm tra dữ liệu
SELECT * FROM "LopHocPhan" WHERE "GiangVienId" IS NULL;
SELECT * FROM "GiangVien";
```
