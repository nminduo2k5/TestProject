# BÁO CÁO LAB 8 — KIỂM THỬ MỜ (FUZZING): HỘP ĐEN và HỘP TRẮNG

**Môn:** An toàn phần mềm (CSE703093) — Chương 4 (4.5 Black-box fuzzing, 4.6 White-box fuzzing)
**Chủ đề xuyên suốt:** DuongUniversity Management System — Module 3 "Tịnh tiến dãy"
**Sinh viên:** nminduo2k5 (23010069)

---

## 1. Mục tiêu

- Cài đặt và so sánh hai loại fuzzer trên cùng một chương trình mục tiêu:
  - **Hộp đen (black-box):** đột biến ngẫu nhiên, chỉ quan sát crash / không crash.
  - **Hộp trắng (white-box, coverage-guided):** dùng phản hồi độ phủ mã (`gcov`) để dẫn dắt tìm kiếm, mô phỏng ý tưởng cốt lõi của AFL.
- Đo định lượng với cùng ngân sách số lần thử, giải thích vì sao backdoor ẩn sau "magic string" khó với fuzzing hộp đen.

## 2. Chương trình mục tiêu

File: `c/tinh_tien_day_fuzz.c` — công cụ đọc từng dòng lệnh cấu hình và phân loại:

| Tiền tố | Xử lý | An toàn? |
|---|---|---|
| `GV:<tên>` | `snprintf` vào `maGV[16]` | An toàn |
| `LHP:<mã>` | in mã lớp học phần | An toàn |
| khác | bỏ qua | An toàn |
| **`GVADM:!<payload>`** | `strcpy(maGV, payload)` với `maGV[16]` | **Lỗi** |

**Lỗ hổng:** kênh "ghi đè hệ số lương quản trị" bị bỏ quên trong code production (**CWE-489 – Active Debug Code**). Khi dòng lệnh bắt đầu bằng magic `GVADM:` và ký tự kích hoạt `!`, phần payload được `strcpy` vào bộ đệm cố định 16 byte không kiểm tra độ dài → **CWE-121 (Stack-based Buffer Overflow)** khi `strlen(payload) ≥ 16`.

**Thiết kế để fuzzer "leo" được:** magic `GVADM:!` (7 ký tự) được so khớp **từng ký tự trên từng dòng lệnh riêng** (dòng 48–51), nên mỗi ký tự khớp thêm sẽ mở ra một nhánh coverage mới. Đây là cách AFL + laf-intel xử lý so sánh đa byte.

**Môi trường:** Clang (MSYS2 clang64) với `-fsanitize=address --coverage`; AddressSanitizer dùng để phát hiện tràn bộ đệm, `gcov` để đo độ phủ.

## 3. Kết quả thí nghiệm

### 3.1. Fuzzer hộp đen (Bước 2 + Bước 5) — `logs/blackbox_seed42_1000_3000_5000.log`

Seed = 42, đột biến ngẫu nhiên có từ điển hỗ trợ, không dùng feedback.

| Ngân sách (số lần thử) | Corpus cuối | Số lần chạm nhánh `GVADM:` | **Số crash** |
|---:|---:|---:|---:|
| 1000 | 39 | 124 | **0** |
| 3000 | 131 | 233 | **0** |
| 5000 | 219 | 333 | **0** |

Tổng thời gian chạy: **29 phút 3,7 giây** (≈ 9000 lần thử, ~5 lần thử/giây do mỗi lần là một tiến trình ASan).

### 3.2. Fuzzer hộp trắng (Bước 3) — `logs/whitebox_seed7_500.log`

Seed = 7, ngân sách 501 lần thử, tổng **27 dòng lệnh** được phủ.

**Các sự kiện "coverage mới" (feedback loop dẫn đường):**

