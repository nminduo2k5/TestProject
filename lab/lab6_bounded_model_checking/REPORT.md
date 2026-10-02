# Báo cáo Lab 6 — Kiểm chứng Mô hình Giới hạn (Bounded Model Checking) & Mô hình Bộ nhớ

**Học phần:** CSE703093 — An toàn phần mềm — Phenikaa University
**Module:** Quản lý Lớp học phần — mảng `danhSachLop[MAX_LOP=10]` & xuất bảng kê thù lao theo trang (**DuongUniversity Management System**)

Module này dùng **đúng domain thực tế** của hệ thống DuongUniversity: phần tử mảng là `LopHocPhanEntry { id, maLop[MAX_MALOP=20], soTiet, heSoHocPhan, soLuongSinhVien }` (bản rút gọn của `LopHocPhan` trong `btl_softsec/ch2_memsafe/lop_hoc_phan.h`), hàm `tien_day_lop()` rút gọn từ `calculate_e2e_salary_SAFE()` với đúng ngưỡng quy mô 50 SV (CON-11) và `dinhMucTienChuan = 85000` — thay vì ví dụ "catalog sách" chung chung của đề gốc. Lỗ hổng được kiểm chứng là **CWE-125 Out-of-bounds Read** trên offset trang `base_index` do người dùng nhập — hậu quả nghiệp vụ: `soTiet` rác đi thẳng vào công thức tiền dạy.

Toàn bộ log trong báo cáo này là **log thật**, thu được bằng cách chạy `python/bmc_engine.py` (Anaconda Python 3.13.5 + z3 5.1.0) và biên dịch `c/lop_hoc_phan_access.c` với `-fsanitize=address` bằng **Clang 22.1.8 (MSYS2 `clang64`)**, chạy trực tiếp trên máy — không phải log dựng minh họa.

> **Ghi chú môi trường:** `python` mặc định trên PATH là MSYS2 Python 3.14 **không có z3**, GCC UCRT64 **không có libasan** (giống Lab 3). `Makefile`, `run_lab6.bat` và `tests/test_bmc.py` đã trỏ thẳng tới `C:\Users\HP\anaconda3\python.exe` và `C:\msys64\clang64\bin\clang.exe`, tự copy 2 DLL runtime ASan vào `c/`.

---

## 1. Bảng dự đoán tay (Bước 1) đối chiếu kết quả công cụ

### 1.1 Dự đoán trên giấy (trước khi chạy)

| ID | Vòng lặp / công thức chỉ số | Dự đoán tay | Lý do |
|---|---|:---:|---|
| BMC-01 | `for (i=0; i<10; i++) danhSachLop[i]` | SAFE | i chạy 0..9, đúng bằng kích thước mảng |
| BMC-02 | `for (i=0; i<=10; i++) danhSachLop[i]` | **UNSAFE** tại i=10 | `<=` thay vì `<` → lần lặp thứ 11 đọc phần tử thứ 11 của mảng 10 phần tử (CWE-193) |
| BMC-03 | `danhSachLop[base_index + i]`, i=0..4, `base_index ∈ [0,10)` không kiểm tra | **UNSAFE** | Chỉ cần `base_index ≥ 6` là `base_index + 4 ≥ 10`; dự đoán Z3 sẽ trả về một giá trị trong 6..9 |
| BMC-04 | như BMC-03 + tiền điều kiện `base_index ≤ 5` | SAFE | max index = 5 + 4 = 9 < 10 |
| BMC-05 | `danhSachLop[10 - i]`, i=0..4 | **UNSAFE** tại i=0 | 10 − 0 = 10 = kích thước mảng → ngoài biên ngay lần đầu |
| BMC-06 | `danhSachLop[10 - 1 - i]`, i=0..4 | SAFE | chỉ số 9,8,7,6,5 đều hợp lệ |

### 1.2 Kết quả công cụ (`python/bmc_engine.py`)

