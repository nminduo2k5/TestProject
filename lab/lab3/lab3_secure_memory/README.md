# Lab 3 — Lập trình C An toàn: Quản lý Bộ nhớ & Đánh giá Rủi ro

**Chủ đề xuyên suốt:** DuongUniversity Management System
**Module con:** Quản lý Học phần & Giảng viên (dùng đúng domain `GiangVien`/`HocPhan` như `btl_softsec/ch2_memsafe`, không phải ví dụ "Inventory/Book/Lecturer thư viện" chung chung của đề gốc)
**Ánh xạ đề cương:** Chương 2 — 2.1 Đánh giá rủi ro, 2.3 Lập trình C an toàn (Quản lý bộ nhớ)
**Báo cáo kết quả đầy đủ (log thật, không phải minh họa):** [`REPORT.md`](REPORT.md)

## 0. Yêu cầu môi trường (đọc trước khi chạy)

`-fsanitize=address` cần một runtime ASan (compiler-rt) thật. **GCC mặc định của
MSYS2 UCRT64** (thường có sẵn trên PATH ở Windows) **không kèm `libasan`**, biên
dịch sẽ báo lỗi linker. Dự án này dùng **Clang của môi trường MSYS2 `clang64`**
(có compiler-rt đầy đủ, ASan chạy thật trên Windows). Cài đặt một lần bằng
"MSYS2 CLANG64" shell:

```bash
pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld
```

`Makefile` và `tests/test_memory_safety.py` đã trỏ thẳng tới
`C:\msys64\clang64\bin\clang.exe` và tự động copy 2 DLL runtime cần thiết
(`libclang_rt.asan_dynamic-x86_64.dll`, `libc++.dll`) vào `c/` sau khi build,
nên các binary chạy được ngay không cần sửa PATH hệ thống.

> **LeakSanitizer không được hỗ trợ trên Windows** (giới hạn chính thức của
> LLVM/compiler-rt, xem [wiki AddressSanitizerLeakSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer),
> mục "Supported Platforms" — chỉ Linux/macOS/NetBSD/Fuchsia). Vì vậy CWE-401
> được xác nhận bằng một **custom leak tracker** thật (đếm `malloc`/`free`
> qua `atexit()`, xem đầu file `c/vulnerable_inventory.c`/`c/secure_inventory.c`)
> thay vì `ASAN_OPTIONS=detect_leaks=1` (cờ này còn khiến ASan abort trước khi
> `main()` chạy trên Windows nếu bật — xem chi tiết trong comment của
> `tests/test_memory_safety.py`).

## 1. Mục tiêu học tập

- Nhận diện và tái hiện 3 lớp lỗi bộ nhớ phổ biến trong C: **Buffer Overflow (CWE-121)**, **Use-After-Free (CWE-416)**, **Memory Leak (CWE-401)**.
- Sử dụng **AddressSanitizer (ASan)** để phát hiện lỗi bộ nhớ tại runtime.
- Sửa lỗi theo các nguyên tắc lập trình C an toàn: `snprintf` thay `strcpy`, đặt con trỏ `NULL` sau `free`, đảm bảo mọi `malloc` có `free` tương ứng.
- Áp dụng một **mô hình đánh giá rủi ro** (risk assessment) đơn giản hóa theo tinh thần CVSS để định lượng và xếp hạng mức độ nghiêm trọng của lỗ hổng, phục vụ ra quyết định ưu tiên khắc phục.
- Hiểu rõ **giới hạn của công cụ**: vì sao lỗi tràn bộ đệm *bên trong* một struct có thể không bị ASan phát hiện, trong khi tràn bộ đệm heap độc lập thì luôn bị bắt.

## 2. Bối cảnh bài toán

Module quản lý `HocPhan` (`id`, `maLop[MAX_MALOP=20]`, `soTiet`, và **con trỏ** `gv_ptr` tới `GiangVien` phụ trách) và `GiangVien` (`id`, `hoTen[MAX_NAME=80]`, `is_deleted`) — dùng **đúng hằng số và kiến trúc con trỏ liên-struct** của **DuongUniversity Management System** (xem `btl_softsec/ch2_memsafe/giang_vien.h`, `lop_hoc_phan.h`), không chỉ đổi tên biến. File `c/vulnerable_inventory.c` cố ý chứa 3 lỗi bộ nhớ kinh điển (cùng bản chất với CWE-120 tại `lop_hoc_phan.c`/`giang_vien.c` và CWE-416 tại `giang_vien.c` đang tồn tại thật trong hệ thống); `c/secure_inventory.c` là bản đã sửa. Cả hai đều hỗ trợ 4 chế độ dòng lệnh: `overflow`, `uaf`, `leak`, và `fmt` (CWE-134, VULN-005 tự thêm — xem mục 3 REPORT.md).

## 3. Các bước thực hành

### Bước 1 — Đọc code, dự đoán lỗi trước khi chạy
Đọc `vulnerable_inventory.c`, với mỗi hàm, dự đoán: lỗi gì, điều kiện nào kích hoạt, hậu quả gì (CWE nào).

### Bước 2 — Biên dịch với AddressSanitizer và tái hiện từng lỗi
```bash
make
./c/vulnerable_inventory overflow "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
./c/vulnerable_inventory uaf
ASAN_OPTIONS=detect_leaks=1 ./c/vulnerable_inventory leak
```
Đọc kỹ output của ASan: địa chỉ lỗi, stack trace, loại lỗi.

