# Báo cáo Lab 3 — Lập trình C An toàn: Quản lý Bộ nhớ & Đánh giá Rủi ro

**Học phần:** CSE703093 — An toàn phần mềm — Phenikaa University
**Module:** Quản lý Học phần & Giảng viên (**DuongUniversity Management System**)

Module này dùng **đúng kiến trúc struct thực tế** của hệ thống DuongUniversity (xem `btl_softsec/ch2_memsafe/giang_vien.h`, `lop_hoc_phan.h`) — không chỉ đổi tên biến, mà tái hiện đúng cơ chế:
- Hằng số `MAX_NAME=80`, `MAX_MALOP=20` **giống hệt** bản thật.
- `HocPhan.gv_ptr` là **con trỏ `GiangVien*` thật** (không phải chuỗi tên copy) — đúng cơ chế liên kết chéo-module đang gây ra CWE-416/476 thật trong hệ thống (Module 2 giữ con trỏ tới Module 1).
- Trường gây tràn (`maLop[MAX_MALOP]`) dùng đúng tên và kích thước thật.

Toàn bộ log trong báo cáo này là **log thật**, thu được bằng cách biên dịch `c/vulnerable_inventory.c` và `c/secure_inventory.c` với `-fsanitize=address` bằng **Clang 22.1.8 (môi trường MSYS2 `clang64`)** và chạy trực tiếp trên máy — không phải log dựng minh họa.

> **Ghi chú môi trường quan trọng:** GCC mặc định của MSYS2 UCRT64 (thường có sẵn trên PATH ở Windows) **không kèm runtime `libasan`**, nên `-fsanitize=address` báo lỗi linker (`ld returned 1/5 exit status`). Đã cài đặt bộ công cụ Clang của môi trường `clang64` (có `compiler-rt` đầy đủ, hỗ trợ ASan thật trên Windows) để khắc phục — xem chi tiết trong `Makefile`/`tests/test_memory_safety.py`.

---

## 1. Bảng liệt kê 3 lỗi kèm stack trace rút gọn

### 1.1 CWE-121 — Heap Buffer Overflow (`add_hocphan_malop_UNSAFE_HEAP`)

Lệnh: `.\vulnerable_inventory.exe overflow AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (39 ký tự, buffer `MAX_MALOP=20` — **đúng hằng số thật** trong `lop_hoc_phan.h`)

```text
==20376==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12bbc05a0054
WRITE of size 40 at 0x12bbc05a0054 thread T0
    #0 0x7ff9467b90d9 in strcpy (...\libclang_rt.asan_dynamic-x86_64.dll+0x1800490d9)
    #1 0x7ff6f86c14d1 in add_hocphan_malop_UNSAFE_HEAP c/vulnerable_inventory.c:114:5
    #2 0x7ff6f86c1bfc in main c/vulnerable_inventory.c:184:23

0x12bbc05a0054 is located 0 bytes after 20-byte region [0x12bbc05a0040,0x12bbc05a0054)
allocated by thread T0 here: ... in malloc
```

**Nhận xét:** ASan chèn "redzone" ngay sau khối `malloc(MAX_MALOP=20)` (mã lớp cấp phát heap độc lập); ghi 40 byte (39 ký tự + `\0`) chạm redzone → bắt được ngay tại `strcpy()`.

### 1.2 CWE-416 — Heap Use-After-Free qua con trỏ liên-struct (`demo_use_after_free`)

Lệnh: `.\vulnerable_inventory.exe uaf`

```text
==21072==ERROR: AddressSanitizer: heap-use-after-free on address 0x1285749a0024
READ of size 1 at 0x1285749a0024 thread T0
    #0 0x7ff9467b25de in strnlen (...\libclang_rt.asan_dynamic-x86_64.dll+0x1800425de)
    #1-#6 ... (ucrtbase.dll, chuoi goi noi bo cua printf khi doc chuoi %s)
    #7 0x7ff6f86c383e in printf (vulnerable_inventory.exe+0x14000383e)
    #8 0x7ff6f86c177c in demo_use_after_free c/vulnerable_inventory.c:143:5
