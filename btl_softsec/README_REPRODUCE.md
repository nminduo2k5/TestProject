# 📘 HUỚNG DẪN CÀI ĐẶT VÀ CHẠY LẠI (README_REPRODUCE.md)
**Bài Tập Lớn Môn An Toàn Phần Mềm (SoftSec Toolkit) - DuongUniversity Management System**

---

## 1. YÊU CẦU MÔI TRƯỜNG (ENVIRONMENT REQUIREMENTS)

- **Hệ điều hành:** Windows 10/11, Linux, hoặc macOS.
- **Trình biên dịch C:** `GCC` (khuyên dùng GCC 14+ hoặc MSYS2 UCRT64 trên Windows).
- **Ngôn ngữ Python:** Python 3.10+ (Đã thử nghiệm trên Python 3.13.5 trong Anaconda environment `messi`).
- **Thư viện Python bắt buộc:**
  ```bash
  pip install z3-solver
  ```

---

## 2. DẪN XUẤT CÁC FILE MÃ NGUỒN VÀ BÀI NỘP 3 MÔ-ĐUN E2E

Toàn bộ các file bài nộp nằm tại thư mục `btl_softsec/`:
1. `ch2_memsafe/giang_vien.c`, `lop_hoc_phan.c`, `tinh_tien_day.c`, `main.c`: Mã nguồn C E2E 3 mô-đun được phân tách mô-đun hóa, phiên bản có 5 lỗ hổng cố ý (CWE-120, CWE-416, CWE-476, CWE-190, CWE-1288).
2. `ch2_memsafe/main_fixed.c`: Driver phiên bản đã khắc phục an toàn bộ nhớ và logic 100% — dùng chung `giang_vien.c`, `lop_hoc_phan.c`, `tinh_tien_day.c` với bản VULN, chỉ gọi các hàm `*_SAFE` đã có sẵn trong 3 file module đó (tương tự cách `main.c` gọi các hàm `*_VULN`), tránh trùng lặp code giữa 2 phiên bản.
3. `ch1_models/kripke_bmc.py`: Kripke Structure 5 trạng thái E2E + Bounded Model Checker (BMC) kiểm chứng 4 thuộc tính LTL (P1-P4).
4. `ch2_memsafe/pattern_scanner.py`: Bộ quét tĩnh mẫu hàm không an toàn liên mô-đun `ch2_memsafe.pattern_scanner`.
5. `ch3_staticsat/smt_verify.py`: Verification formal với Z3 SMT Solver kiểm chứng các ràng buộc E2E 3 mô-đun và BMC LTL.
6. `ch4_dynafuzz/fuzzer_blackbox.py`: Script Fuzzing Hộp đen (Black-box) ngẫu nhiên liên mô-đun.
7. `ch4_dynafuzz/fuzzer_whitebox.py`: Script Fuzzing Hộp trắng (White-box Z3-Guided) giải ràng buộc 5 target E2E.
8. `BAO_CAO_BTL_SOFTSEC.md`: Báo cáo chi tiết theo cấu trúc chuẩn BTL Slide BTL_02.

---

## 3. HƯỚNG DẪN CHẠY NHANH TOÀN BỘ BÀI TẬP LỚN (ONE-CLICK / SINGLE COMMAND)

Để biên dịch tự động 4 Module C và kích hoạt toàn bộ Test Suite 4 Chương (Kripke BMC, Static Pattern Scanner, Formal SMT Z3 Solver, Black-box & White-box Fuzzing), chỉ cần mở Terminal tại thư mục `btl_softsec/` và gõ **1 câu lệnh duy nhất**:

```bash
python run_all.py
```

* **Cơ chế hoạt động tự động của `run_all.py`:**
  1. Tự động gọi `gcc` liên kết 4 file module C (`giang_vien.c`, `lop_hoc_phan.c`, `tinh_tien_day.c`, `main.c`) để tạo file thực thi `salary_calc.exe` và `salary_calc_fixed.exe`.
  2. Lần lượt chạy Chương 1 (`kripke_bmc.py`), Chương 2 (`pattern_scanner.py`), Chương 3 (`smt_verify.py`), Chương 4 (`fuzzer_blackbox.py` & `fuzzer_whitebox.py`).
  3. Tự động thu thập và xuất 100% kết quả log thực thi vào thư mục `btl_softsec/logs/`.

---

## 4. HƯỚNG DẪN CHẠY TỪNG BƯỚC (STEP-BY-STEP EXECUTION)

### Bước 1: Biên dịch Mã nguồn C E2E
Mở Terminal/PowerShell tại thư mục `btl_softsec/` và chạy lệnh:

**Biên dịch phiên bản có lỗi (VULN) từ 4 mô-đun:**
```bash
gcc -Wall -g -o ch2_memsafe/salary_calc.exe ch2_memsafe/giang_vien.c ch2_memsafe/lop_hoc_phan.c ch2_memsafe/tinh_tien_day.c ch2_memsafe/main.c
```

**Biên dịch phiên bản đã sửa lỗi (SAFE) — dùng chung 3 module với bản VULN, chỉ khác driver `main_fixed.c`:**
```bash
gcc -Wall -g -o ch2_memsafe/salary_calc_fixed.exe ch2_memsafe/giang_vien.c ch2_memsafe/lop_hoc_phan.c ch2_memsafe/tinh_tien_day.c ch2_memsafe/main_fixed.c
```