| Lần thử | Input (rút gọn) | Dòng mới được phủ | Ý nghĩa |
|---:|---|---|---|
| 1 | `GVADM:GVADM:inchaoCRDLSB` | 42, 43, 48–51, 56, 59, 60, 62, 64, 65, 73, 75, 76, 80–82 | Vào nhánh `GVA…` → `kenh_ghi_de_luong`, qua `D`, `M`, `:` nhưng chưa có `!` |
| 5 | `AAAA…GVADM:xinchao` | 68, 71 | Nhánh "bỏ qua" |
| 27 | `LHP:CNLHP:TT2!24AAAA…` | 69, 70 | Nhánh `LHP:` |
| 42 | `GV:NguynVa3nARMQ…` | 66, 67 | Nhánh `GV:` (an toàn, `snprintf`) |
| 472 | `GVADM:!xi9chao` | 53, 54, 55 | **Khớp đủ magic `GVADM:!`** nhưng payload ngắn (7 ký tự) → chưa tràn |

**Crash tìm được: 2**

| # | Lần thử | Input | Payload | File lưu |
|---|---:|---|---|---|
| 0 | **395** | `GVADM:!xinchao` + 44 ký tự `A` | 51 byte > 15 | `crashes/whitebox_crash_0.txt` |
| 1 | 477 | `GVADM:!xi9LHP:cGVADM:haso` | 18 byte > 15 | `crashes/whitebox_crash_1.txt` |

Thời gian: **2 phút 5,2 giây** (~4 lần thử/giây).

Lưu ý: crash đầu tiên (lần 395) đến *trước* sự kiện "coverage mới" ở lần 472, vì khi đã vượt `!` thì đường đi tới `strcpy` đã có sẵn trong coverage cũ; sự kiện 472 chỉ là lần đầu một input *không* crash vẫn chạm được dòng 53–55. Điều này khớp với thiết kế: crash cần thêm điều kiện độ dài ≥ 16 mà coverage không phản ánh.

### 3.3. Bộ kiểm thử tự động (Bước 6) — `logs/test_fuzzing.log`

```
[PASS] test_normal_inputs_do_not_crash
[PASS] test_known_crash_input_triggers_asan
[PASS] test_whitebox_fuzzer_finds_crash_within_budget
[PASS] test_blackbox_fuzzer_fails_within_same_budget
[PASS] test_saved_crash_files_reproduce
5/5 test PASS  (exit = 0, 6 phút 20 giây)
```

Các test xác nhận: input bình thường không crash; input đã biết gây ASan error; fuzzer hộp trắng tìm được crash trong ngân sách; fuzzer hộp đen thất bại trong cùng ngân sách (seed cố định, tái lập được); các file crash đã lưu tái hiện được lỗi.

## 4. Bảng so sánh công bằng (Bước 4)

Cùng ngân sách ≈ 500–1000 lần thử, seed cố định:

| Tiêu chí | Hộp đen (1000 lần) | Hộp trắng (501 lần) |
|---|---|---|
| Số crash | **0** | **2** |
| Crash đầu tiên | Không có | Lần thử **395** |
| Dùng phản hồi coverage | Không | Có (`gcov`) |
| Cách tiếp cận magic `GVADM:!` | Phải đoán đúng cả chuỗi | Leo dần từng ký tự |
| Thời gian | ~10 phút (ước tính theo tỉ lệ 29 phút / 9000 lần) | 2 phút 5 giây |

Với **một nửa** ngân sách, fuzzer hộp trắng tìm được lỗi còn fuzzer hộp đen không tìm được.

## 5. Nhận xét

1. **Hộp đen mở rộng ngân sách:** ngay cả với 5000 lần thử (gấp 10 lần hộp trắng), vẫn **0 crash** trong lần chạy này. Số lần chạm nhánh `GVADM:` tăng (124 → 333) nhờ từ điển, nhưng chạm `GVADM:` mới chỉ là 6 ký tự; còn phải ghép thêm `!` và payload ≥ 16 byte trong cùng một input mà không có tín hiệu nào báo "đang đi đúng hướng".
   *Ghi chú trung thực:* README dự đoán hộp đen "có thể" tìm ra ở 5000+ lần; thực nghiệm của chúng tôi (seed 42) **chưa** tìm ra. Điều đó không mâu thuẫn — chỉ cho thấy khoảng cách còn lớn hơn dự đoán, và kết quả phụ thuộc seed.