```

**Nhận xét:** Đây **chính xác là cơ chế thật** trong `btl_softsec` — `HocPhan hp` giữ con trỏ `hp.gv_ptr` trỏ tới một `GiangVien` cấp phát động. Khi `free(gv)` được gọi mà **không cập nhật `hp.gv_ptr = NULL`** (y hệt lỗi thật trong `giang_vien.c` hàm `delete_lecturer_VULN`), dòng code sau đó đọc `hp.gv_ptr->hoTen` — ASan bắt được ngay việc đọc chuỗi (`strnlen` bên trong `printf("%s", ...)`) từ vùng nhớ đã giải phóng.

### 1.3 CWE-401 — Memory Leak (`demo_memory_leak`, struct `HocPhan`)

`LeakSanitizer` (thành phần phát hiện leak của ASan) **không được hỗ trợ trên Windows** ở bất kỳ trình biên dịch nào — đây là giới hạn nền tảng chính thức của LLVM/compiler-rt (xem mục 2.2). Chạy thử xác nhận:

```text
$ vulnerable_inventory.exe leak    (với ASAN_OPTIONS=detect_leaks=1)
==...==AddressSanitizer: detect_leaks is not supported on this platform.
```

Vì vậy dự án bổ sung một **custom leak tracker** thật (đếm `malloc`/`free` qua `atexit()`), hoạt động đúng trên mọi nền tảng:

```text
$ vulnerable_inventory.exe leak
[CUSTOM-LEAK-TRACKER] 5 allocation(s) leaked (alloc=5, free=0)
Demo Memory Leak (CWE-401):
  (da cap phat 5 HocPhan, KHONG giai phong -> memory leak)

$ secure_inventory.exe leak
[CUSTOM-LEAK-TRACKER] No leaks detected (alloc=6, free=6)
Demo Memory Leak (DA SUA):
  (da cap phat va giai phong day du 5 HocPhan)
```

---

## 2. Giải thích hiện tượng tràn trong struct không bị ASan bắt

### 2.1 Thực nghiệm — tràn ĐỦ LỚN để chạm biên biến struct thì VẪN bị bắt

Ban đầu thử với 39 ký tự (độ dài giống hệt mục 1.1) qua chế độ `safe_input` — vì `sizeof(HocPhan) = 40` byte (nhỏ hơn dự kiến do struct đã được rút gọn đúng phạm vi Lab3), 39 ký tự tràn **vượt qua cả biên của toàn bộ biến `hp` trên stack**, nên **ASan vẫn bắt được** (`stack-buffer-overflow`):

```text
$ vulnerable_inventory.exe safe_input BBB...B (39 ky tu)
==21200==ERROR: AddressSanitizer: stack-buffer-overflow ...
SUMMARY: ... in add_hocphan_malop_UNSAFE
    [32, 72) 'hp' (line 176) <== Memory access at offset 72 overflows this variable
