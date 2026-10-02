# Báo cáo Lab 7 — Phân tích Động: Phủ mã (Code Coverage) & Giám sát Thực thi

**Học phần:** CSE703093 — An toàn phần mềm — Phenikaa University
**Module:** Tính tiền dạy — `calculate_salary()` (**DuongUniversity Management System**, Module 3)

Hàm được đo coverage viết lại từ `calculate_e2e_salary_SAFE()` (`btl_softsec/ch2_memsafe/tinh_tien_day.c`) và bảng hệ số bằng cấp trong `add_lecturer_SAFE()` (`giang_vien.c`), gộp đúng các ràng buộc đã đặc tả trong BTL: CON-12 (`soTiet ≤ 500`), tab:range (`soLuongSinhVien ∈ [0,300]`), CON-13/CWE-1288 (bằng cấp lạ), CON-11 (ngưỡng quy mô 50 SV), CON-5/CWE-197 (audit byte 127), `dinhMucTienChuan = 85000` — thay vì ví dụ "xử lý đơn hàng" chung chung của đề gốc.

Toàn bộ log trong báo cáo này là **log thật**, thu được bằng `gcc/gcov 16.1.0 (MSYS2 UCRT64)` với cờ `--coverage` và `gcov -b`, chạy trực tiếp trên máy — không phải log dựng minh họa.

---

## 1. Cây quyết định của `calculate_salary()` đối chiếu log coverage

### 1.1 Cây quyết định (vẽ tay trước khi chạy công cụ)

```
calculate_salary(soTiet, heSoHocPhan, soLuongSinhVien, bangCap)
│
├─ out==NULL || bangCap==NULL ─────────────── INVALID_DEGREE   (phong thu - KHONG the kich hoat tu CSV)   [dong 68]
├─ soTiet <= 0 || soTiet > 500 ────────────── INVALID_SOTIET                                              [dong 70-71]
├─ heSoHocPhan <= 0 ───────────────────────── INVALID_HESO                                                [dong 73-74]
├─ soLuongSinhVien < 0 || > 300 ───────────── INVALID_SV                                                  [dong 76-77]
├─ bangCap:
│    ├─ "GS"      → heSoBangCap 2.0                                                                        [dong 82-83]
│    ├─ "PGS"     → 1.8                                                                                    [dong 84-85]
│    ├─ "TIEN_SI" → 1.5                                                                                    [dong 86-87]
│    ├─ "THAC_SI" → 1.2                                                                                    [dong 88-89]
│    ├─ "CU_NHAN" → 1.0                                                                                    [dong 90-91]
│    └─ khac      ───────────────────────────── INVALID_DEGREE                                             [dong 93]
├─ soLuongSinhVien > 50 ?                                                                   (CON-11)      [dong 99]
│    ├─ CO : heSoQuyMo = 0.2                                                                               [dong 100]
│    │        └─ soLuongSinhVien > 127 ?                                                    (CON-5)       [dong 101]
│    │             ├─ CO : audit_byte_ok = 0                                                               [dong 102]
│    │             └─ KHONG: audit_byte_ok = 1                                                             [dong 104]
│    └─ KHONG: heSoQuyMo = 0.0, audit_byte_ok = 1                                                          [dong 107-108]
├─ tienDay = soTiet*(heSoHocPhan+heSoQuyMo)*heSoBangCap*85000                                             [dong 112-122]
└─ tienDay > 50 000 000 ?                                                                                  [dong 124]
     ├─ CO : APPROVAL_REQUIRED                                                                             [dong 125]
     └─ KHONG: OK                                                                                          [dong 127]
```

**Số đường thực thi lý thuyết** (chỉ phần nghiệp vụ): 3 đường kết thúc sớm ở validate + 1 đường `INVALID_DEGREE` + (5 bằng cấp hợp lệ) × (3 nhánh quy mô: ≤50 / 51..127 / >127) × (2 nhánh phê duyệt) = **4 + 30 = 34 đường**. Bộ `partial` chỉ đi **1** trong 34 đường đó (TIEN_SI × 51..127 × OK) — hai lần.

### 1.2 Đối chiếu với log gcov của bộ `partial` (2 case)

