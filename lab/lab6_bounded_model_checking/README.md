# Lab 6 — Kiểm chứng Mô hình Giới hạn (Bounded Model Checking) & Mô hình Bộ nhớ

**Chủ đề xuyên suốt:** DuongUniversity Management System
**Module con:** Quản lý Lớp học phần — mảng `danhSachLop[MAX_LOP=10]` của một giảng viên trong 1 học kỳ và chức năng "xuất bảng kê thù lao theo trang" (tiếp nối Lab 3/4 — dùng đúng `MAX_MALOP=20`, các trường `soTiet`/`heSoHocPhan`/`soLuongSinhVien` và công thức tiền dạy của `btl_softsec/ch2_memsafe`, không phải ví dụ "catalog sách" chung chung của đề gốc)
**Ánh xạ đề cương:** Chương 3 — 3.5 Kiểm chứng mô hình phần mềm (BMC), 3.6 Mô hình bộ nhớ, 3.7 Sắp xếp mô hình bộ nhớ
**Báo cáo kết quả đầy đủ (log thật, không phải minh họa):** [`REPORT.md`](REPORT.md)

## 0. Yêu cầu môi trường (đọc trước khi chạy)

| Thành phần | Dùng để | Ghi chú trên máy này |
|---|---|---|
| **Python + `z3-solver`** | động cơ BMC (`python/bmc_engine.py`) | `python` mặc định trên PATH là MSYS2 Python 3.14 **không có z3** → `Makefile`/`run_lab6.bat` tự dùng `C:\Users\HP\anaconda3\python.exe` (Python 3.13.5, z3 5.1.0). Máy khác: `pip install z3-solver`. |
| **Clang MSYS2 `clang64`** | biên dịch C với `-fsanitize=address` | Giống Lab 3: GCC UCRT64 **không kèm libasan** trên Windows. Cài một lần: `pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld`. 2 DLL runtime (`libclang_rt.asan_dynamic-x86_64.dll`, `libc++.dll`) được copy tự động vào `c/`. |
| `mingw32-make` | (tuỳ chọn) chạy `Makefile` | hoặc chạy `run_lab6.bat` không cần make |

Để ASan in **tên hàm + số dòng** (thay vì chỉ địa chỉ) hãy thêm `C:\msys64\clang64\bin` (chứa `llvm-symbolizer.exe`) vào PATH khi chạy binary — log trong `REPORT.md` thu được theo cách này.

## 1. Mục tiêu học tập

- Hiểu nguyên lý **Bounded Model Checking**: mở cuộn (unwind) vòng lặp k bước, mã hóa mỗi bước thành công thức SMT, hỏi solver "tồn tại đầu vào nào vi phạm khẳng định an toàn không?".
- Phân biệt rõ **"SAFE up to bound k"** với **"an toàn tuyệt đối"** — chứng minh bằng thí nghiệm thật (`--bound-experiment`) rằng giảm bound làm BMC **bỏ sót** lỗi off-by-one có thật.
- Tự viết một động cơ BMC đơn giản bằng Z3 (không dùng CBMC) để hiểu cơ chế bên trong.
- Đối chiếu kết quả kiểm chứng tĩnh (BMC) với hành vi runtime thực tế (AddressSanitizer): **nhân chứng** `base_index=9` do Z3 tìm ra được đưa thẳng vào chương trình C và làm nó crash thật.
- Thiết kế **tiền điều kiện (precondition)** `base_index <= MAX_LOP - PAGE_SIZE` để sửa lỗi đọc ngoài biên (CWE-125).

## 2. Bối cảnh bài toán

Trong DuongUniversity, mỗi giảng viên phụ trách tối đa `MAX_LOP = 10` lớp học phần/học kỳ, lưu trong mảng `danhSachLop[MAX_LOP]` (phần tử `LopHocPhanEntry` — bản rút gọn của `LopHocPhan` trong `lop_hoc_phan.h`, bỏ `gv_ptr` vì vòng đời con trỏ đã là chủ đề Lab 3). Module 3 có chức năng **xuất bảng kê thù lao theo trang**: đọc `PAGE_SIZE = 5` lớp liên tiếp từ `base_index` (offset trang do người dùng nhập) và cộng dồn `tien_day_lop()` (rút gọn từ `calculate_e2e_salary_SAFE`, đúng ngưỡng quy mô 50 SV — CON-11 — và `dinhMucTienChuan = 85000`).

Nếu `base_index` không được kiểm tra, vòng lặp đọc `danhSachLop[index]` với `index >= 10` → **CWE-125 Out-of-bounds Read**: `soTiet` rác từ stack đi thẳng vào công thức tiền dạy (sai thù lao, lộ nội dung stack). `dataset/bmc_programs.json` mô tả 6 chương trình: duyệt đúng, off-by-one, offset không kiểm tra, bản sửa có tiền điều kiện, và 2 chương trình tự thêm (đếm ngược sai / đếm ngược đúng).

## 3. Các bước thực hành