```text
[BMC-01-SAFE-FULL-SCAN] ...
  Ket qua BMC : SAFE  (ky vong: SAFE)  [OK]
  Giai thich  : Khong tim thay vi pham trong 10 buoc unwind dau tien (SAFE-UP-TO-BOUND, khong phai chung minh an toan vo han).

[BMC-02-UNSAFE-OFFBYONE] ...
  Ket qua BMC : UNSAFE  (ky vong: UNSAFE)  [OK]
  Giai thich  : Tai buoc unwind i=10, ton tai gia tri lam truy cap danhSachLop[index] voi index nam ngoai [0, 10).
  Nhan chung  : {'unwind_step_i': 10, 'index_accessed': 10}

[BMC-03-UNSAFE-SYMBOLIC-OFFSET] ...
  Ket qua BMC : UNSAFE  (ky vong: UNSAFE)  [OK]
  Giai thich  : Tai buoc unwind i=1, ton tai gia tri lam truy cap danhSachLop[index] voi index nam ngoai [0, 10).
  Nhan chung  : {'base_index': 9, 'unwind_step_i': 1, 'index_accessed': 10}

[BMC-04-SAFE-SYMBOLIC-OFFSET-BOUNDED] ...
  Ket qua BMC : SAFE  (ky vong: SAFE)  [OK]
  Giai thich  : Khong tim thay vi pham trong 5 buoc unwind dau tien (SAFE-UP-TO-BOUND, ...).

[BMC-05-UNSAFE-REVERSE-COUNTDOWN] ...
  Ket qua BMC : UNSAFE  (ky vong: UNSAFE)  [OK]
  Giai thich  : Tai buoc unwind i=0, ton tai gia tri lam truy cap danhSachLop[index] voi index nam ngoai [0, 10).
  Nhan chung  : {'unwind_step_i': 0, 'index_accessed': 10}

[BMC-06-SAFE-REVERSE-COUNTDOWN-FIXED] ...
  Ket qua BMC : SAFE  (ky vong: SAFE)  [OK]

Tong ket: 6/6 chuong trinh khop ky vong.
```

### 1.3 Đối chiếu

| ID | Dự đoán tay | BMC (Z3) | Khớp? | Ghi chú |
|---|:---:|:---:|:---:|---|
| BMC-01 | SAFE | SAFE | ✅ | |
| BMC-02 | UNSAFE @ i=10 | UNSAFE @ i=10 | ✅ | đúng bước vi phạm |
| BMC-03 | UNSAFE, base ∈ 6..9 | UNSAFE, **base_index = 9** @ i=1 | ✅ | Z3 không trả về giá trị "nhỏ nhất" (6) mà trả về **giá trị đầu tiên nó tìm thấy** ở bước unwind sớm nhất: tại i=0 không có vi phạm (base ≤ 9), tại i=1 cần base + 1 ≥ 10 ⇒ base = 9 là **nghiệm duy nhất** của bước i=1 — vì BMC duyệt i tăng dần và dừng ngay khi SAT. |
| BMC-04 | SAFE | SAFE | ✅ | |
| BMC-05 | UNSAFE @ i=0 | UNSAFE @ i=0 | ✅ | |
| BMC-06 | SAFE | SAFE | ✅ | |

**6/6 khớp.** Điểm học được từ BMC-03: nhân chứng của BMC gắn với **bước unwind sớm nhất** có vi phạm, không phải "đầu vào xấu nhỏ nhất" — muốn liệt kê mọi `base_index` gây lỗi phải lặp solver với ràng buộc loại trừ nghiệm cũ (`base_index != 9`, ...).

---

## 2. Thí nghiệm giới hạn nền tảng của BMC (Bước 4): giảm `unwind_bound`

Lệnh: `python/bmc_engine.py --bound-experiment` (giảm bound của BMC-01/BMC-02 xuống 5, kết quả lưu `dataset/bmc_bound_experiment.json`).

```text
=== THI NGHIEM GIOI HAN BMC: giam unwind_bound (Buoc 4) ===
[BMC-01-SAFE-FULL-SCAN] bound 10 -> 5: BMC bao SAFE (ky vong voi bound day du: SAFE)
[BMC-02-UNSAFE-OFFBYONE] bound 11 -> 5: BMC bao SAFE (ky vong voi bound day du: UNSAFE)   <-- FALSE NEGATIVE: loi off-by-one o buoc i=10 nam NGOAI 5 buoc da unwind
Ket luan: 'SAFE up to bound k' chi dam bao k buoc dau; vong lap that chay 11 buoc nen loi tai i=10 bi bo sot. Phai chon k >= so lan lap thuc te (hoac dung k-induction).
```

**Giải thích:**