**Chạy thử nghiệm E2E Binaries trực tiếp:**
```bash
.\ch2_memsafe\salary_calc.exe e2e_uaf
.\ch2_memsafe\salary_calc_fixed.exe e2e_uaf
.\ch2_memsafe\salary_calc.exe e2e_null
.\ch2_memsafe\salary_calc_fixed.exe e2e_null
```

---

### Bước 2: Kiểm chứng Mô hình hóa Kripke & BMC (Chương 1)
Chạy script mô hình hóa Kripke Structure 5 trạng thái E2E và kiểm tra 4 thuộc tính LTL Safety/Liveness bằng BMC với độ sâu $k=5$:
```bash
python ch1_models/kripke_bmc.py
```
* **Tự động lưu log vào:** `logs/kripke_bmc.log`
* **Kết quả kỳ vọng:**
  - `Property 1` ($G(\text{calculated} \rightarrow \text{assigned})$): **SAT** cho `BUGGY` (Counterexample Trace found), **UNSAT** cho `FIXED`.
  - `Property 2` ($G(\text{exported} \rightarrow \text{calculated})$): **UNSAT** cho cả 2 bản.
  - `Property 3` ($G(\text{assigned} \rightarrow F \text{calculated})$): **SAT** cho cả 2 bản do rẽ nhánh gián đoạn lỗi $S_4$.
  - `Property 4` ($G(\text{error} \rightarrow \neg \text{exported})$): **UNSAT** cho cả 2 bản.

---

### Bước 3: Kiểm tra An toàn Bộ nhớ & Pattern Scanner (Chương 2)

**1. Quét tĩnh bằng pattern_scanner:**
```bash
python ch2_memsafe/pattern_scanner.py
```
* **Tự động lưu log vào:** `logs/pattern_scanner.log`

**2. Quét tĩnh bằng Cppcheck:**
```bash
cppcheck --enable=all --std=c11 ch2_memsafe/giang_vien.c ch2_memsafe/lop_hoc_phan.c ch2_memsafe/tinh_tien_day.c ch2_memsafe/main.c
```

---

### Bước 4: Kiểm chứng Formal SMT với Z3 Solver (Chương 3)
Chạy script kiểm chứng các ràng buộc E2E 3 mô-đun:
```bash
python ch3_staticsat/smt_verify.py
```
* **Tự động lưu log vào:** `logs/smt_verify.log`
* **Kết quả kỳ vọng:**
  - `Check 1` (Tích lũy tổng thù lao dạy nhiều lớp): Trả về `SAT` (tràn số 32-bit `int32` xảy ra) và in tham số counterexample.
  - `Check 2` (Kiểu 64-bit `long long`): Trả về `UNSAT` (Chứng minh an toàn tuyệt đối).
  - `Check 3` (Kiểm chứng BMC LTL): Nhất quán với kết quả Chương 1.

---

### Bước 5: Kiểm thử Fuzzing Hộp đen & Hộp trắng E2E (Chương 4)

**1. Chạy Black-box Fuzzing E2E:**
```bash
python ch4_dynafuzz/fuzzer_blackbox.py
```
* **Tự động lưu log vào:** `logs/fuzzer_blackbox.log`
* Số liệu đại diện tiêu chuẩn 200 runs: `salary_calc.exe` (71 crashes - 35.5%, 50.30s) vs `salary_calc_fixed.exe` (0 crashes - 0.0%, 2.93s).

**2. Chạy White-box Z3-Guided Fuzzing E2E:**
```bash
python ch4_dynafuzz/fuzzer_whitebox.py
```
* **Tự động lưu log vào:** `logs/fuzzer_whitebox.log`
* Phát hiện chính xác cả 5/5 target lỗ hổng E2E trong **5 lần giải Z3 Solver** với thời gian **0.0512 giây**, nhanh hơn **~982.4 lần** so với Fuzzing hộp đen ngẫu nhiên.

---

## 4. BẢNG ĐỐI CHIẾU KẾT QUẢ KỲ VỌNG E2E

| Mô-đun | Script / Lệnh | Đầu ra kỳ vọng chính thức |
| :--- | :--- | :--- |
| **Chương 1** | `python ch1_models/kripke_bmc.py` | P1 SAT cho `BUGGY`, UNSAT cho `FIXED`; P2 UNSAT; P3 SAT; P4 UNSAT |
| **Chương 2** | `python ch2_memsafe/pattern_scanner.py` | Cảnh báo `strcpy`, `dangling_free`, `unchecked_nested_deref`, `int_overflow_cast` |
| **Chương 3** | `python ch3_staticsat/smt_verify.py` | `SAT` đối với int32 multi-class, `UNSAT` đối với int64 & LTL Proof |
| **Chương 4** | `python ch4_dynafuzz/fuzzer_blackbox.py` | `salary_calc.exe`: 71 crashes (35.5%), 50.30s; `salary_calc_fixed.exe`: 0 crashes |
| **Chương 4** | `python ch4_dynafuzz/fuzzer_whitebox.py` | 5/5 target E2E được giải chính xác trong 0.0512s (~982.4x speedup) |

---
*DuongUniversity SoftSec BTL E2E reproduce guide completed.*