```

Đây là một phát hiện quan trọng: **kích thước tràn phải "vừa đủ"** để ở lại trong biên của biến cấp phát nhưng vượt field đích, thì mới minh họa đúng hiện tượng "không bị bắt". Giảm xuống **30 ký tự** (vẫn tràn `maLop[20]` nhưng không chạm biên ngoài của `hp`):

```text
$ vulnerable_inventory.exe safe_input CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC (30 ky tu)
[CUSTOM-LEAK-TRACKER] No leaks detected (alloc=0, free=0)
Ma lop da luu (struct field, khong ASan-detectable neu chi tran nhe): CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
EXIT=0
```

**Không có bất kỳ cảnh báo ASan nào** — chương trình "chạy xong bình thường".

### 2.2 Bằng chứng thực nghiệm: con trỏ `gv_ptr` bị GHI ĐÈ MỘT PHẦN

Đây là điểm quan trọng nhất: với layout thật `{int id; char maLop[20]; int soTiet; GiangVien *gv_ptr;}`, `maLop` nằm ở offset 4, và tràn 30 ký tự (31 byte kể cả `\0`) ghi tới offset 34 — **chạm vào 3 byte đầu của chính con trỏ `gv_ptr`** (offset 32-39). Đã viết một chương trình xác nhận độc lập, tái hiện đúng layout struct và phép `strcpy` không kiểm tra, in giá trị con trỏ trước/sau:

```text
sizeof(HocPhan) = 40
gv_ptr TRUOC overflow: 0000002E78F2F918
gv_ptr SAU  overflow:  0000002E78004343  <-- da bi ghi de mot phan!
```

3 byte thấp của con trỏ (`F918` → `4343`, trong đó `0x43` = ký tự `'C'` của payload tràn) đã bị ghi đè bởi dữ liệu tấn công. Nếu code sau đó dereference `hp->gv_ptr` (như trong `demo_use_after_free`), nó sẽ truy cập một địa chỉ **đã bị kẻ tấn công thao túng một phần** thay vì địa chỉ hợp lệ ban đầu — hậu quả nghiêm trọng hơn nhiều so với chỉ ghi đè một chuỗi vô hại.

### 2.3 Giải thích kỹ thuật

ASan chèn **redzone** chỉ ở **biên của mỗi khối cấp phát** (`malloc()`/khai báo biến local) — không chèn redzone **giữa các trường của cùng một struct**. Miễn là byte ghi đè cuối cùng còn nằm trong biên ngoài của biến cấp phát (`hp`, tổng 40 byte), ASan không thấy gì bất thường — dù trường `maLop[20]` cụ thể đã bị tràn nghiêm trọng, ghi đè cả `soTiet` và một phần `gv_ptr`.

**Hệ quả sư phạm:** "Chạy không báo lỗi ASan" **không đồng nghĩa với "an toàn"** — lỗi tràn bộ đệm trong `add_hocphan_malop_UNSAFE()` vẫn tồn tại y hệt về bản chất (không kiểm tra độ dài trước `strcpy`) và **y hệt lỗi thật đang tồn tại trong `btl_softsec/ch2_memsafe/lop_hoc_phan.c` dòng 13** (`strcpy(lhp->maLop, maLop)`), chỉ là vị trí bộ nhớ bị ghi đè (field kề bên, thậm chí một phần con trỏ `gv_ptr`) nằm ngoài khả năng quan sát của công cụ khi vẫn ở trong biên biến cấp phát. Đây chính là lý do bản vá `add_hocphan_malop_SAFE()` dùng `snprintf(hp->maLop, MAX_MALOP, ...)` — chặn lỗi **tại nguồn** thay vì trông chờ công cụ phát hiện sau khi lỗi đã xảy ra.

---

## 3. Báo cáo đánh giá rủi ro đầy đủ (5 lỗ hổng, gồm VULN-005 tự thêm)

Lệnh: `python python/risk_assessor.py` (điểm số tính thật qua công thức CVSS-lite trong `python/risk_assessor.py`, không phải số gán tay).

```text
ID        CWE       Ten loi                                    Diem   Muc do
--------------------------------------------------------------------------------
VULN-001  CWE-121   Stack/Heap-based Buffer Overflow           9.8    CRITICAL
VULN-005  CWE-134   Uncontrolled Format String (tu them)       8.1    HIGH
VULN-002  CWE-416   Use After Free                             6.9    MEDIUM
VULN-003  CWE-401   Memory Leak (Missing Release of Memory)    5.4    MEDIUM
VULN-004  CWE-476   NULL Pointer Dereference (rui ro tiem an)  2.5    LOW

Thu tu uu tien khac phuc (theo diem rui ro giam dan):
  1. [CRITICAL] VULN-001 (CWE-121) - Stack/Heap-based Buffer Overflow
  2. [HIGH] VULN-005 (CWE-134) - Uncontrolled Format String (tu them)
  3. [MEDIUM] VULN-002 (CWE-416) - Use After Free
  4. [MEDIUM] VULN-003 (CWE-401) - Memory Leak (Missing Release of Memory)
  5. [LOW] VULN-004 (CWE-476) - NULL Pointer Dereference (rui ro tiem an)