1. **Cơ chế:** BMC chỉ sinh công thức cho các bước `i = 0..k-1`. Với k = 5, các khẳng định được kiểm tra là `0 ≤ 0 < 10`, …, `0 ≤ 4 < 10` — tất cả đều đúng ⇒ `Not(assertion)` UNSAT ở mọi bước ⇒ báo SAFE. Bước `i = 10` (nơi BMC-02 thực sự đọc `danhSachLop[10]`) **không bao giờ được mã hoá** nên solver không có cơ hội tìm ra.
2. **BMC-01 cũng báo SAFE với k = 5** — kết quả này *trùng* với sự thật nhưng **không phải vì BMC đã chứng minh** vòng lặp 10 bước an toàn; nó chỉ chứng minh 5 bước đầu an toàn. Nếu vòng lặp thật chạy đến 10 bước, kết luận "SAFE" với k = 5 là **không đủ cơ sở** — cùng một công cụ, cùng một thông điệp "SAFE", nhưng một trường hợp đúng (BMC-01) và một trường hợp sai (BMC-02): người dùng **không phân biệt được nếu chỉ nhìn output**.
3. **Hệ quả thực tiễn:** BMC là công cụ **tìm lỗi (bug finding)**, không phải **chứng minh vắng lỗi (proof of absence)**. "SAFE" phải luôn được đọc là "SAFE up to bound k". CBMC thực tế vì vậy có cờ `--unwinding-assertions`: nếu vòng lặp *có thể* chạy quá k bước, nó báo lỗi "unwinding assertion failed" thay vì im lặng — chính là cách phát hiện tình huống của BMC-02 ở trên. Hướng khắc phục khác là **k-induction** (chứng minh bước k ⇒ bước k+1) để suy ra an toàn không giới hạn.
4. **Chọn k như thế nào:** k phải ≥ số lần lặp lớn nhất có thể của vòng lặp thật (ở đây 11 cho `i <= 10`). Với vòng lặp phụ thuộc đầu vào (không biết cận trên) BMC không thể kết luận an toàn tuyệt đối — đây là giới hạn nền tảng, không phải lỗi cài đặt.

---

## 3. BMC-05 tự thêm (Bước 5): đếm ngược `danhSachLop[MAX_LOP - i]`

**Bối cảnh nghiệp vụ:** bảng kê muốn in **lớp mới nhất trước** (duyệt ngược từ cuối mảng). Lập trình viên viết `index = MAX_LOP - i` thay vì `MAX_LOP - 1 - i`.

**Dataset:** `BMC-05-UNSAFE-REVERSE-COUNTDOWN` (`index_formula = size_minus_i`, bound 5) và bản sửa `BMC-06-SAFE-REVERSE-COUNTDOWN-FIXED` (`size_minus_1_minus_i`). Động cơ BMC được mở rộng trường `index_formula` để hỗ trợ công thức chỉ số khác `base + i`.

**Kết quả BMC:** UNSAFE **ngay bước i = 0**, `index_accessed = 10` (xem log mục 1.2). Khác với BMC-02 (lỗi ở bước *cuối*), đây là lỗi ở bước *đầu* — nên **ngay cả bound rất nhỏ (k = 1) cũng bắt được**. Đây là ví dụ cho thấy "lỗi off-by-one" có hai dạng: vượt biên trên ở cuối vòng lặp (BMC-02) và vượt biên trên ở đầu vòng lặp đếm ngược (BMC-05); dạng thứ hai *dễ* cho BMC hơn vì xuất hiện ở bước unwind nông.

**Cài đặt C tương ứng** (`symbolic_reverse` / `symbolic_reverse_fixed` trong `c/lop_hoc_phan_access.c`) và log ASan thật:

```text
$ ./lop_hoc_phan_access.exe symbolic_reverse
=== symbolic_reverse (tuong ung BMC-05, tu them) ===
==18132==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x006fd20ffbc0 at pc 0x7ff6a1b2219a ...
READ of size 4 at 0x006fd20ffbc0 thread T0
    #0 0x7ff6a1b22199 in symbolic_reverse K:/TestProject/lab/lab6_bounded_model_checking/c/lop_hoc_phan_access.c:120:90
    #1 0x7ff6a1b21857 in main K:/TestProject/lab/lab6_bounded_model_checking/c/lop_hoc_phan_access.c:156:9
Address 0x006fd20ffbc0 is located in stack of thread T0 at offset 416 in frame
    #0 0x7ff6a1b2146f in main K:/TestProject/lab/lab6_bounded_model_checking/c/lop_hoc_phan_access.c:132
    [32, 392) 'danhSachLop' (line 136) <== Memory access at offset 416 overflows this variable
SUMMARY: AddressSanitizer: stack-buffer-overflow ... in symbolic_reverse
[exit code = 1]

$ ./lop_hoc_phan_access.exe symbolic_reverse_fixed
=== symbolic_reverse_fixed (tuong ung BMC-06, tu them) ===
  danhSachLop[9] CNTT2024_10  soTiet=57
  danhSachLop[8] CNTT2024_09  soTiet=54
  danhSachLop[7] CNTT2024_08  soTiet=51
  danhSachLop[6] CNTT2024_07  soTiet=48
  danhSachLop[5] CNTT2024_06  soTiet=45
[exit code = 0]
```

Chú ý dòng ASan `[32, 392) 'danhSachLop'` — mảng 10 phần tử × `sizeof(LopHocPhanEntry) = 36` byte = 360 byte nằm ở offset 32..392 của frame; truy cập tại offset **416 = 392 + 24** đúng bằng vị trí trường `soTiet` (offset 24 trong struct: `id` 4 + `maLop` 20) của "phần tử thứ 11" không tồn tại. Chương trình **không in được dòng nào** trước khi crash — khớp với BMC: vi phạm ở bước i = 0.

---

## 4. Đối chiếu tĩnh ↔ động và log `make test`

### 4.1 Nhân chứng BMC-03 (`base_index = 9`) làm chương trình C crash thật

```text
$ ./lop_hoc_phan_access.exe symbolic_unsafe 9
=== symbolic_unsafe base_index=9 (tuong ung BMC-03) ===
  danhSachLop[9] CNTT2024_10  soTiet=57  tien=8721000 VND          <-- buoc i=0: hop le (9 < 10)
==11680==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x0063438ff708 ...
READ of size 4 at 0x0063438ff708 thread T0
    #0 0x7ff6a1b22311 in tien_day_lop K:/.../c/lop_hoc_phan_access.c:59:30      <-- doc lhp->soLuongSinhVien
    #1 0x7ff6a1b21eaa in symbolic_unsafe K:/.../c/lop_hoc_phan_access.c:91:23
    #2 0x7ff6a1b217bf in main K:/.../c/lop_hoc_phan_access.c:150:9
    [32, 392) 'danhSachLop' (line 136) <== Memory access at offset 424 overflows this variable
SUMMARY: AddressSanitizer: stack-buffer-overflow ... in tien_day_lop
[exit code = 1]
```

Đúng như BMC dự đoán: bước **i = 0** in được 1 lớp hợp lệ, bước **i = 1** đọc `danhSachLop[10]` → crash. Điểm đáng chú ý về bảo mật: lệnh đọc đầu tiên vượt biên là `lhp->soLuongSinhVien` **bên trong hàm tính tiền** — nếu không có ASan, giá trị rác này sẽ quyết định hệ số quy mô (`> 50 ? 0.2 : 0.0`) và `soTiet` rác sẽ nhân thẳng vào thù lao: lỗi bộ nhớ biến thành **sai lệch tài chính thầm lặng**, không phải crash.

### 4.2 Bản sửa (tiền điều kiện) và các kịch bản sạch