2. **Hộp trắng hiệu quả nhờ feedback:** mỗi ký tự magic khớp thêm cho coverage mới → input được giữ lại làm hạt giống → đột biến tiếp từ nó. Bài toán đoán 7 ký tự một lúc được chia thành chuỗi các bước đoán 1 ký tự.
3. **Chi phí:** mỗi lần thử hộp trắng tốn thêm bước đo `gcov`, nhưng vẫn nhanh hơn rất nhiều so với tổng thời gian hộp đen cần nếu muốn tìm ra lỗi.
4. **Hạn chế của coverage-guided:** độ phủ dòng không phản ánh điều kiện *độ dài* payload (`strlen ≥ 16`) — crash vẫn cần đột biến "may mắn" kéo dài chuỗi. Thực tế dùng thêm ASan, sanitizer và các tín hiệu khác (độ phủ cạnh, so sánh giá trị).
5. **Bài học bảo mật:** kênh debug bị bỏ quên (CWE-489) kết hợp `strcpy` không kiểm tra (CWE-121) là mẫu lỗi thật. Khắc phục: xóa kênh debug khỏi bản production; thay `strcpy` bằng `snprintf`/`strncpy` có giới hạn kích thước; biên dịch với stack protector, ASan trong CI.

## 6. Trả lời câu hỏi mở rộng (magic 10 ký tự, bảng chữ cái 68 ký tự)

Fuzzing hộp đen thuần túy (không từ điển) phải đoán đúng cả chuỗi ngẫu nhiên:

- Xác suất một lần thử khớp: p = (1/68)^10
- Số lần thử trung bình (phân phối hình học): **E = 68^10 ≈ 2,1 × 10^18**

So sánh với magic hiện tại của bài lab (7 ký tự `GVADM:!`): 68^7 ≈ 6,7 × 10^12 — nghĩa là chuỗi 10 ký tự khó hơn **68^3 ≈ 314 000 lần**.

| Tốc độ thực thi | Thời gian trung bình cho 2,1 × 10^18 lần thử |
|---|---|
| ~5 lần/giây (đo thực tế trong lab này) | ≈ 4,2 × 10^17 giây ≈ **13 tỷ năm** |
| 10 000 lần/giây (fuzzer in-process hiệu năng cao) | ≈ 2,1 × 10^14 giây ≈ **6,7 triệu năm** |
| 1 triệu lần/giây (lý tưởng, nhiều lõi) | ≈ 2,1 × 10^12 giây ≈ **67 000 năm** |

Ngân sách khả thi trong CI/CD (vài phút, chừng 10^3–10^6 lần thử tùy tốc độ) chỉ bằng khoảng **10^-12 – 10^-15** lượng cần thiết. Vì vậy fuzzing hộp đen thuần túy **không thể** phát hiện loại backdoor này; cần fuzzing hộp trắng (coverage-guided), từ điển/token trích từ binary, hoặc phân tích tĩnh / thực thi tượng trưng (liên hệ Lab 5–6).

Với fuzzer coverage-guided, chi phí chuyển từ nhân (68^10) sang cộng: tối đa ≈ 10 × 68 ≈ **680 phép đoán** khi từng ký tự đem lại coverage mới.

## 7. Kết luận

- Fuzzer hộp trắng tìm được lỗi tràn bộ đệm CWE-121 sau **395 lần thử (~2 phút)**; fuzzer hộp đen **0 crash** ở cả 1000, 3000 và 5000 lần thử (~29 phút).
- Phản hồi độ phủ mã biến bài toán "đoán cả chuỗi bí mật" thành "đoán từng ký tự", giảm độ phức tạp từ hàm mũ xuống tuyến tính.
- 5/5 test tự động PASS; hai input gây lỗi được lưu trong `crashes/` và tái hiện được.

## 8. Tệp liên quan

| Tệp | Mô tả |
|---|---|
| `c/tinh_tien_day_fuzz.c` | Chương trình mục tiêu (chứa lỗi) |
| `python/blackbox_fuzzer.py`, `python/whitebox_fuzzer.py`, `python/fuzz_common.py` | Hai fuzzer và mã dùng chung |
| `seed_corpus/seed{1,2,3}.txt` | Hạt giống ban đầu |
| `logs/*.log` | Log thí nghiệm (nguồn của báo cáo này) |
| `crashes/whitebox_crash_{0,1}.txt` | Input gây crash |
| `tests/test_fuzzing.py` | Bộ kiểm thử tự động |