```text
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=TIEN_SI  expected=OK  actual=OK  quyMo=0.2 audit=1 tien=6885000
[PASS] soTiet=30   heSo=1.0  sv=60   bangCap=TIEN_SI  expected=OK  actual=OK  quyMo=0.2 audit=1 tien=4590000
Tong: 2/2 test PASS

Line coverage  : 72.09% (62/86 dong)
Branch coverage: 44.26% (27/61 nhanh 'taken at least once')
Cac dong CHUA duoc kiem thu:
  Dong 71: return SALARY_INVALID_SOTIET;
  Dong 74: return SALARY_INVALID_HESO;
  Dong 77: return SALARY_INVALID_SV;
  Dong 83: heSoBangCap = 2.0f;
  Dong 85: heSoBangCap = 1.8f;
  Dong 88: } else if (strcmp(bangCap, "THAC_SI") == 0) {
  Dong 89: heSoBangCap = 1.2f;
  Dong 90: } else if (strcmp(bangCap, "CU_NHAN") == 0) {
  Dong 91: heSoBangCap = 1.0f;
  Dong 93: return SALARY_INVALID_DEGREE;
  Dong 102: audit_byte_ok = 0;
  Dong 107: heSoQuyMo = 0.0;
  Dong 108: audit_byte_ok = 1;
  Dong 125: return SALARY_APPROVAL_REQUIRED;
  Dong 133-138: 6 case cua salary_status_to_string() (chi "OK" duoc goi)
  Dong 147-148, 152-153: nhanh loi CLI (argc < 2, fopen that bai)
```

Mọi nhánh trên cây **không có mặt** trong 2 case (3 nhánh validate, 4 bằng cấp khác + bằng cấp lạ, nhánh ≤ 50 SV, nhánh > 127 SV, nhánh phê duyệt) xuất hiện **chính xác** trong danh sách dòng chưa phủ của gcov — cây vẽ tay và log công cụ khớp 1-1. Đáng chú ý: dòng 88 và 90 (chính các lệnh `else if`) cũng chưa được thực thi vì chuỗi `strcmp` đã dừng ở "TIEN_SI".

**Kết luận mấu chốt:** 2/2 PASS = 100% tỷ lệ PASS, nhưng 56% nhánh chưa từng chạy — tỷ lệ PASS **không nói lên điều gì** về việc code đã được kiểm thử tới đâu.

---

## 2. Bảng so sánh coverage của 4 bộ test

Lệnh: `python python/coverage_runner.py` (kết quả lưu `dataset/coverage_comparison_results.json`)

```text
=== BANG SO SANH ===
Bo test                  So case    PASS   Line cov  Branch cov
partial                        2       2     72.09%      44.26%
full                          13      13     94.19%      77.05%
combinatorial                450     450     94.19%      77.05%
combinatorial_extended       630     630     94.19%      77.05%
```

| Bộ test | Số case | Tỷ lệ PASS | Line coverage | Branch coverage | Dòng chưa phủ |
|---|:---:|:---:|:---:|:---:|:---:|
| `partial` (không đầy đủ) | 2 | **100%** | 72.09% (62/86) | 44.26% (27/61) | 24 |
| `full` (đầy đủ, viết tay) | 13 | 100% | **94.19%** (81/86) | **77.05%** (47/61) | 5 |
| `combinatorial` (tự sinh) | 450 | 100% | 94.19% | 77.05% | 5 |
| `combinatorial_extended` (+ biên 50/51) | 630 | 100% | 94.19% | 77.05% | 5 |

**Nhận xét:**
- `full` hơn `partial` **22.1 điểm** line coverage và **32.8 điểm** branch coverage (yêu cầu ≥ 5) — toàn bộ phần tăng là logic nghiệp vụ (validate, 5 bằng cấp, quy mô lớp, audit byte, phê duyệt).
- 13 case viết tay có ý thức về cấu trúc nhánh đạt **cùng coverage** với 450 case tổ hợp: coverage bão hoà ở **94.19% / 77.05%** vì phần còn lại không thể chạm từ CSV (mục 3). Số lượng test không phải thước đo; **thiết kế theo nhánh** mới là thước đo.
- Branch coverage luôn thấp hơn line coverage rõ rệt (77% vs 94%) — gcov đếm *mỗi hướng* của từng điều kiện, kể cả các vế của `||` được short-circuit; đây là chỉ số nghiêm khắc và có ý nghĩa bảo mật hơn line coverage.

Log bộ `full` (13/13):