```text
$ ./lop_hoc_phan_access.exe symbolic_safe 9
=== symbolic_safe base_index=9 (tuong ung BMC-04) ===
[TU CHOI] base_index=9 khong hop le (offset trang phai trong [0, 5])
[exit code = 0]

$ ./lop_hoc_phan_access.exe symbolic_safe 3
=== symbolic_safe base_index=3 (tuong ung BMC-04) ===
  danhSachLop[3] CNTT2024_04  soTiet=39  tien=5966999 VND
  danhSachLop[4] CNTT2024_05  soTiet=42  tien=6425999 VND
  danhSachLop[5] CNTT2024_06  soTiet=45  tien=6885000 VND
  danhSachLop[6] CNTT2024_07  soTiet=48  tien=7343999 VND
  danhSachLop[7] CNTT2024_08  soTiet=51  tien=7803000 VND
  TONG THU LAO TRANG: 34424997 VND
[exit code = 0]

$ ./lop_hoc_phan_access.exe safe_full_scan
=== safe_full_scan (tuong ung BMC-01) ===
  danhSachLop[0] CNTT2024_01  soTiet=30  tien=3825000 VND
  ... (10 dong) ...
  danhSachLop[9] CNTT2024_10  soTiet=57  tien=8721000 VND
  TONG THU LAO HOC KY: 64030496 VND
[exit code = 0]

$ ./lop_hoc_phan_access.exe offbyone
=== offbyone_scan (tuong ung BMC-02) ===
  danhSachLop[0] ... danhSachLop[9]  (10 dong hop le)
==4104==ERROR: AddressSanitizer: stack-buffer-overflow ...
    #1 0x7ff6a1b21d7a in offbyone_scan K:/.../c/lop_hoc_phan_access.c:79:23     <-- i == 10
    [32, 392) 'danhSachLop' (line 136) <== Memory access at offset 424 overflows this variable
[exit code = 1]
```

> **Quan sát phụ (không thuộc phạm vi BMC nhưng có thật):** `tien=5966999` thay vì 5 967 000 — do `heSoHocPhan` là `float` (1.0f) cộng với `0.2` rồi ép `(long long)` giống hệt `calculate_e2e_salary_SAFE()` thật; sai số 1 VND/lớp này là **hành vi của hệ thống gốc**, được giữ nguyên để log đối chiếu trung thực (liên quan CWE-681/682, có thể sửa bằng `llround()`).

### 4.3 Log `mingw32-make test` (7/7 PASS)

```text
C:/Users/HP/anaconda3/python.exe tests/test_bmc.py
[PASS] test_bmc_results_match_expectation
[PASS] test_bmc03_witness_matches_c_runtime_bug
[PASS] test_c_safe_full_scan_no_crash
[PASS] test_c_symbolic_safe_with_precondition_rejects_bad_input
[PASS] test_c_symbolic_safe_with_valid_input_runs_clean
[PASS] test_bmc05_reverse_witness_matches_c_runtime_bug
[PASS] test_bmc06_reverse_fixed_runs_clean

7/7 test da PASS
```

| Test | Đối chiếu gì |
|---|---|
| `test_bmc_results_match_expectation` | 6/6 chương trình khớp nhãn kỳ vọng |
| `test_bmc03_witness_matches_c_runtime_bug` | lấy `base_index` **từ kết quả Z3** (không hard-code) → chạy C → phải crash với `stack-buffer-overflow` |
| `test_c_safe_full_scan_no_crash` | BMC-01 SAFE ⇔ ASan sạch |
| `test_c_symbolic_safe_with_precondition_rejects_bad_input` | tiền điều kiện BMC-04 chặn đúng nhân chứng BMC-03 |
| `test_c_symbolic_safe_with_valid_input_runs_clean` | base=3 in đúng tới `danhSachLop[7]` |
| `test_bmc05_reverse_witness_matches_c_runtime_bug` | BMC-05: `violated_at_step == 0`, `index == 10`, C crash |
| `test_bmc06_reverse_fixed_runs_clean` | BMC-06 SAFE ⇔ in đúng 9..5, ASan sạch |

---

## 5. Kết luận

- Module dùng đúng domain thật (`danhSachLop[MAX_LOP]`, `LopHocPhanEntry`, `MAX_MALOP=20`, công thức tiền dạy CON-11, `dinhMucTienChuan=85000`) của DuongUniversity Management System; lỗ hổng kiểm chứng là CWE-125 trên offset trang người dùng nhập, với hậu quả nghiệp vụ là **sai thù lao thầm lặng**.
- Dự đoán tay 6/6 khớp Z3; nhân chứng `base_index = 9` của BMC-03 và `i = 0, index = 10` của BMC-05 **thực sự** làm chương trình C crash dưới ASan (trace có tên hàm và số dòng), tiền điều kiện của BMC-04 chặn đúng giá trị đó.
- Thí nghiệm giảm bound chứng minh **bằng log thật** rằng BMC-02 (lỗi có thật) bị báo SAFE với k = 5: "SAFE up to bound" ≠ an toàn tuyệt đối — BMC là công cụ tìm lỗi, không phải chứng minh vắng lỗi.
- `make test` → **7/7 PASS** thật (5 theo đề + 2 bổ sung).
