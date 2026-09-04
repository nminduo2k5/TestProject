# 📘 HUỚNG DẪN CÀI ĐẶT VÀ CHẠY LẠI (README_REPRODUCE.md)
**Bài Tập Lớn Môn An Toàn Phần Mềm (SoftSec Toolkit) - DuongUniversity Management System**

---

## 1. YÊU CẦU MÔI TRƯỜNG (ENVIRONMENT REQUIREMENTS)

- **Hệ điều hành:** Windows 10/11, Linux, hoặc macOS.
- **Trình biên dịch C:** `GCC` (khuyên dùng GCC 14+ hoặc MSYS2 UCRT64 trên Windows).
- **Ngôn ngữ Python:** Python 3.10+ (Đã thử nghiệm trên Python 3.13.5).
- **Thư viện Python bắt buộc:**
  ```bash
  pip install z3-solver
  ```

---

## 2. DẪN XUẤT CÁC FILE MÃ NGUỒN VÀ BÀI NỘP

Toàn bộ các file bài nộp nằm tại thư mục `btl_softsec/`:
1. `salary_calc.c`: Mã nguồn C phiên bản có 4 lỗi cố ý.
2. `salary_calc_fixed.c`: Mã nguồn C phiên bản đã khắc phục an toàn bộ nhớ và logic.
3. `kripke_bmc.py`: Kripke Structure 5 trạng thái + Thuật toán Bounded Model Checker (BMC) (Chương 1).
4. `pattern_scanner.py`: Bộ quét tĩnh mẫu hàm không an toàn `ch2_memsafe.pattern_scanner` (Chương 2).
5. `smt_verify.py`: Verification formal với Z3 SMT Solver kiểm chứng tràn số nguyên (Chương 3).
6. `fuzzer_blackbox.py`: Script Fuzzing Hộp đen (Black-box) ngẫu nhiên (Chương 4).
7. `fuzzer_whitebox.py`: Script Fuzzing Hộp trắng (White-box Z3-Guided) giải ràng buộc trực tiếp (Chương 4).
8. `BAO_CAO_BTL_SOFTSEC.md`: Báo cáo chi tiết theo cấu trúc chuẩn BTL.

---

## 3. HƯỚNG DẪN CHẠY TỪNG BƯỚC (STEP-BY-STEP EXECUTION)

### Bước 1: Biên dịch Mã nguồn C
Mở Terminal/PowerShell tại thư mục `btl_softsec/` và chạy lệnh:

**Biên dịch phiên bản có lỗi:**
```bash
gcc -Wall -o salary_calc.exe salary_calc.c
```

**Biên dịch phiên bản đã sửa lỗi:**
```bash
gcc -Wall -o salary_calc_fixed.exe salary_calc_fixed.c
```

---

### Bước 2: Kiểm chứng Mô hình hóa & BMC (Chương 1)
Chạy script mô hình hóa Kripke Structure 5 trạng thái và kiểm tra các thuộc tính LTL Safety bằng BMC với độ sâu $k=5$:
```bash
python kripke_bmc.py
```
* **Kết quả kỳ vọng:**
  - Mô hình lỗi (`BUGGY`): Báo `SAT` đối với thuộc tính Safety `G(calculated -> assigned)` và xuất vết phản ví dụ (`Counterexample Trace`).
  - Mô hình sửa lỗi (`FIXED`): Báo `UNSAT` trên toàn bộ $k=5$.

---

### Bước 3: Kiểm tra An toàn Bộ nhớ & ASan / Cppcheck (Chương 2)

**1. Quét tĩnh bằng pattern_scanner:**
```bash
python pattern_scanner.py salary_calc.c
```

**2. Quét tĩnh bằng Cppcheck:**
```bash
cppcheck --enable=all --std=c11 salary_calc.c
```

**3. Biên dịch và kích hoạt Crash thực tế bằng AddressSanitizer (ASan):**
```bash
# Biên dịch cờ -fsanitize=address,undefined
gcc -fsanitize=address,undefined -g -o salary_calc_asan salary_calc.c

# Kích hoạt lỗi Stack Buffer Overflow với tên dài 90 ký tự (> 80)
python3 -c "print('A'*90 + '\nCU_NHAN\n')" | ./salary_calc_asan
```
* **Kết quả kỳ vọng:** ASan lập tức chặn chương trình và xuất thông báo `==ERROR: AddressSanitizer: stack-buffer-overflow` chỉ rõ dòng 33 tại hàm `parse_lecturer`.

---

### Bước 4: Kiểm chứng Formal SMT với Z3 Solver (Chương 3)
Chạy script kiểm chứng tràn số nguyên 32-bit vs 64-bit dựa trên miền giá trị thực tế của DuongUniversity:
```bash
python smt_verify.py
```
* **Kết quả kỳ vọng:**
  - `Check 1A` (Tích lũy tổng số tiết trong kỳ): Trả về `SAT` (tràn 32-bit `int32` xảy ra) và in tham số counterexample.
  - `Check 1B` (Miền đơn lớp học phần): Trả về `UNSAT` (Tiền max 1 lớp = 700.000.000 VNĐ < `INT32_MAX`).
  - `Check 2` (Kiểu 64-bit `long long`): Trả về `UNSAT` (Chứng minh an toàn tuyệt đối).

---

### Bước 5: Kiểm thử Fuzzing Hộp đen & Hộp trắng (Chương 4)

**1. Chạy Black-box Fuzzing:**
```bash
python fuzzer_blackbox.py
```
* In số lần thử (500 runs), số lần crash (`ExitCode=3221225477` - Access Violation) và số lỗi logic bằng cấp.

**2. Chạy White-box Z3-Guided Fuzzing:**
```bash
python fuzzer_whitebox.py
```
* Tìm trực tiếp testcase gây crash trong **1-2 lần giải Z3** với thời gian **0.0237 giây (< 0.05s)**, nhanh hơn **~9,578 lần (gần 10.000 lần)** so với Black-box.

---

## 4. BẢNG ĐỐI CHIẾU KẾT QUẢ KỲ VỌNG

| Mô-đun | Script / Lệnh | Đầu ra kỳ vọng |
| :--- | :--- | :--- |
| **Chương 1** | `python kripke_bmc.py` | Counterexample Trace cho `BUGGY`, `UNSAT` cho `FIXED` |
| **Chương 2** | `python pattern_scanner.py` | 3 cảnh báo hàm `strcpy` và ép kiểu `(int)` |
| **Chương 2** | `cppcheck salary_calc.c` | Alert `bufferAccessOutOfBounds` tại `parse_lecturer` |
| **Chương 2** | `ASan execution` | `==ERROR: AddressSanitizer: stack-buffer-overflow` |
| **Chương 3** | `python smt_verify.py` | `SAT` đối với int32 accumulation, `UNSAT` đối với int64 |
| **Chương 4** | `python fuzzer_blackbox.py` | ~30% - 35% testcase gây crash ngẫu nhiên |
| **Chương 4** | `python fuzzer_whitebox.py` | 100% crash input được sinh chính xác trong < 0.05s |

---
*DuongUniversity SoftSec BTL reproduce guide completed.*