```text
[PASS] soTiet=0    heSo=1.0  sv=60   bangCap=TIEN_SI  expected=INVALID_SOTIET     actual=INVALID_SOTIET     quyMo=0.0 audit=0 tien=0
[PASS] soTiet=501  heSo=1.0  sv=60   bangCap=TIEN_SI  expected=INVALID_SOTIET     actual=INVALID_SOTIET     quyMo=0.0 audit=0 tien=0
[PASS] soTiet=45   heSo=0.0  sv=60   bangCap=TIEN_SI  expected=INVALID_HESO       actual=INVALID_HESO       quyMo=0.0 audit=0 tien=0
[PASS] soTiet=45   heSo=1.0  sv=-1   bangCap=TIEN_SI  expected=INVALID_SV         actual=INVALID_SV         quyMo=0.0 audit=0 tien=0
[PASS] soTiet=45   heSo=1.0  sv=301  bangCap=TIEN_SI  expected=INVALID_SV         actual=INVALID_SV         quyMo=0.0 audit=0 tien=0
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=KY_SU    expected=INVALID_DEGREE     actual=INVALID_DEGREE     quyMo=0.0 audit=0 tien=0
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=GS       expected=OK                 actual=OK                 quyMo=0.2 audit=1 tien=9180000
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=PGS      expected=OK                 actual=OK                 quyMo=0.2 audit=1 tien=8261999
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=TIEN_SI  expected=OK                 actual=OK                 quyMo=0.2 audit=1 tien=6885000
[PASS] soTiet=45   heSo=1.0  sv=60   bangCap=THAC_SI  expected=OK                 actual=OK                 quyMo=0.2 audit=1 tien=5508000
[PASS] soTiet=45   heSo=1.0  sv=40   bangCap=CU_NHAN  expected=OK                 actual=OK                 quyMo=0.0 audit=1 tien=3825000
[PASS] soTiet=45   heSo=1.0  sv=200  bangCap=TIEN_SI  expected=OK                 actual=OK                 quyMo=0.2 audit=0 tien=6885000
[PASS] soTiet=500  heSo=2.0  sv=100  bangCap=GS       expected=APPROVAL_REQUIRED  actual=APPROVAL_REQUIRED  quyMo=0.2 audit=1 tien=187000000
Tong: 13/13 test PASS
```

> **Quan sát phụ có thật:** `PGS → tien=8261999` thay vì 8 262 000 vì `heSoBangCap` là `float` (1.8f = 1.79999995) rồi ép `(long long)` — **đúng kiểu dữ liệu của `GiangVien.heSoBangCap` thật** trong `giang_vien.h`. Lab giữ nguyên để log trung thực; đây là một finding nhỏ về sai số số học (CWE-681/682) cho BTL: nên dùng `double` hoặc `llround()`. Case `sv=200` cho `audit=0` — xác nhận nhánh CWE-197 (`pack_class_size_byte_SAFE` sẽ từ chối) được phủ.

---

## 3. Vì sao không thể đạt 100% coverage dù đã thử mọi tổ hợp nghiệp vụ hợp lệ

Sau bộ `full`/`combinatorial`, gcov còn **5 dòng** và **14/61 nhánh** chưa phủ. Tất cả đều là **mã không thể chạm từ tầng dữ liệu CSV**, chia 4 nhóm:

| Nhóm | Vị trí (dòng / nhánh) | Vì sao không thể phủ từ CSV | Cách kiểm thử đúng tầng |
|---|---|---|---|
| **A. Guard phòng thủ** | dòng 68: `out == NULL` (nhánh 1), `bangCap == NULL` (nhánh 2) | CLI luôn truyền `&result` và một chuỗi hợp lệ — không có cách nào biểu diễn con trỏ NULL trong CSV | Unit test gọi trực tiếp `calculate_salary(45,1.0,60,NULL,&r)` từ C/ctypes, hoặc kiểm chứng tĩnh (Lab 4 cppcheck) |
| **B. `default` của `switch`** | dòng 138 + nhánh 6 của `salary_status_to_string` | `SalaryStatus` là enum đóng: hàm chỉ nhận giá trị do chính `calculate_salary` trả về, không bao giờ là giá trị lạ | Test "unreachable" bằng cách ép `(SalaryStatus)99` trong unit test; hoặc chấp nhận là defensive code |
| **C. Nhánh lỗi CLI** | dòng 147-148 (`argc < 2`), 152-153 (`fopen` thất bại) | Runner **luôn** truyền đúng 1 đường dẫn file tồn tại; đây là lỗi *vận hành*, không phải lỗi *nghiệp vụ* | Test tích hợp riêng: gọi binary không tham số / với đường dẫn không tồn tại, kiểm tra exit code 1 |
| **D. Nhánh parse CSV & nhánh FAIL** | 6 nhánh `if (line[0]=='\0') continue` / `if (!tok) continue` (dòng 218-252 trong `.gcov`), 3 nhánh "test FAIL" (`if (ok)`, ternary `ok ? "PASS" : "FAIL"`, `return passed == total ? 0 : 2`) | Mọi dòng CSV đều đúng định dạng 5 cột và **mọi test đều PASS** nên hướng "FAIL" không bao giờ được rẽ — nghịch lý: *bộ test càng tốt thì nhánh FAIL càng không được phủ* | Fuzz định dạng CSV (dòng rỗng, thiếu cột) và cố ý đưa 1 case có nhãn sai để kiểm thử chính harness |