```

### 3.1 VULN-005 tự thêm — CWE-134 Uncontrolled Format String

**Vị trí:** `tra_cuu_hocphan_UNSAFE()` trong `vulnerable_inventory.c` — đưa thẳng từ khóa tìm kiếm mã lớp của người dùng vào `printf(tu_khoa)` thay vì `printf("%s", tu_khoa)`.

**Minh chứng thật (chạy `.\vulnerable_inventory.exe fmt "%x %x %x %x %n"`):**
```text
Demo Format String Bug (CWE-134, VULN-005 tu them):
Ket qua tim kiem ma lop: 0 0 0 80aa0030
```
Chương trình đã **rò rỉ 4 giá trị rác trên stack** ra màn hình (đọc bằng `%x` dù không có tham số tương ứng được truyền) — một ví dụ thật về information disclosure. Bản vá in đúng chuỗi gốc dưới dạng văn bản thuần:
```text
Ket qua tim kiem ma lop: %x %x %x %x %n
```
Clang tự phát hiện lỗi này ngay lúc biên dịch qua `-Wformat-security`:
```text
vulnerable_inventory.c:156:12: warning: format string is not a string literal (potentially insecure) [-Wformat-security]
```

**Giải thích thứ hạng (8.1, HIGH, đứng thứ 2):** Impact sub-score bằng đúng VULN-001/VULN-002 (CIA đều HIGH — `%n` về lý thuyết cho phép ghi bộ nhớ tùy ý). Exploitability sub-score thấp hơn buffer overflow (Attack Complexity = HIGH thay vì LOW) vì khai thác thật (đặc biệt ghi qua `%n`) đòi hỏi kỹ thuật tinh vi hơn. Kết quả: xếp ngay dưới buffer overflow, khớp trực giác.

---

## 4. Log `make test` toàn bộ PASS

```text
$ make clean && make test
C:/msys64/clang64/bin/clang.exe -g -Wall -Wextra -fsanitize=address -o c/vulnerable_inventory.exe c/vulnerable_inventory.c
cp -f ".../libclang_rt.asan_dynamic-x86_64.dll" ".../libc++.dll" c/
C:/msys64/clang64/bin/clang.exe -g -Wall -Wextra -fsanitize=address -o c/secure_inventory.exe c/secure_inventory.c
cp -f ".../libclang_rt.asan_dynamic-x86_64.dll" ".../libc++.dll" c/
python tests/test_memory_safety.py
[PASS] test_vulnerable_overflow_detected
[PASS] test_vulnerable_uaf_detected
[PASS] test_vulnerable_leak_detected
[PASS] test_secure_overflow_clean
[PASS] test_secure_uaf_clean
[PASS] test_secure_leak_clean
[PASS] test_risk_assessment_matches_baseline
[PASS] test_critical_vuln_is_the_buffer_overflow

8/8 test da PASS
```

---

## 5. Kết luận

- Module dùng đúng **kiến trúc struct thật** của DuongUniversity Management System: `MAX_NAME=80`, `MAX_MALOP=20`, và quan trọng nhất — `HocPhan.gv_ptr` là con trỏ `GiangVien*` thật, tái hiện đúng cơ chế liên kết chéo-module gây ra CWE-416/476 trong hệ thống thật, không chỉ đổi tên biến.
- ASan phát hiện đúng **3/3 lỗi trên bản vulnerable** (heap-buffer-overflow, heap-use-after-free qua `gv_ptr`, và memory leak qua custom tracker do LeakSanitizer không hỗ trợ Windows), **0/3 lỗi trên bản secure**.
- `tests/test_memory_safety.py`: **8/8 test PASS**, chạy thật qua `make test`.
- Đánh giá rủi ro đầy đủ 5 lỗ hổng (bao gồm VULN-005 tự thêm), khớp `dataset/expected_risk_baseline.json` trong dung sai 0.05.
- Đã thực nghiệm và **chứng minh bằng số liệu thật** (không chỉ suy luận lý thuyết) rằng tràn bộ đệm trong struct có thể ghi đè một phần con trỏ liên-module `gv_ptr` mà ASan không phát hiện — minh họa trực tiếp mức độ nghiêm trọng của lỗi CWE-120/121 đang tồn tại thật trong `btl_softsec/ch2_memsafe/lop_hoc_phan.c`.
