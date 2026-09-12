# Lab 4 — Cấu trúc Dữ liệu Động & Công cụ Phân tích Tĩnh

**Chủ đề xuyên suốt:** DuongUniversity Management System
**Module con:** Quản lý Giảng viên dạng danh sách liên kết (tiếp nối Lab 3 — dùng đúng hằng số `MAX_NAME=80` thật trong `btl_softsec/ch2_memsafe/giang_vien.h`, không phải ví dụ "Catalog sách/BookNode" chung chung của đề gốc)
**Ánh xạ đề cương:** Chương 2 — 2.2 Cấu trúc động, 2.5 Công cụ phân tích tĩnh tìm lỗi bảo mật
**Báo cáo kết quả đầy đủ (log thật, không phải minh họa):** [`REPORT.md`](REPORT.md)

## 0. Yêu cầu môi trường (đọc trước khi chạy)

Cần cài `cppcheck` (chưa có sẵn theo mặc định). Cài một lần qua MSYS2 pacman:
```bash
pacman -S mingw-w64-ucrt-x86_64-cppcheck
```
Sau khi cài, `cppcheck` gọi được trực tiếp (không cần thêm PATH thủ công) vì `C:\msys64\ucrt64\bin` đã có sẵn trên PATH hệ thống — khác với Lab 3 (cần `clang64` riêng cho ASan).

## 1. Mục tiêu học tập

- Cài đặt và thao tác trên danh sách liên kết đơn (singly linked list) cấp phát động trong C.
- Sử dụng công cụ phân tích tĩnh **cppcheck** để phát hiện lỗi mà **không cần chạy chương trình**.
- Đọc hiểu báo cáo XML của công cụ phân tích tĩnh, phân biệt mức độ `error` / `warning` / `style` / `information`.
- Hiểu rõ **giới hạn** của phân tích tĩnh: vì sao cppcheck phát hiện tốt "uninitialized variable" nhưng khó phát hiện memory leak có luồng điều khiển phức tạp — từ đó thấy được vai trò bổ sung của phân tích động (ASan ở Lab 3, fuzzing ở Lab 8).

## 2. Bối cảnh bài toán

`booklist_v1_buggy.c` cài đặt **danh sách Giảng viên** (`GiangVienNode { hoTen[MAX_NAME], namVaoNghe, next }`) bằng linked list — đúng domain thực tế của DuongUniversity Management System (`MAX_NAME=80` giống hệt `giang_vien.h` thật), chứa 3 lỗi tinh vi: thiếu kiểm tra `malloc` trả về NULL (`list_insert_front`, CWE-476), thiếu `free()` khi xóa node (`list_remove_by_name`, CWE-401), và biến đếm không được khởi tạo (`list_count_UNSAFE`, CWE-457). `booklist_v2_fixed.c` là bản đã sửa.

> **Lưu ý chính xác:** các hàm `add_lecturer_VULN()`/`create_class_section_VULN()` THẬT trong `btl_softsec/ch2_memsafe/giang_vien.c`/`lop_hoc_phan.c` **đều đã kiểm tra `malloc` trả về NULL** (`if (!gv) return NULL;`) — nên `list_insert_front` ở đây KHÔNG phải bản sao của một bug cụ thể đã tồn tại trong `btl_softsec`. Đây chính là lỗ hổng **VULN-004 (CWE-476)** đã được liệt kê trong `lab3_secure_memory/dataset/vulnerabilities.json` với `"detected_by": "Code review / static analysis (Lab 4)"` — tức lab3 đã **chủ động để dành** lỗ hổng này cho Lab 4 minh họa bằng phân tích tĩnh, thay vì bằng ASan. Lab 4 hiện thực hoá đúng lời hẹn đó.

## 3. Các bước thực hành

### Bước 1 — Tự tìm lỗi bằng mắt (code review) trước khi chạy công cụ
Đọc `booklist_v1_buggy.c`, đánh dấu nghi ngờ tại mỗi hàm.

### Bước 2 — Biên dịch và chạy thử cả 2 phiên bản
```bash
make
./c/booklist_v1
./c/booklist_v2
```
**Lưu ý quan trọng (đã xác minh thật):** `main()` của bản buggy chỉ gọi `list_count_UNSAFE()` trên danh sách **không rỗng** (3 giảng viên), nên biến `count` chưa khởi tạo vẫn vô tình cho ra số đúng (3) — lỗi **không hiện rõ** qua output mặc định, đúng như comment trong code (`"chi de minh hoa, khong luon kich hoat duoc"`). Để tự thấy giá trị rác thật, gọi hàm trên danh sách rỗng: đã thử nghiệm thật `list_count_UNSAFE(NULL)` cho ra `156` rồi `6` ở 2 lần chạy khác nhau — xác nhận đây là hành vi không xác định (UB) thật, không phải suy luận lý thuyết.