### Bước 3 — Thí nghiệm quan trọng: tràn trong struct KHÔNG luôn bị bắt
Chạy `add_hocphan_malop_UNSAFE` (tràn trong struct `HocPhan`) qua chế độ `safe_input` và so sánh với `add_hocphan_malop_UNSAFE_HEAP` (chế độ `overflow`). **Lưu ý về độ dài input:** vì `HocPhan` chỉ có 40 byte, input quá dài (vd. 39 ký tự) sẽ tràn qua cả biên ngoài của biến struct và **vẫn bị ASan bắt** (`stack-buffer-overflow`) — dùng input **~30 ký tự** để tràn đúng field `maLop[20]` mà không chạm biên ngoài, minh họa đúng hiện tượng "không bị bắt":
```bash
./c/vulnerable_inventory.exe safe_input CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
```
Giải thích trong báo cáo **vì sao** ASan không luôn phát hiện lỗi loại này (gợi ý: redzone chỉ đặt ở biên vùng cấp phát, không đặt giữa các field của cùng một struct) — xem thực nghiệm thật, kèm bằng chứng con trỏ `gv_ptr` bị ghi đè một phần, trong `REPORT.md` mục 2.

### Bước 4 — Đối chiếu bản đã sửa
```bash
./c/secure_inventory overflow "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
./c/secure_inventory uaf
ASAN_OPTIONS=detect_leaks=1 ./c/secure_inventory leak
```
Không có lỗi nào được báo. Với `overflow`, quan sát chuỗi bị **cắt bớt (truncated)** thay vì tràn.

### Bước 5 — Đánh giá rủi ro định lượng
```bash
make risk-report
```
Đọc `dataset/vulnerabilities.json`, hiểu ý nghĩa từng trường (Attack Vector, Attack Complexity, Privileges Required, User Interaction, C/I/A Impact) và cách `python/risk_assessor.py` tính điểm.

### Bước 6 — Bổ sung một lỗ hổng mới vào dataset
Đã thêm `VULN-005` (CWE-134, Uncontrolled Format String) vào `dataset/vulnerabilities.json`, kèm demo thật ở chế độ `fmt` trong cả 2 file `.c` (`tra_cuu_hocphan_UNSAFE`/`_SAFE`). Xem giải thích vị trí xếp hạng (8.1, HIGH) trong `REPORT.md` mục 3.1.
```bash
make risk-report
./c/vulnerable_inventory.exe fmt "%x %x %x %x %n"
./c/secure_inventory.exe fmt "%x %x %x %x %n"
```

### Bước 7 — Chạy bộ test tự động
```bash
make test
```

## 4. Yêu cầu hoàn thiện (Deliverables)

1. ✅ Bảng liệt kê 3 lỗi (địa chỉ, loại ASan report, stack trace rút gọn) — `REPORT.md` mục 1.
2. ✅ Giải thích bằng lời + ví dụ cụ thể cho hiện tượng ở Bước 3 (tràn trong struct không bị bắt) — `REPORT.md` mục 2, kèm log thực nghiệm thật.
3. N/A Diff code sửa lỗi (không áp dụng — mọi hàm VULN đều đã có sẵn bản `_SAFE`/`_FIXED` tương ứng).
4. ✅ Báo cáo đánh giá rủi ro đầy đủ 5 lỗ hổng (bao gồm `VULN-005` tự thêm — CWE-134), có thứ tự ưu tiên khắc phục — `REPORT.md` mục 3.
5. ✅ Log `make test` toàn bộ PASS — `REPORT.md` mục 4.

## 5. Yêu cầu kết quả

- ✅ ASan phát hiện đủ 3/3 lỗi trên bản vulnerable (`heap-buffer-overflow`, `heap-use-after-free`, và leak qua custom tracker vì LeakSanitizer không hỗ trợ Windows), 0/3 lỗi trên bản secure.
- ✅ `tests/test_memory_safety.py` toàn bộ 8 test PASS (`make test`).
- ✅ Kết quả đánh giá rủi ro khớp với `dataset/expected_risk_baseline.json` (dung sai 0.05 điểm) — đã bao gồm cả `VULN-005`.

## 6. Sơ đồ luồng dữ liệu (Dataflow)

```
 c/vulnerable_inventory.c  --clang -fsanitize=address-->  Binary co ASan that
            │                                                 │
            │ (chay 4 kich ban: overflow / uaf / leak / fmt)   ▼
            │                              Bao cao loi runtime (ASan / custom leak tracker)
            ▼
 dataset/vulnerabilities.json (mo ta CWE + thuoc tinh CVSS-lite)
            │
            ▼
 python/risk_assessor.py  (tinh Exploitability + Impact subscore)
            │
            ▼
 dataset/risk_assessment_results.json  <--so sanh-->  dataset/expected_risk_baseline.json
            │
            ▼
 tests/test_memory_safety.py  (doi chieu tu dong ASan + diem rui ro)
```

## 7. Tài liệu tham khảo
- Đề cương CSE703093 — An toàn phần mềm, Chương 2 (2.1, 2.3).
- CWE-121, CWE-416, CWE-401, CWE-476, CWE-134 (cwe.mitre.org).
- FIRST.org — Common Vulnerability Scoring System (CVSS) v3.1 Specification.
- Google/Sanitizers wiki — AddressSanitizerLeakSanitizer, mục "Supported Platforms" (giới hạn LeakSanitizer trên Windows).