Tổng: 2 + 1 + 2 + 9 = **14 nhánh** = 61 − 47 ✓, và 1 + 2 + 2 = **5 dòng** ✓ (nhóm D chỉ mất nhánh, không mất dòng vì các câu lệnh vẫn được thực thi theo hướng còn lại).

**Bài học:** coverage tối đa đạt được từ *một tầng kiểm thử* (dữ liệu nghiệp vụ) có trần cứng; muốn vượt trần phải đổi **tầng** (unit test gọi hàm trực tiếp, test tích hợp CLI, fuzz định dạng — Lab 8), chứ không phải thêm case cùng loại. Đây cũng là lý do nhóm D cho thấy "100% branch coverage" nhiều khi còn đòi hỏi test *cố tình thất bại*.

---

## 4. Lớp tương đương mới (Bước 5): giá trị biên `soLuongSinhVien = 50 / 51`

**Lựa chọn:** ngưỡng quy mô lớp CON-11 trong hệ thống thật là `soLuongSinhVien > 50` (literal cứng trong `calculate_e2e_salary_SAFE`). Tương tự "qty = 9 ngay dưới ngưỡng thành viên" của đề gốc, lớp mới thêm 2 giá trị biên: **50** (đúng tại ngưỡng — *không* được hệ số, vì `>` chứ không phải `>=`) và **51** (ngay trên ngưỡng).

Lệnh: `python python/test_case_generator.py --extended`

```text
Da sinh 630 test case to hop (5 soTiet x 3 heSo x 7 sv x 6 bangCap).
Phan bo nhan ky vong (oracle): {'INVALID_SOTIET': 252, 'INVALID_HESO': 252, 'INVALID_SV': 36, 'OK': 52, 'INVALID_DEGREE': 15, 'APPROVAL_REQUIRED': 23}
```

Log coverage mới (bộ `combinatorial_extended`):

```text
(an 630 dong chi tiet) Tong: 630/630 test PASS
Line coverage  : 94.19% (81/86 dong)
Branch coverage: 77.05% (47/61 nhanh 'taken at least once')
```

Hai case biên đại diện (trích từ output CLI, cùng soTiet=45, heSo=1.0, TIEN_SI):

```text
[PASS] soTiet=45   heSo=1.0  sv=50   bangCap=TIEN_SI  expected=OK  actual=OK  quyMo=0.0 audit=1 tien=5737500
[PASS] soTiet=45   heSo=1.0  sv=51   bangCap=TIEN_SI  expected=OK  actual=OK  quyMo=0.2 audit=1 tien=6885000
```

**Phân tích — vì sao coverage KHÔNG tăng nhưng test vẫn có giá trị:**
- Về mặt **coverage**, `sv = 50` rơi vào nhánh "≤ 50" (đã được `sv = 30` phủ) và `sv = 51` rơi vào nhánh "51..127" (đã được `sv = 60` phủ) — không có dòng/nhánh mới nào được chạm, nên 94.19% / 77.05% giữ nguyên. Đây là bằng chứng thật rằng **coverage không đo được chất lượng dữ liệu test**, chỉ đo "có đi qua hay không".
- Về mặt **phát hiện lỗi**, 2 case này là những case **duy nhất** phân biệt được `> 50` với `>= 50`: nếu lập trình viên viết nhầm `>=`, case `sv = 50` sẽ cho `quyMo=0.2` ≠ oracle (0.0) → FAIL, trong khi toàn bộ 450 case cũ vẫn PASS 100% và coverage vẫn 77.05%. Nói cách khác, một *mutant* off-by-one của CON-11 sống sót qua bộ 450 case nhưng bị giết bởi bộ 630 case — giá trị của test biên nằm ở **mutation score**, không nằm ở coverage.
- Hệ quả tài chính cụ thể: lớp đúng 50 SV với 45 tiết, TIEN_SI chênh **1 147 500 VND** (5 737 500 vs 6 885 000) giữa hai cách hiểu ngưỡng — đúng loại sai lệch mà audit thù lao cần chặn.