### Bước 3 — Chạy cppcheck và đọc báo cáo
```bash
make cppcheck-report
```
Đối chiếu các finding với dự đoán ở Bước 1. Với mỗi finding, tra cứu mã CWE tương ứng trên cwe.mitre.org.

### Bước 4 — Tìm lỗi mà cppcheck KHÔNG phát hiện được
Bản buggy còn lỗi memory leak (`list_remove_by_name` thiếu `free(cur)`). **Đã xác nhận thật** (không chỉ suy luận): ngay cả với `--enable=all --inconclusive` (đã bật sẵn trong script, xem `REPORT.md` mục 1), cppcheck 2.21.0 **vẫn không báo lỗi này** — 0/4 finding bảo mật trên bản buggy liên quan đến memory leak, dù đã bật toàn bộ mức phân tích. Đây là bằng chứng thật cho nhận xét sư phạm của đề bài: cppcheck không theo dõi tốt data-flow qua nhiều nhánh `return`.

### Bước 5 — Sửa lỗi thủ công (không nhìn bản mẫu) rồi so sánh
Copy `booklist_v1_buggy.c` sang file mới, tự sửa từng lỗi, chạy lại cppcheck cho đến khi 0 finding bảo mật, rồi so sánh với `booklist_v2_fixed.c`.

### Bước 6 — Chạy bộ test tự động
```bash
make test
```

## 4. Yêu cầu hoàn thiện (Deliverables)

1. ✅ Bảng đối chiếu: lỗi tự tìm bằng mắt (Bước 1) vs. lỗi cppcheck phát hiện (Bước 3) — `REPORT.md` mục 1.
2. ✅ Bản tự sửa lỗi (Bước 5) kèm log cppcheck xác nhận 0 finding bảo mật — `REPORT.md` mục 2.
3. ✅ Lập luận trade-off cppcheck (tĩnh) vs. ASan (động) cho pipeline CI/CD — `REPORT.md` mục 3.

## 5. Yêu cầu kết quả

- ✅ `tests/test_static_analysis.py` toàn bộ 5 test PASS (`make test`).
- ✅ Bản fixed đạt 0 finding cppcheck mức `error`/`warning`.
- ✅ Bản buggy có **4** finding mức `error`/`warning` bị phát hiện thật (≥ 2 theo yêu cầu) — 3× CWE-476 + 1× CWE-457. **Không có finding nào cho CWE-401 (memory leak)** — xác nhận thật đúng nhận xét sư phạm của đề bài.

## 6. Sơ đồ luồng dữ liệu (Dataflow)

```
 c/booklist_v1_buggy.c , c/booklist_v2_fixed.c
            │
            ▼ (khong bien dich, chi phan tich AST/CFG)
 cppcheck --enable=all --inconclusive --xml
            │
            ▼
 python/static_analysis_runner.py  (parse XML, loc theo severity)
            │
            ▼
 dataset/cppcheck_comparison_results.json  <--so sanh-->  expected_cppcheck_baseline.json
            │
            ▼
 tests/test_static_analysis.py (doi chieu tu dong)
```

## 7. Tài liệu tham khảo
- Đề cương CSE703093 — An toàn phần mềm, Chương 2 (2.2, 2.5).
- cppcheck.sourceforge.io — tài liệu chính thức.
- CWE-457 (Use of Uninitialized Variable), CWE-401 (Memory Leak), CWE-476 (NULL Pointer Dereference).


Thư mục làm việc: K:\TestProject\lab\lab4_data_structures_static_analysis\lab4_data_structures_static_analysis

Cách 1 — chạy toàn bộ 1 lệnh (khuyên dùng):


cd K:\TestProject\lab\lab4_data_structures_static_analysis\lab4_data_structures_static_analysis
make test
Lệnh này tự biên dịch cả 2 bản, chạy cppcheck, và in ra 5/5 test da PASS.

Cách 2 — chạy từng bước để xem chi tiết:


# 1. Biên dịch cả 2 bản
make

# 2. Chạy thử chương trình
./c/booklist_v1      # bản buggy
./c/booklist_v2      # bản đã sửa

# 3. Xem báo cáo cppcheck chi tiết (kèm lưu JSON)
make risk-report      # (tên đúng trong Makefile là: cppcheck-report)

# 4. Chạy bộ test tự động
make test
Lưu ý sửa nhỏ ở bước 3, lệnh đúng là:


make cppcheck-report
Yêu cầu môi trường (chỉ cần làm 1 lần): nếu máy bạn chưa có cppcheck:


pacman -S mingw-w64-ucrt-x86_64-cppcheck