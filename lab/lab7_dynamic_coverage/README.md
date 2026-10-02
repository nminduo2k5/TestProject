# Lab 7 — Phân tích Động: Phủ mã (Code Coverage) & Giám sát Thực thi

**Chủ đề xuyên suốt:** DuongUniversity Management System
**Module con:** Tính tiền dạy (Module 3) — hàm `calculate_salary(soTiet, heSoHocPhan, soLuongSinhVien, bangCap)` viết lại từ `calculate_e2e_salary_SAFE()` + bảng hệ số bằng cấp của `add_lecturer_SAFE()` trong `btl_softsec/ch2_memsafe` (không phải ví dụ "xử lý đơn hàng" chung chung của đề gốc)
**Ánh xạ đề cương:** Chương 4 — 4.1 Giới thiệu kiểm thử bảo mật, 4.2 Phủ mã nguồn, 4.3 Theo dõi thực thi chương trình, 4.4 Tạo đường thực thi chương trình
**Báo cáo kết quả đầy đủ (log thật, không phải minh họa):** [`REPORT.md`](REPORT.md)

## 0. Yêu cầu môi trường (đọc trước khi chạy)

Chỉ cần **gcc + gcov của MSYS2 UCRT64** (có sẵn trên PATH, gcc/gcov 16.1.0) và Python bất kỳ (không cần z3, không cần clang). `run_lab7.bat` tự ưu tiên Anaconda Python nếu có; `mingw32-make test` dùng `python` mặc định — cả hai đều đã chạy thật PASS.

## 1. Mục tiêu học tập

- Đo độ phủ mã (**line coverage** và **branch coverage**) bằng `gcov -b` cho một hàm nhiều nhánh lồng nhau.
- Hiểu rõ khoảng cách giữa "test PASS 100%" và "coverage cao" — hai khái niệm độc lập: bộ `partial` 2/2 PASS nhưng chỉ phủ **72% dòng / 44% nhánh**.
- Áp dụng **sinh test tổ hợp** (combinatorial testing) từ lớp tương đương để chủ động tăng độ phủ thay vì viết test ngẫu nhiên.
- Xây dựng **oracle độc lập** (`expected_status()` viết lại đặc tả bằng Python, tách biệt khỏi code C) để tự động gán nhãn kỳ vọng.
- Nhận ra giới hạn của coverage: các dòng/nhánh **không thể** phủ từ tầng nghiệp vụ, và việc thêm giá trị biên **không làm tăng coverage** nhưng vẫn cần thiết (phát hiện off-by-one `>` vs `>=`).

## 2. Bối cảnh bài toán

`calculate_salary()` gộp các ràng buộc đã đặc tả trong BTL thành một hàm nhiều nhánh:

| Ràng buộc | Nguồn trong BTL | Nhánh |
|---|---|---|
| `0 < soTiet ≤ 500` | CON-12 (guard trên thiếu ở bản VULN) | `INVALID_SOTIET` |
| `heSoHocPhan > 0` | `create_class_section_SAFE` | `INVALID_HESO` |
| `0 ≤ soLuongSinhVien ≤ 300` | tab:range | `INVALID_SV` |
| `bangCap ∈ {GS 2.0, PGS 1.8, TIEN_SI 1.5, THAC_SI 1.2, CU_NHAN 1.0}` | `add_lecturer_SAFE`, CON-13, CWE-1288 | 5 nhánh hợp lệ + `INVALID_DEGREE` (**từ chối** thay vì fallback) |
| `heSoQuyMo = 0.2` nếu `soLuongSinhVien > 50` | CON-11 | 2 nhánh, **lồng** kiểm tra audit byte `> 127` (CON-5 / CWE-197 `pack_class_size_byte_SAFE`) |
| `tienDay > 50 000 000` → `APPROVAL_REQUIRED` | kiểm soát chi bất thường (tương tự ngưỡng phê duyệt đơn hàng) | 2 nhánh |

Công thức: `tienDay = soTiet × (heSoHocPhan + heSoQuyMo) × heSoBangCap × 85000` tính bằng `double`/`long long` (FIX CWE-190).

## 3. Các bước thực hành

### Bước 1 — Vẽ cây quyết định của `calculate_salary()`
Cây quyết định và số đường thực thi lý thuyết: `REPORT.md` mục 1.

