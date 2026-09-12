# Báo cáo Lab 4 — Cấu trúc Dữ liệu Động & Công cụ Phân tích Tĩnh

**Học phần:** CSE703093 — An toàn phần mềm — Phenikaa University
**Module:** Quản lý Giảng viên dạng danh sách liên kết (**DuongUniversity Management System**)

Module này dùng **đúng domain thực tế** của hệ thống DuongUniversity — `GiangVienNode { hoTen[MAX_NAME=80], namVaoNghe, next }`, với `MAX_NAME=80` **giống hệt** hằng số thật trong `btl_softsec/ch2_memsafe/giang_vien.h` — thay vì ví dụ "Catalog sách/BookNode" chung chung của đề gốc. Tiếp nối Lab 3: lỗ hổng CWE-476 minh họa ở đây chính là **VULN-004** đã được liệt kê trong `lab3_secure_memory/dataset/vulnerabilities.json` với `"detected_by": "Code review / static analysis (Lab 4)"` — nghĩa là Lab 3 đã chủ động để dành lỗ hổng này cho Lab 4 phát hiện bằng phân tích tĩnh thay vì ASan.

Toàn bộ log trong báo cáo này là **log thật**, thu được bằng cách chạy `cppcheck 2.21.0` (cài qua MSYS2 `pacman -S mingw-w64-ucrt-x86_64-cppcheck`, vì môi trường mặc định chưa có sẵn) trực tiếp trên `c/booklist_v1_buggy.c` và `c/booklist_v2_fixed.c` — không phải log dựng minh họa.

---

## 1. Bảng đối chiếu: lỗi tự tìm bằng mắt (code review) vs. lỗi cppcheck phát hiện

### 1.1 Lỗi tự tìm bằng mắt (đọc code trước khi chạy công cụ)

| # | Vị trí | CWE | Mô tả tự phát hiện |
|---|---|---|---|
| 1 | `list_insert_front` | CWE-476 | `malloc()` không được kiểm tra `NULL` trước khi ghi `node->hoTen` — nếu hết bộ nhớ, đây là NULL pointer dereference. |
| 2 | `list_remove_by_name` | CWE-401 | Sau khi gỡ node ra khỏi danh sách (cập nhật `head`/`prev->next`), **không gọi `free(cur)`** — node bị "mồ côi", rò rỉ bộ nhớ vĩnh viễn. |
| 3 | `list_count_UNSAFE` | CWE-457 | Biến `count` khai báo nhưng không khởi tạo `= 0` — nếu gọi trên danh sách rỗng, vòng `while` không chạy lần nào, trả về giá trị rác. |

### 1.2 Lỗi cppcheck thực sự phát hiện được (`cppcheck --enable=all --inconclusive --xml`)

```text
=== cppcheck: booklist_v1_buggy.c (PHIEN BAN CO LOI) ===
  [WARNING] [CWE-476] dong 40: If memory allocation fails, then there is a possible null pointer dereference: node
  [WARNING] [CWE-476] dong 41: If memory allocation fails, then there is a possible null pointer dereference: node
  [WARNING] [CWE-476] dong 42: If memory allocation fails, then there is a possible null pointer dereference: node
  [WARNING] [CWE-457] dong 73: Uninitialized variable: count
  -> 4 finding lien quan bao mat (error/warning)
```
*(Ngoài ra còn 7 finding mức `style` thuần túy — gợi ý phong cách code như `const` pointer, static linkage — không tính vào "finding bảo mật" vì không liên quan CWE an toàn bộ nhớ.)*

### 1.3 Bảng đối chiếu

| Lỗi tự tìm (mục 1.1) | cppcheck có phát hiện? | Ghi chú |
|---|:---:|---|
| #1 CWE-476 (`list_insert_front`) | ✅ **Có** — 3 warning (dòng 40, 41, 42 — mỗi lần `node` được dereference) | Phát hiện chính xác, đúng dòng |
| #2 CWE-401 (`list_remove_by_name`) | ❌ **KHÔNG** — 0 finding nào đề cập leak | Xem giải thích mục 2 dưới |
| #3 CWE-457 (`list_count_UNSAFE`) | ✅ **Có** — 1 warning (dòng 73) | Phát hiện chính xác, đúng dòng |

**Kết quả: 2/3 lỗi tự tìm được cppcheck xác nhận, 1/3 bị bỏ sót — đúng 100% với nhận xét sư phạm nêu trong đề bài** ("cppcheck không luôn phát hiện được lỗi memory leak có luồng điều khiển phức tạp").

### 1.4 Vì sao cppcheck bỏ sót lỗi CWE-401 (memory leak)?

`list_remove_by_name` có **2 nhánh cập nhật `head`** (`prev == NULL` vs `prev != NULL`) trước khi `return head;` mà không giải phóng `cur`. Để phát hiện đây là leak, công cụ cần theo dõi rằng: (a) `cur` trỏ tới vùng nhớ do `malloc()` cấp phát ở một lệnh gọi hàm khác (`list_insert_front`, cách xa về mặt lời gọi hàm); (b) `cur` bị "ngắt kết nối" khỏi mọi biến còn sống ngay tại điểm `return`. Đây là bài toán **phân tích luồng dữ liệu liên thủ tục (interprocedural data-flow)** phức tạp hơn nhiều so với phát hiện "biến cục bộ chưa gán giá trị trước khi đọc" (CWE-457) — vốn chỉ cần phân tích nội bộ 1 hàm. cppcheck (ở chế độ mặc định, kể cả bật `--enable=all --inconclusive`) không đủ mạnh để suy luận loại sở hữu con trỏ (pointer ownership) qua nhiều hàm như vậy.