Test bổ sung `test_extended_suite_with_boundary_class` kiểm tra tự động: oracle gán `OK` cho cả 2, bộ 630 PASS 100%, coverage ≥ bộ gốc, và output CLI phải chứa `sv=50 ... quyMo=0.0` và `sv=51 ... quyMo=0.2`.

---

## 5. Vì sao oracle phải độc lập với code C

`expected_status()` trong `python/test_case_generator.py` **viết lại đặc tả** (CON-5/11/12/13, tab:range, bảng hệ số, ngưỡng 50 triệu) bằng Python, không gọi và không đọc code C. Nếu dùng chính `calculate_salary()` để sinh nhãn, mọi test sẽ PASS **kể cả khi C sai** (ví dụ `>=` thay vì `>` ở CON-11, hoặc PGS = 1.5 thay vì 1.8) — đó là "kiểm thử chương trình bằng chính nó", tỷ lệ PASS 100% khi ấy vô nghĩa đúng như bộ `partial` ở mục 1. Oracle độc lập biến mỗi test case thành một **phép đối chiếu hai cách hiểu đặc tả** (người viết C và người viết oracle); bất đồng giữa chúng chính là lỗi hoặc lỗ hổng đặc tả. Trong lab này 630/630 đồng thuận — và sự đồng thuận đó có giá trị *vì* hai bên độc lập.

Oracle cố ý dùng số thực Python (`double`) trong khi C dùng `float` cho `heSoHocPhan`/`heSoBangCap`: mọi giá trị trong lớp tương đương đều cách xa ngưỡng 50 triệu nên khác biệt 1 VND (mục 2) không đổi nhãn; nếu một ngày có case nằm sát ngưỡng, chính sự khác biệt này sẽ làm lộ vấn đề kiểu dữ liệu — một lý do nữa để không sao chép cách tính của C vào oracle.

---

## 6. Log `mingw32-make test` (5/5 PASS)

```text
python tests/test_coverage.py
[PASS] test_partial_suite_all_pass
[PASS] test_full_suite_all_pass
[PASS] test_full_suite_covers_significantly_more_than_partial
[PASS] test_combinatorial_suite_all_pass_and_matches_or_exceeds_full_coverage
[PASS] test_extended_suite_with_boundary_class

5/5 test da PASS
```

| Test | Kiểm tra gì |
|---|---|
| `test_partial_suite_all_pass` | 2/2 PASS (điểm xuất phát của nghịch lý "PASS ≠ phủ") |
| `test_full_suite_all_pass` | 13/13 PASS |
| `test_full_suite_covers_significantly_more_than_partial` | line ≥ +5 điểm (thực tế +22.1) và branch tăng |
| `test_combinatorial_suite_all_pass_and_matches_or_exceeds_full_coverage` | sinh lại 450 case, 450/450 PASS, line/branch ≥ `full` |
| `test_extended_suite_with_boundary_class` (bổ sung) | oracle & C đồng thuận tại biên 50/51, 630/630 PASS, coverage ≥ bộ gốc |

---

## 7. Kết luận

- Module dùng đúng đặc tả thật của DuongUniversity (CON-5/11/12/13, tab:range, bảng hệ số bằng cấp, `dinhMucTienChuan = 85000`), hàm `calculate_salary()` có 34 đường thực thi nghiệp vụ.
- Bộ `partial` 2/2 PASS nhưng chỉ phủ 72.09% dòng / 44.26% nhánh; bộ `full` 13 case đạt 94.19% / 77.05% — bằng đúng bộ tổ hợp 450 và 630 case: coverage bão hoà vì 5 dòng / 14 nhánh còn lại thuộc tầng khác (guard NULL, `default`, lỗi CLI, parse CSV, hướng FAIL).
- Lớp biên 50/51 không tăng coverage nhưng là case duy nhất giết được mutant `>=` của CON-11 (chênh 1 147 500 VND/lớp) — coverage đo "đã đi qua", không đo "đã kiểm tra đúng".
- Oracle độc lập là điều kiện để tỷ lệ PASS có nghĩa; `make test` → **5/5 PASS** thật.