### Bước 2 — Chạy với bộ test KHÔNG đầy đủ, quan sát coverage thấp
```bash
python python/coverage_runner.py          # chay ca 4 bo, in bang so sanh
```
`salary_test_inputs_partial.csv` chỉ có 2 case (cùng TIEN_SI, cùng lớp > 50 SV) — **cả 2 đều PASS** nhưng bỏ sót 24 dòng và 34/61 nhánh.

### Bước 3 — So sánh với bộ test đầy đủ
`salary_test_inputs_full.csv` (13 case) phủ mọi trạng thái trả về: coverage tăng **72.09% → 94.19%** (dòng) và **44.26% → 77.05%** (nhánh). 5 dòng còn lại là nhánh lỗi CLI / `default` của `switch` — không thuộc logic nghiệp vụ.

### Bước 4 — Tự sinh test tổ hợp
```bash
python python/test_case_generator.py            # 5 x 3 x 5 x 6 = 450 case
```
Đọc `expected_status()` — oracle độc lập. Vì sao không được dùng chính hàm C làm oracle: `REPORT.md` mục 5.

### Bước 5 — Thêm lớp tương đương mới (giá trị biên)
```bash
python python/test_case_generator.py --extended # them sv = 50 va 51 -> 630 case
```
`sv = 50` nằm **đúng tại ngưỡng** CON-11 (không được hệ số quy mô vì điều kiện là `> 50`), `sv = 51` ngay trên ngưỡng. Kết quả và phân tích vì sao coverage **không đổi** nhưng test vẫn có giá trị: `REPORT.md` mục 4.

### Bước 6 — Chạy bộ test tự động
```bash
mingw32-make test        # hoac run_lab7.bat
```

## 4. Yêu cầu hoàn thiện (Deliverables)

1. ✅ Cây quyết định tự vẽ (Bước 1), đối chiếu log coverage thực tế theo số dòng — `REPORT.md` mục 1.
2. ✅ Bảng so sánh % coverage (line + branch) của 4 bộ test: partial / full / combinatorial / combinatorial_extended — `REPORT.md` mục 2.
3. ✅ Giải thích 5 dòng và 14 nhánh KHÔNG THỂ đạt 100% dù đã thử mọi tổ hợp nghiệp vụ hợp lệ — `REPORT.md` mục 3.
4. ✅ Lớp tương đương mới `sv = 50/51` (Bước 5) kèm log coverage mới — `REPORT.md` mục 4.

## 5. Yêu cầu kết quả

- ✅ `tests/test_coverage.py` **5/5 PASS** (4 test theo đề + 1 test bổ sung cho lớp biên).
- ✅ Bộ `full` phủ cao hơn bộ `partial` **22.1 điểm** (yêu cầu ≥ 5).
- ✅ Bộ tổ hợp tự sinh đạt coverage **bằng** bộ `full` (94.19% / 77.05%) với 450/450 PASS.

## 6. Sơ đồ luồng dữ liệu (Dataflow)

```
 c/tinh_tien_day_coverage.c  --gcc --coverage -DSALARY_CLI_MAIN-->  c/tinh_tien_day_cli.exe (instrumented)
            │
            ▼ (chay voi tung bo du lieu test)
 dataset/salary_test_inputs_{partial,full,combinatorial,combinatorial_extended}.csv
            │
            ▼
 python/coverage_runner.py  --gcov -b-->  % line + % branch + danh sach dong chua phu
            │
            ▲
 python/test_case_generator.py [--extended] (lop tuong duong x oracle doc lap expected_status())
            │
            ▼
 dataset/coverage_comparison_results.json
            │
            ▼
 tests/test_coverage.py (doi chieu tu dong 4 bo test, 5 test)
```

## 7. Tài liệu tham khảo
- Đề cương CSE703093 — An toàn phần mềm, Chương 4 (4.1–4.4).
- P. Ammann, J. Offutt, *Introduction to Software Testing* — Combinatorial Testing, Equivalence Partitioning, Boundary Value Analysis.
- GCC Manual — *gcov: a Test Coverage Program* (`-b` branch probabilities).
- `btl_softsec/ch2_memsafe/tinh_tien_day.c`, `giang_vien.c` (đặc tả và công thức gốc).