---

## 2. Bản tự sửa lỗi kèm log cppcheck xác nhận 0 finding

`c/booklist_v2_fixed.c` sửa cả 3 lỗi: `if (node == NULL) return head;` (CWE-476), thêm `free(cur);` trước `return head;` (CWE-401), và `int count = 0;` (CWE-457).

```text
=== cppcheck: booklist_v2_fixed.c (PHIEN BAN DA SUA) ===
  -> 0 finding lien quan bao mat (error/warning)
```

Xác nhận qua test tự động (`make test`):
```text
[PASS] test_buggy_compiles_and_runs
[PASS] test_fixed_compiles_and_runs_correct_count
[PASS] test_cppcheck_detects_issues_in_buggy_version
[PASS] test_cppcheck_clean_on_fixed_version
[PASS] test_matches_baseline

5/5 test da PASS
```

---

## 3. Trade-off: cppcheck (tĩnh) vs. AddressSanitizer (động, Lab 3) cho pipeline CI/CD

| Tiêu chí | cppcheck (phân tích tĩnh) | ASan (phân tích động, Lab 3) |
|---|---|---|
| **Cần chạy chương trình?** | Không — chỉ phân tích AST/CFG | Có — phải biên dịch + thực thi với input thật |
| **Tốc độ** | Rất nhanh (mili-giây tới vài giây/file), không cần input | Chậm hơn (cần build + chạy từng kịch bản, phụ thuộc coverage input) |
| **Độ phủ (coverage)** | Xét được **mọi nhánh code cùng lúc** (kể cả nhánh hiếm gặp không ai từng chạy tới) | Chỉ phát hiện lỗi trên **đường thực thi thực tế** đã chạy qua — bỏ sót nhánh chưa được test |
| **Bằng chứng thật từ 2 lab** | Bắt được CWE-476 + CWE-457 tốt (lỗi cục bộ trong 1 hàm); **bỏ sót CWE-401** (leak liên hàm) | Bắt được CWE-121/416/401 rất tốt (kể cả CWE-401 mà cppcheck bỏ sót ở đây!) NHƯNG có giới hạn riêng: tràn bộ đệm bên trong 1 struct có thể không bị bắt nếu không chạm biên vùng cấp phát (xem `lab3_secure_memory/REPORT.md` mục 2) |
| **Yêu cầu hạ tầng** | Chỉ cần cài cppcheck, không cần biên dịch được chương trình | Cần toolchain hỗ trợ `-fsanitize=address` thật (đã gặp vấn đề này ở Lab 3 — GCC MSYS2 UCRT64 mặc định KHÔNG có, phải cài Clang riêng) |
| **False negative đặc trưng** | Lỗi có data-flow phức tạp qua nhiều hàm (memory leak) | Lỗi chỉ xảy ra trên input/nhánh chưa từng được test tới |

**Nếu CHỈ được chọn một công cụ cho CI/CD:** chọn **ASan (động)**, với lý do cụ thể dựa trên bằng chứng thật thu được từ chính 2 lab này — ASan đã chứng minh bắt được **cả 3 loại lỗi bộ nhớ** (buffer overflow, UAF, và **cả memory leak** mà cppcheck bỏ sót ở Lab 4 này), trong khi cppcheck chỉ bắt được 2/3. Tuy nhiên đây là lựa chọn có đánh đổi thật, không phải "ASan luôn tốt hơn tuyệt đối":
- ASan cần chương trình build được và có **bộ test case chạy tới đúng nhánh lỗi** — nếu CI không có test coverage tốt, lỗi ở nhánh chưa test sẽ không bao giờ lộ diện.
- cppcheck chạy **nhanh hơn và không cần build/test** — phù hợp làm **pre-commit hook** hoặc bước gate đầu tiên (rẻ, tức thời), trong khi ASan phù hợp làm bước **kiểm thử tích hợp** sâu hơn (đắt hơn, chạy sau).

**Kết luận thực tế:** một pipeline CI/CD tốt nên dùng **cả hai theo tầng** (cppcheck ở bước lint nhanh trên mọi commit, ASan ở bước test tích hợp trước khi merge) — đúng như tinh thần "bổ sung cho nhau" mà đề bài đã nêu; nhưng nếu ngân sách hạ tầng chỉ cho phép một công cụ, bằng chứng thật từ 2 lab này cho thấy ASan bắt được nhiều lớp lỗi bộ nhớ nghiêm trọng hơn.

---

## 4. Kết luận

- Module dùng đúng domain thật (`GiangVienNode`, `MAX_NAME=80`) của DuongUniversity Management System, nối tiếp đúng lỗ hổng VULN-004 (CWE-476) mà Lab 3 đã để dành cho Lab 4.
- Đối chiếu thật xác nhận: cppcheck phát hiện đúng 2/3 lỗi tự tìm bằng mắt (CWE-476, CWE-457), bỏ sót CWE-401 (memory leak) — đúng 100% với dự đoán sư phạm của đề bài, có giải thích kỹ thuật cụ thể (data-flow liên hàm).
- Bản sửa lỗi đạt 0 finding bảo mật, `make test` → 5/5 PASS thật.
- Lập luận trade-off cppcheck/ASan dựa trên bằng chứng thật thu được từ chính Lab 3 và Lab 4, không chỉ suy luận lý thuyết.