### Bước 1 — Tự phân tích từng chương trình trên giấy
Dự đoán SAFE/UNSAFE cho 6 mục trước khi chạy công cụ — bảng dự đoán và đối chiếu ở `REPORT.md` mục 1.

### Bước 2 — Chạy động cơ BMC
```bash
C:\Users\HP\anaconda3\python.exe python/bmc_engine.py
```
Đọc kỹ phần "Nhân chứng" (witness): với BMC-03, Z3 tìm ra `base_index = 9` làm bước unwind `i = 1` đọc `danhSachLop[10]`.

### Bước 3 — Đối chiếu với runtime thực tế (C + ASan)
```bash
mingw32-make            # hoặc run_lab6.bat
./c/lop_hoc_phan_access.exe safe_full_scan
./c/lop_hoc_phan_access.exe offbyone
./c/lop_hoc_phan_access.exe symbolic_unsafe 9      # <-- dung dung nhan chung BMC-03
./c/lop_hoc_phan_access.exe symbolic_safe 9        # bi TU CHOI o tien dieu kien
./c/lop_hoc_phan_access.exe symbolic_safe 3
```
Giá trị `base_index=9` gây `stack-buffer-overflow` ở `symbolic_unsafe` **đúng là** nhân chứng BMC tìm ra ở Bước 2.

### Bước 4 — Thử nghiệm giới hạn của BMC (đã tự động hoá)
```bash
C:\Users\HP\anaconda3\python.exe python/bmc_engine.py --bound-experiment
```
Script giảm `unwind_bound` của BMC-01/BMC-02 xuống 5 (nhỏ hơn `array_size=10`) và chạy lại: BMC-02 (off-by-one **thật**) bị báo **SAFE** — một **false negative** đúng nghĩa. Giải thích chi tiết ở `REPORT.md` mục 2.

### Bước 5 — Mở rộng: thêm chương trình mới vào dataset
`BMC-05` mô tả in bảng kê theo thứ tự ngược `danhSachLop[MAX_LOP - i]` → vi phạm **ngay bước i = 0** (index = 10). `BMC-06` là bản sửa `MAX_LOP - 1 - i`. Cả hai có hàm C tương ứng (`symbolic_reverse`, `symbolic_reverse_fixed`) — xem `REPORT.md` mục 3.

### Bước 6 — Chạy bộ test tự động
```bash
mingw32-make test       # hoặc: C:\Users\HP\anaconda3\python.exe tests\test_bmc.py
```

## 4. Yêu cầu hoàn thiện (Deliverables)

1. ✅ Bảng dự đoán tay (Bước 1) đối chiếu kết quả công cụ — `REPORT.md` mục 1.
2. ✅ Giải thích thí nghiệm giới hạn BMC (giảm `unwind_bound`), kèm log thật — `REPORT.md` mục 2.
3. ✅ `BMC-05` tự thêm (đếm ngược) kèm giải thích, bản cài đặt C `symbolic_reverse()` và bản sửa `BMC-06` — `REPORT.md` mục 3.
4. ✅ Log `make test` toàn bộ PASS — `REPORT.md` mục 4.

## 5. Yêu cầu kết quả

- ✅ `tests/test_bmc.py` **7/7 PASS** (5 test theo đề + 2 test bổ sung cho BMC-05/06).
- ✅ Giá trị `base_index=9` trong nhân chứng BMC-03 **thực sự** làm chương trình C crash dưới ASan (`stack-buffer-overflow`, `READ of size 4` tại `tien_day_lop` dòng 59) — test `test_bmc03_witness_matches_c_runtime_bug` kiểm tra điều này tự động.

## 6. Sơ đồ luồng dữ liệu (Dataflow)

```
 dataset/bmc_programs.json (array_size=MAX_LOP, unwind_bound, symbolic_base, index_formula, ...)
            │
            ▼ (unwind vong lap, ma hoa SMT tung buoc: Not(0 <= index < 10) SAT?)
 python/bmc_engine.py  (Z3)  ──--bound-experiment──►  dataset/bmc_bound_experiment.json
            │
            ▼
 dataset/bmc_results.json  (SAFE / UNSAFE + nhan chung cu the: base_index=9, i=1, index=10)
            │
            ▼ (lay nhan chung lam tham so dong lenh that)
 c/lop_hoc_phan_access.c  --clang -fsanitize=address-->  ASan: stack-buffer-overflow tai danhSachLop[10]
            │
            ▼
 tests/test_bmc.py  (doi chieu ket qua tinh <-> dong, 7 test)
```

## 7. Tài liệu tham khảo
- Đề cương CSE703093 — An toàn phần mềm, Chương 3 (3.5, 3.6, 3.7).
- E. Clarke, D. Kroening, F. Lerda, *A Tool for Checking ANSI-C Programs* (nền tảng của CBMC), TACAS 2004.
- CWE-125 — Out-of-bounds Read; CWE-193 — Off-by-one Error.
- `btl_softsec/ch2_memsafe/lop_hoc_phan.h`, `tinh_tien_day.c` (domain và công thức gốc).
