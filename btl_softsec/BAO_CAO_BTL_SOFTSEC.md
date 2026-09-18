# BÀI TẬP LỚN MÔN AN TOÀN PHẦN MỀM (SOFTSEC TOOLKIT)

---

```text
========================================================================================
                                TRƯỜNG ĐẠI HỌC DUONGUNIVERSITY
                                KHOA CÔNG NGHỆ THÔNG TIN
                            BỘ MÔN AN TOÀN VÀ BẢO MẬT THÔNG TIN
                                    -------------------

                                  BÁO CÁO BÀI TẬP LỚN
                        MÔN HỌC: AN TOÀN PHẦN MỀM (SOFTSEC TOOLKIT)

    ĐỀ TÀI:
    PHÂN TÍCH VÀ KIỂM CHỨNG END-TO-END (E2E) AN TOÀN BỘ NHỚ & DỮ LIỆU TÍCH HỢP 
    3 MÔ-ĐUN: QUẢN LÝ GIẢNG VIÊN, QUẢN LÝ LỚP HỌC PHẦN VÀ TÍNH TIỀN DẠY
                (giang_vien.c, lop_hoc_phan.c, tinh_tien_day.c, main.c)
                TRONG HỆ THỐNG DUONGUNIVERSITY MANAGEMENT SYSTEM

    Giảng viên hướng dẫn : Bộ môn An toàn Phần mềm
    Sinh viên thực hiện  : Nguyễn Văn Duong
    Mã số sinh viên (MSSV): 20246001
    Lớp / Khóa           : CNTT K68 - DuongUniversity
    Học kỳ / Năm học     : Học kỳ I - Năm học 2025-2026

========================================================================================
```

---

## MỤC LỤC

1. [PHẦN 1: GIỚI THIỆU VÀ MỤC TIÊU](#1-phần-1-giới-thiệu-và-mục-tiêu)
   - 1.1 [Đặt vấn đề và Lý do chọn đề tài](#11-đặt-vấn-đề-và-lý-do-chọn-đề-tài)
   - 1.2 [Mục tiêu và Điều kiện bắt buộc của BTL (Slide 19)](#12-mục-tiêu-và-điều-kiện-bắt-buộc-của-btl-slide-19)
   - 1.3 [Tư duy cốt lõi: Input vượt phạm vi & 4 lăng kính kiểm chứng](#13-tư-duy-cốt-lõi-input-vượt-phạm-vi--4-lăng-kính-kiểm-chứng)
2. [PHẦN 2: MÔ TẢ HỆ THỐNG VÀ CHƯƠNG TRÌNH MỤC TIÊU 3 MÔ-ĐUN E2E](#2-phần-2-mô-tả-hệ-thống-và-chương-trình-mục-tiêu-3-mô-đun-e2e)
   - 2.1 [Kiến trúc Tổng quan DuongUniversity Management System](#21-kiến-trúc-tổng-quan-duonguniversity-management-system)
   - 2.2 [Liên thông Dữ liệu 3 Mô-đun E2E (Lecturer -> ClassSection -> Salary)](#22-liên-thông-dữ-liệu-3-mô-đun-e2e-lecturer---classsection---salary)
   - 2.3 [Công thức Tính Tiền Dạy Chính Xác (Giữ Nguyên 100%)](#23-công-thức-tính-tiền-dạy-chính-xác-giữ-nguyên-100)
   - 2.4 [Phân tích Bề mặt Tấn công E2E (E2E Attack Surface Analysis)](#24-phân-tích-bề-mặt-tấn-công-e2e-e2e-attack-surface-analysis)
   - 2.5 [Sơ đồ Luồng Dữ liệu E2E 3 Mô-đun (Mermaid DFD)](#25-sơ-đồ-luồng-dữ-liệu-e2e-3-mô-đun-mermaid-dfd)
3. [PHẦN 3: PHƯƠNG PHÁP THỰC HIỆN TỪNG CHƯƠNG](#3-phần-3-phương-pháp-thực-hiện-từng-chương)
   - 3.1 [Chương 1: Mô hình hóa Kripke 5 Trạng thái & Kiểm chứng BMC (`kripke_bmc.py`)](#31-chương-1-mô-hình-hóa-kripke-5-trạng-thái--kiểm-chứng-bmc-kripke_bmcpy)
   - 3.2 [Chương 2: Kiểm tra An toàn Bộ nhớ Liên mô-đun (`pattern_scanner.py` & Mã CWE)](#32-chương-2-kiểm-tra-an-toàn-bộ-nhớ-liên-mô-đun-pattern_scannerpy--mã-cwe)
   - 3.3 [Chương 3: Kiểm chứng Formal SMT Z3 E2E (`smt_verify.py`)](#33-chương-3-kiểm-chứng-formal-smt-z3-e2e-smt_verifypy)
   - 3.4 [Chương 4: Kiểm thử Fuzzing E2E Hộp đen vs Hộp trắng (`fuzzer_blackbox.py` & `fuzzer_whitebox.py`)](#34-chương-4-kiểm-thử-fuzzing-e2e-hộp-đen-vs-hộp-trắng-fuzzer_blackboxpy--fuzzer_whiteboxpy)
4. [PHẦN 4: KẾT QUẢ VÀ PHÂN TÍCH THỰC NGHIỆM CHI TIẾT LOG](#4-phần-4-kết-quả-và-phân-tích-thực-nghiệm-chi-tiết-log)
   - 4.1 [Kết quả Chương 1: BMC Trace & E2E Proof 5 Thuộc tính P1-P5](#41-kết-quả-chương-1-bmc-trace--e2e-proof-5-thuộc-tính-p1-p5)
   - 4.2 [Kết quả Chương 2: Pattern Scanner, Cppcheck & Runtime Binary Log](#42-kết-quả-chương-2-pattern-scanner-cppcheck--runtime-binary-log)
     - 4.2.2 [Bằng chứng động: Memory Trace qua AddressSanitizer thật](#422-bằng-chứng-động-memory-trace-qua-addresssanitizer-thật)
   - 4.3 [Kết quả Chương 3: Chứng minh SMT E2E Ràng buộc An toàn](#43-kết-quả-chương-3-chứng-minh-smt-e2e-ràng-buộc-an-toàn)
   - 4.4 [Kết quả Chương 4: Fuzzing E2E Số liệu Đại diện Nhất quán](#44-kết-quả-chương-4-fuzzing-e2e-số-liệu-đại-diện-nhất-quán)
5. [PHẦN 5: BẢNG TỔNG HỢP VÀ PHÂN TÍCH MÃ CWE LỖI E2E](#5-phần-5-bảng-tổng-hợp-và-phân-tích-mã-cwe-lỗi-e2e)
6. [PHẦN 6: THẢO LUẬN VÀ HẠN CHẾ (DISCUSSION & LIMITATIONS)](#6-phần-6-thảo-luận-và-hạn-chế-discussion--limitations)
7. [PHẦN 7: KẾT LUẬN, TÀI LIỆU THAM KHẢO VÀ PHỤ LỤC](#7-phần-7-kết-luận-tài-liệu-tham-khảo-và-phụ-lục)

---

## 1. PHẦN 1: GIỚI THIỆU VÀ MỤC TIÊU

### 1.1 Đặt vấn đề và Lý do chọn đề tài
Trong các hệ thống phần mềm quản lý đào tạo đại học quy mô lớn, việc kiểm thử từng mô-đun riêng lẻ (Unit Testing) là chưa đủ để đảm bảo an toàn bộ nhớ và toàn vẹn dữ liệu. Khi các mô-đun tương tác liên thông với nhau—chẳng hạn mô-đun **Quản lý Giảng viên** truyền dữ liệu cho **Quản lý Lớp học phần**, và kết quả được truyền tiếp cho mô-đun **Tính tiền dạy & Thanh toán**—những lỗi thao tác ở mô-đun trước (như giải phóng bộ nhớ giảng viên `free(gv)`) có thể lan truyền và gây ra các lỗ hổng an ninh bộ nhớ nghiêm trọng ở mô-đun sau (**Use-After-Free - CWE-416**, **Null Pointer Dereference - CWE-476**, **Integer Overflow - CWE-190**, **Numeric Truncation Error - CWE-197**).

Đề tài Bài tập lớn tập trung xây dựng và thực thi bộ kiểm thử **End-to-End (E2E) Testing** toàn diện trên 3 file module C (`giang_vien.c`, `lop_hoc_phan.c`, `tinh_tien_day.c`, liên kết qua `main.c`) đại diện cho 3 mô-đun chính của hệ thống **DuongUniversity Management System**, áp dụng trọn vẹn 4 chương công cụ của học phần **SoftSec Toolkit**.

### 1.2 Mục tiêu và Điều kiện bắt buộc của BTL (Slide 19)
1. **[1] Mô tả hệ thống E2E 3 mô-đun:** Khai báo cấu trúc dữ liệu `GiangVien`, `LopHocPhan`, `Config` và luồng liên kết dữ liệu qua con trỏ.
2. **[2] Áp dụng đủ 4 chương:**
   - Chương 1: Kripke Structure 5/6 Trạng thái (FIXED/BUGGY) & Kiểm chứng BMC 5 thuộc tính LTL (`ch1_models`).
   - Chương 2: Memory Safety Pattern Scanner & Cppcheck (`ch2_memsafe`).
   - Chương 3: Formal SMT Z3 Solver E2E (`ch3_staticsat`).
   - Chương 4: Black-box Fuzzing vs White-box Z3-Guided Fuzzing E2E (`ch4_dynafuzz`).
3. **[3] Ghi nhận log thực tế 100%:** Trích xuất verbatim toàn bộ kết quả log thực thi từ các file log tự động trong `btl_softsec/logs/`.
4. **[4] Mã nguồn runnable:** Cung cấp đầy đủ file binaries `.exe` và mã nguồn Python tái lập 100%.

---

### 1.3 Tư duy cốt lõi: Input vượt phạm vi & 4 lăng kính kiểm chứng

Toàn bộ đề tài không đặt câu hỏi **"output có đúng không?"** (câu hỏi của test thông thường) mà đặt câu hỏi rộng hơn:

> **"Mô-đun có chịu được khi input vượt ra ngoài vùng an toàn (specification) không?"**

**Vùng input hợp lệ (đặc tả) của hệ thống E2E 3 mô-đun:**

```text
┌─────────────────────────────────────┐   Vùng input HỢP LỆ
│  soTiet     : 1 – 500                │
│  bangCap    : GS/PGS/TIEN_SI/THAC_SI/CU_NHAN │   ← Module PHẢI chịu được
│  hoTen      : ≤ 80 ký tự             │
│  soLuongSinhVien : 0 – 127 (char)    │
│  gv_ptr     : luôn hợp lệ khi đọc    │
└─────────────────────────────────────┘
              ↓ vượt ra ngoài
┌─────────────────────────────────────┐
│  soTiet = 50000            → CWE-190 (tràn số 32-bit)   │
│  bangCap = "HACKER"        → CWE-1288 (logic sai lặng)  │
│  hoTen = 173 ký tự         → CWE-120 (buffer overflow)  │
│  soLuongSinhVien = 256     → CWE-197 (numeric truncation, thậm chí trùng byte với 0)│
│  gv_ptr đã bị free()       → CWE-416 (use-after-free)   │
│  gv_ptr = NULL             → CWE-476 (null deref)       │
└─────────────────────────────────────┘
              ↓ module KHÔNG chịu được → defect phát sinh
```

**4 chương = 4 cách kiểm chứng cùng một câu hỏi, ở 4 tầng khác nhau:**

| Chương | Loại (Static/Dynamic/Formal) | Câu hỏi đặt ra | Cách trả lời |
| :--- | :--- | :--- | :--- |
| **Ch1 — Kripke/BMC** | Formal | "Có tồn tại đường thi hành nào (trong không gian trạng thái) vi phạm thuộc tính an toàn không?" | Xét **toàn bộ** không gian trạng thái cùng lúc bằng Z3, không chạy code. SAT = tìm được đường vi phạm → module không chịu được về **logic điều khiển**. |
| **Ch2 — Pattern Scanner** | Static | "Có chỗ nào trong code khả năng không chịu được input biên không?" | Đọc code, không cần input cụ thể, không cần biên dịch — chỉ cần nhìn cấu trúc (vd `strcpy` không giới hạn ⇒ sẽ gãy khi input > buffer). |
| **Ch3 — Z3 SMT** | Formal | "Có tồn tại bộ giá trị nào **trong toàn miền hợp lệ** khiến module gãy không?" | SAT = có tồn tại → chứng minh không chịu được **về mặt số học**. UNSAT = không tồn tại → chứng minh **an toàn tuyệt đối** với kiểu dữ liệu đó, không phải suy đoán. |
| **Ch4 — Fuzzing** | Dynamic | "Thực sự ném input ra ngoài range, module có gãy không?" | Black-box: ngẫu nhiên/BVA có chủ đích. White-box: Z3 tính chính xác input biên tối thiểu gây gãy. Crash/sai lệch đo được = **bằng chứng thực nghiệm**, không phải suy luận. |

**Điểm then chốt phân biệt Formal (Ch1, Ch3) với Testing thông thường (Ch4 + test truyền thống):**

| | Testing (Ch4 + test truyền thống) | Formal (Ch1, Ch3) |
| :--- | :--- | :--- |
| Cách tiếp cận | Thử N trường hợp cụ thể | Xét toàn bộ không gian giá trị/trạng thái |
| Khi không thấy lỗi | "Chưa thấy lỗi" (confidence tăng dần theo N) | "Chứng minh không có lỗi" (UNSAT = tuyệt đối, không phụ thuộc N) |
| Phụ thuộc | Phụ thuộc bộ input đã chọn để thử | Độc lập với input cụ thể — quantify trên biến ký hiệu |
| Kết luận | Xác suất/thống kê | Tuyệt đối trong phạm vi ràng buộc đã khai báo |

Ví dụ cụ thể ngay trong đề tài: `fuzzer_blackbox.py` chạy 200 lần trên `salary_calc_fixed.exe` cho `0/200` crash — đây là **"chưa thấy lỗi sau 200 lần thử"**. Trong khi đó **Check 2** (`smt_verify.py`) chứng minh **UNSAT** cho tràn số 64-bit trên toàn miền `numClasses∈[1,100], soTiet∈[1,500],...` — đây là **"chứng minh không có lỗi"**, không phụ thuộc việc đã thử bao nhiêu lần. Hai loại bằng chứng này **bổ sung cho nhau**, không thay thế nhau: Formal chứng minh trong phạm vi ràng buộc đã khai báo đúng với thực tế; Dynamic xác nhận điều đó cũng đúng trên chính binary đã biên dịch (bắt được cả lỗi ở tầng biên dịch/runtime mà mô hình hình thức không mô hình hóa, ví dụ CWE-120 buffer overflow thực sự làm crash tiến trình).

---

## 2. PHẦN 2: MÔ TẢ HỆ THỐNG VÀ CHƯƠNG TRÌNH MỤC TIÊU 3 MÔ-ĐUN E2E

### 2.1 Kiến trúc Tổng quan DuongUniversity Management System
Hệ thống **DuongUniversity Management System (TestProject)** gồm:
* **Backend API:** .NET 9.0 Web API (C#) + EF Core 9 + PostgreSQL (Port `5249`).
* **Client Frontend:** React 19 + Vite 6 + Ant Design v5 (Port `5173`).
* **Database rich-data:** 22 Giảng viên, 19 Học phần (nghiêm ngặt 2–3 tín chỉ), 403 Lớp học phần qua 5 học kỳ.

### 2.2 Liên thông Dữ liệu 3 Mô-đun E2E (Lecturer -> ClassSection -> Salary)
1. **Module 1: Quản lý Giảng viên:** Khởi tạo thông tin giảng viên (`id`, `hoTen`, `bangCap`, `heSoBangCap`).
2. **Module 2: Quản lý Lớp học phần:** Khởi tạo lớp học phần (`maLop`, `soTiet`, `heSoHocPhan`, `soLuongSinhVien`) và gán con trỏ giảng viên phụ trách (`gv_ptr`).
3. **Module 3: Tính tiền dạy & Thanh toán:** Đọc thông tin từ cả 2 mô-đun trên để tính toán tổng thù lao và duyệt thanh toán; đồng thời đóng gói bản ghi audit log gọn nhẹ (`pack_class_size_byte_*`) ép `soLuongSinhVien` (int) xuống `char` khi xuất báo cáo.

### 2.3 Công thức Tính Tiền Dạy Chính Xác (Giữ Nguyên 100%)
$$\text{Số tiết quy đổi} = \text{Số tiết} \times (\text{Hệ số học phần} + \text{Hệ số quy mô lớp})$$
$$\text{Thù lao dạy} = \text{Số tiết quy đổi} \times \text{Hệ số bằng cấp} \times \text{Đơn giá tiết chuẩn}$$

---

### 2.4 Phân tích Bề mặt Tấn công E2E (E2E Attack Surface Analysis)

```mermaid
graph TD
    A["[Module 1 Input] User Input (Name / Degree)"] -->|strcpy without bounds| B["CWE-120: Stack/Heap Buffer Overflow (Lecturer Name)"]
    A -->|Unvalidated string| C["CWE-1288: Fallthrough to Default Coefficient (1.0f)"]
    
    D["[Module 1 Admin Operation] delete_lecturer()"] -->|free(gv) without nulling lhp->gv_ptr| E["CWE-416: Use-After-Free Dangling Pointer in Module 2"]
    
    F["[Module 2 Section Creation] Unassigned Section"] -->|lhp->gv_ptr == NULL| G["CWE-476: Null Pointer Dereference in Module 3"]
    
    E --> H["[Module 3 Calculation Engine] calculate_e2e_salary()"]
    G --> H
    B --> H
    
    H -->|int32 32-bit truncation| I["CWE-190: Integer Overflow on Total Semester Salary"]

    J["[Module 2 Input] soLuongSinhVien (int, up to hundreds)"] -->|"(char) cast without range check"| K["CWE-197: Numeric Truncation Error in Audit Log Export"]
    H --> K
```

---

### 2.5 Sơ đồ Luồng Dữ liệu E2E 3 Mô-đun (Mermaid DFD)

```mermaid
flowchart LR
    subgraph Module 1: Lecturer Management
        M1_IN[Lecturer Input Data] --> M1_PROC["add_lecturer() / delete_lecturer()"]
        M1_PROC --> M1_STRUCT[GiangVien Struct Memory]
    end

    subgraph Module 2: Class Section Management
        M2_IN[Class Section Input Params] --> M2_PROC["create_class_section()"]
        M1_STRUCT -.->|Pointer Link: lhp->gv_ptr| M2_PROC
        M2_PROC --> M2_STRUCT[LopHocPhan Struct Memory]
    end

    subgraph Module 3: Salary Calculation & Payment
        M3_CFG[Config Rate & Year] --> M3_PROC["calculate_e2e_salary()"]
        M2_STRUCT --> M3_PROC
        M3_PROC --> M3_OUT["export_report() & Payment Approval"]
    end
```

---

## 3. PHẦN 3: PHƯƠNG PHÁP THỰC HIỆN TỪNG CHƯƠNG

### 3.1 Chương 1: Mô hình hóa Kripke & Kiểm chứng BMC (`kripke_bmc.py`)
Mô hình Kripke $M = (S, S_0, R, L)$: **bản FIXED có 5 trạng thái** (S0-S4) chuyển tiếp chuẩn; **bản BUGGY mở rộng thành 6 trạng thái** (thêm $S_5$ mô phỏng nhánh nhảy cóc bỏ qua bước phân công) — 2 con số khác nhau, không gọi chung là "5 trạng thái" cho cả hai bản như trước để tránh nhầm lẫn:
- $S_0: \text{S0\_INIT}$ (Chưa phân công)
- $S_1: \text{S1\_GV\_ASSIGNED}$ (Đã phân công)
- $S_2: \text{S2\_SALARY\_CALC}$ (Tính tiền)
- $S_3: \text{S3\_EXPORTED}$ (Xuất báo cáo)
- $S_4: \text{S4\_ERROR}$ (Lỗi)
- $S_5: \text{S5\_INVALID\_CALC}$ (chỉ có ở bản BUGGY)

**5 Thuộc tính LTL/CTL Kiểm chứng với BMC ($k=5$):**
1. **$P_1$ (Safety):** $G(\text{calculated} \rightarrow \text{assigned})$ — Chưa phân công $\rightarrow$ không được tính tiền.
2. **$P_2$ (Safety):** $G(\text{exported} \rightarrow \text{calculated})$ — Chưa tính tiền $\rightarrow$ không được xuất báo cáo.
3. **$P_3$ (Liveness):** $G(\text{assigned} \rightarrow F\,\text{calculated})$ — Phân công rồi $\rightarrow$ cuối cùng phải tính tiền.
4. **$P_4$ (Safety):** $G(\text{error} \rightarrow \neg\,\text{exported})$ — Hệ thống lỗi $\rightarrow$ không xuất báo cáo.
5. **$P_5$ (Safety):** $G(\text{exported} \rightarrow \neg\,\text{byte\_truncated})$ — Báo cáo xuất ra không được mang dữ liệu bị ép kiểu `(char)` sai lệch (CWE-197). Nhãn `byte_truncated` chỉ gắn lên $S_3$ ở bản BUGGY (tương ứng `pack_class_size_byte_VULN()` luôn ép kiểu không kiểm tra phạm vi), bản FIXED dùng `pack_class_size_byte_SAFE()` có guard nên không bao giờ mang nhãn này.

**Đối chiếu mô hình với code C thật (traceability):** Mỗi trạng thái được gắn với vị trí thực trong `ch2_memsafe/*.c` bằng comment tường minh trong `kripke_bmc.py` (`S1_GV_ASSIGNED` ↔ sau `add_lecturer_*()`+`create_class_section_*()`, `S2_SALARY_CALC` ↔ sau `calculate_e2e_salary_*()`, `S4_ERROR` ↔ nhánh CWE-416/CWE-476...). Để tránh việc mô hình Kripke chỉ tồn tại độc lập trên giấy mà không có cơ chế nào xác nhận nó khớp với code thật, hàm `cross_validate_with_pattern_scanner()` **gọi lại chính scanner của Chương 2** trên `giang_vien.c`/`tinh_tien_day.c` và khẳng định: trạng thái lỗi `S4_ERROR` tương ứng với đúng 2 lỗ hổng thật đã được quét thấy (`dangling_free` tại `giang_vien.c:32`, `unchecked_nested_deref` tại `tinh_tien_day.c:13`) — nếu code C thay đổi khiến 2 lỗ hổng này không còn bị quét thấy nữa, bước này sẽ tự động in cảnh báo "mô hình Kripke có thể KHÔNG còn khớp với code thật" thay vì im lặng.

---

### 3.2 Chương 2: Kiểm tra An toàn Bộ nhớ Liên mô-đun (`pattern_scanner.py` & Mã CWE)
Sử dụng bộ lọc quét tĩnh phát hiện lỗi liên mô-đun:
1. `strcpy`: Tràn đệm mảng ký tự Giảng viên / Mã lớp (CWE-120).
2. `dangling_free`: Gọi `free(gv)` mà không gán con trỏ liên kết trong lớp học phần về `NULL` (CWE-416).
3. `unchecked_nested_deref`: Đọc con trỏ lồng `lhp->gv_ptr->heSoBangCap` khi chưa kiểm tra `NULL` (CWE-476).
4. `int_overflow_cast`: Ép kiểu `(int)` trong phép nhân thù lao tổng hợp (CWE-190).
5. `unchecked_numeric_truncation`: Ép kiểu `(char)` trên biểu thức số nguyên mà không có `if` kiểm tra phạm vi (`<`/`>`/`<=`/`>=`) trong cùng phạm vi hàm bao quanh trước đó (CWE-197). Bắt đúng `pack_class_size_byte_VULN()` (không guard) và không báo động giả trên `pack_class_size_byte_SAFE()` (có guard `if (soLuongSinhVien < 0 || soLuongSinhVien > 127)` đứng trước).

**Lưu ý về giới hạn công cụ:** Đây là scanner so khớp chuỗi/regex (không phải phân tích AST/data-flow đầy đủ như Clang Static Analyzer). Phạm vi tìm "đã được bảo vệ" (`if`/NULL-check) được scope đúng theo **hàm bao quanh** (`_compute_function_starts()` xác định ranh giới hàm dựa trên quy ước code luôn ở cột 0 và kết thúc bằng `{`) thay vì một cửa sổ N dòng cố định — tránh bỏ sót guard-check nằm xa vị trí truy cập trong hàm dài, đồng thời tránh tràn ngược sang hàm liền trước nếu hàm hiện tại quá ngắn. Đây vẫn là một cải tiến heuristic, không phải phân tích ngữ nghĩa hoàn chỉnh; công cụ này được thiết kế để bổ trợ cho `cppcheck` (một static analyzer thật, xem Bước 3.2 `README_REPRODUCE.md`), không thay thế.

#### 3.2.1 Bổ sung: Memory Usage Trace động qua ASan thật (`memory_trace_demo.py`)

Toàn bộ phần trên của Chương 2 là **phân tích tĩnh** (không biên dịch, không chạy chương trình). Để trả lời câu hỏi "giả định chương trình chạy được, bộ nhớ thực sự được dùng/tái sử dụng/bypass ra sao qua từng bước của một luồng bất kỳ" — vốn là một câu hỏi về **hành vi runtime**, không thể trả lời bằng suy luận tĩnh — đã bổ sung `ch2_memsafe/memory_trace_demo.py`: biên dịch **2 phiên bản nhị phân riêng** cho cùng 1 luồng E2E 7 bước (nhập input → tạo Giảng viên → tạo Lớp học phần → tính lương → ép kiểu byte → xóa Giảng viên → xuất báo cáo):

1. **Bản Plain GCC** (không ASan): chỉ in địa chỉ con trỏ thật (`%p`) tại từng bước, để đối chiếu bằng mắt rằng địa chỉ đọc ở Bước 7 **trùng hệt** địa chỉ vừa `free()` ở Bước 6.
2. **Bản Clang64 + AddressSanitizer** (công cụ độc lập, giống `lab3_secure_memory`): không tự báo cáo gì cả — để chính ASan **tự phát hiện** và dừng chương trình khi xảy ra vi phạm.

Cả 2 bản đều chạy trên cùng cặp driver `main.c` (VULN) và `main_fixed.c` (SAFE), cho ra 4 tổ hợp kết quả — xem log đầy đủ tại [4.2.2](#422-bằng-chứng-động-memory-trace-qua-addresssanitizer-thật).

---

### 3.3 Chương 3: Kiểm chứng Formal SMT Z3 E2E (`smt_verify.py`)
Mô hình hóa ràng buộc Z3 SMT Solver:
- Ràng buộc tổng số tiết quy đổi và tổng thù lao dạy tích lũy trên $N$ lớp học phần.
- Chứng minh **SAT** đối với tràn số 32-bit `int32` và **UNSAT** (An toàn 100%) đối với kiểu số nguyên 64-bit `long long`.
- Kiểm chứng BMC 5 thuộc tính LTL của Chương 1.

**Check 3** (ràng buộc "chưa gán/đã xóa giảng viên → lương = 0") được mã hoá bằng **đúng công thức thật** trong `calculate_e2e_salary_SAFE()` (`tinh_tien_day.c`) qua biểu thức `If(Or(gv_ptr_is_null, is_deleted), 0, soTietQuyDoi*heSoBangCap*dinhMucTienChuan)` — dùng cùng bộ biến `soTiet`/`heSoHocPhan`/`heSoBangCap`/`dinhMucTienChuan` như Check 1/2, thay vì biến Bool/Real trừu tượng tách rời code C như bản trước đó.

**Check 4/5** chứng minh hình thức lỗi CWE-197 (Numeric Truncation Error): ép kiểu `(char)` trên `soLuongSinhVien` được mô hình hóa bằng số học modulo 256 với wrap về miền có dấu `[-128,127]` — đúng cách biểu diễn two's-complement của `signed char`. **Check 4** (mô hình `pack_class_size_byte_VULN()`, không guard) chứng minh **SAT**: tồn tại `soLuongSinhVien` hợp lệ (0..300) khiến giá trị sau ép kiểu khác giá trị gốc. **Check 5** (mô hình `pack_class_size_byte_SAFE()`, có guard `0 <= soLuongSinhVien <= 127`) chứng minh **UNSAT**: khi guard đúng, ép kiểu không bao giờ làm sai lệch giá trị — đây là bằng chứng hình thức (không chỉ test mẫu) rằng bản vá loại trừ hoàn toàn lỗ hổng.

**Check 6 — chứng minh sự tồn tại của trường hợp "trùng lặp byte" (lớp nguy hiểm nhất của CWE-197):** thay vì chỉ hỏi "có sai lệch không", Check 6 hỏi câu hỏi sâu hơn — "có tồn tại 2 giá trị `soLuongSinhVien` khác nhau nhưng cho ra CÙNG 1 byte sau khi ép kiểu không?" bằng ràng buộc $\exists\, a, b \in [0,300], a \neq b : \text{byte}(a) = \text{byte}(b)$. Kết quả **SAT** với phản ví dụ $a=0$ (lớp thật sự rỗng) và $b=256$ (lớp có thật 256 sinh viên) — cả hai xuất ra cùng byte `0`. Đây là bằng chứng hình thức cho luận điểm: lỗi này không chỉ "làm sai số liệu" mà có thể khiến **một lớp học có thật bị hệ thống hiểu nhầm thành một lớp hoàn toàn khác** sau khi dữ liệu đã được xuất ra.

---

### 3.4 Chương 4: Kiểm thử Fuzzing E2E Hộp đen vs Hộp trắng (`fuzzer_blackbox.py` & `fuzzer_whitebox.py`)
* **Black-box Fuzzing (`fuzzer_blackbox.py`):** Lấy 1 lần chạy đại diện tiêu chuẩn **200 runs** trên `salary_calc.exe` và `salary_calc_fixed.exe` — gồm 2 kịch bản: fuzzing qua `stdin` (tên/bằng cấp/mã lớp, tìm crash CWE-120) và fuzzing qua subcommand `e2e_byte_truncate <soLuongSinhVien>` (tìm sai lệch dữ liệu CWE-197, không phải crash).
* **White-box Fuzzing Z3-Guided (`fuzzer_whitebox.py`):** Giải trực tiếp 7 mục tiêu ràng buộc điều kiện lỗi E2E bằng Z3 Solver (Target 6 và 7 cùng minh hoạ CWE-197 ở 2 khía cạnh khác nhau — xem bên dưới).

**Phạm vi & giới hạn thuật ngữ "White-box":** Đây KHÔNG phải symbolic execution duyệt qua CFG của source/binary (kiểu KLEE/angr) — 7 "target" là 7 ràng buộc Z3 viết tay ứng với 6 CWE đã biết trước trong `ch2_memsafe`, nên việc "phát hiện 7/7 trong 7 lần thử" mang tính minh hoạ hơn là một quy trình khám phá tự động không biết trước mục tiêu. Điểm "white-box" thật sự nằm ở chỗ: hằng số `MAX_NAME`/`MAX_MALOP` được **đọc trực tiếp từ header `.h`** (`read_header_define()`) thay vì hard-code, nên ràng buộc Z3 tự động bám theo đúng source hiện tại nếu hằng số đổi.

**Boundary Value Analysis (BVA) có chủ đích thay cho ngẫu nhiên thuần túy:** `fuzzer_blackbox.py` bổ sung `run_bva_truncation_test()` chạy đúng **17 giá trị biên cố định** (thiết kế theo phân tích lớp tương đương ở mục 6, không phải `random`) trên cả 2 bản: quanh mép miền `signed char` (`-129/-128/-127`, `126/127/128/129`), quanh các mốc chu kỳ 256 (`-256/-255`, `255/256/257`), và vài giá trị "lớp đại cương" thực tế (`300`, `384`). Với mỗi giá trị, script đọc byte **thật** do chương trình in ra, đối chiếu với byte tính tay bằng công thức modulo-256, rồi **gom nhóm theo byte kết quả** để tự động lộ ra các bộ giá trị trùng lặp — thay vì chỉ liệt kê từng lần thử rời rạc như fuzzing ngẫu nhiên.

---

## 4. PHẦN 4: KẾT QUẢ VÀ PHÂN TÍCH THỰC NGHIỆM CHI TIẾT LOG

### 4.1 Kết quả Chương 1: BMC Trace & E2E Proof 5 Thuộc tính P1-P5
Lệnh thực thi: `python ch1_models/kripke_bmc.py`  
File log ghi nhận: [`logs/kripke_bmc.log`](file:///k:/TestProject/btl_softsec/logs/kripke_bmc.log)

**Bảng Đối chiếu Kết quả BMC 5 Thuộc tính P1-P5:**

| Thuộc tính LTL | Ý nghĩa an toàn / Liveness | Kết quả bản BUGGY | Kết quả bản FIXED | Giải thích bản chất BMC ($k=5$) |
| :--- | :--- | :---: | :---: | :--- |
| **$P_1$ (Safety)** | $G(\text{calculated} \rightarrow \text{assigned})$ | **SAT** *(Vi phạm)* | **UNSAT** *(An toàn)* | Bản BUGGY nhảy cóc từ $S_0$ sang $S_5$ tính tiền khi chưa phân công $S_1$. Bản FIXED ngăn chặn tuyệt đối. |
| **$P_2$ (Safety)** | $G(\text{exported} \rightarrow \text{calculated})$ | **UNSAT** *(An toàn)* | **UNSAT** *(An toàn)* | Cả 2 bản đều tuân thủ: Không bao giờ xuất báo cáo $S_3$ khi chưa trải qua bước tính tiền $S_2$. |
| **$P_3$ (Liveness)** | $G(\text{assigned} \rightarrow F\,\text{calculated})$ | **SAT** *(Vi phạm)* | **SAT** *(Hạn chế BMC)* | Trong độ sâu $k=5$, tiến trình rẽ nhánh sang $S_4$ (lỗi hệ thống/hủy) ngắt luồng trước $S_2$. Đây là hạn chế kỹ thuật của BMC với Liveness hữu hạn (cần $k$-induction), không phải lỗi mã nguồn SAFE. |
| **$P_4$ (Safety)** | $G(\text{error} \rightarrow \neg\,\text{exported})$ | **UNSAT** *(An toàn)* | **UNSAT** *(An toàn)* | Hệ thống ở trạng thái lỗi $S_4$ không bao giờ chuyển tiếp tới xuất báo cáo $S_3$. |
| **$P_5$ (Safety)** | $G(\text{exported} \rightarrow \neg\,\text{byte\_truncated})$ | **SAT** *(Vi phạm — CWE-197)* | **UNSAT** *(An toàn)* | Bản BUGGY: $S_3$ mang cả nhãn `exported` và `byte_truncated` (do `pack_class_size_byte_VULN()` luôn ép kiểu không kiểm tra) → vi phạm. Bản FIXED dùng `pack_class_size_byte_SAFE()` có guard nên $S_3$ không bao giờ mang `byte_truncated`. |

*Log thực thi Verbatim (`logs/kripke_bmc.log`):*
```text
=========================================================
  CHUONG 1: MO HINH HOA KRIPKE & BMC (k=5)
  Ban FIXED: 5 trang thai (S0-S4) | Ban BUGGY: 6 trang thai (S0-S5)
=========================================================

=======================================================
  RUNNING BMC CHECK ON: DuongUniversity_Kripke_BUGGY (6 trang thai, k=5)
=======================================================

[Property 1] Safety: G(calculated -> assigned) [Chưa phân công -> Không tính tiền]
  --> RESULT: SAT (Counterexample Trace Found!)
  Counterexample Trace:
    Step 0: S0_INIT [Labels: ['init']]
    Step 1: S5_INVALID_CALC [Labels: ['calculated', 'error']]
    Step 2: S4_ERROR [Labels: ['error']]
    Step 3: S0_INIT [Labels: ['init']]
    Step 4: S5_INVALID_CALC [Labels: ['calculated', 'error']]
    Step 5: S4_ERROR [Labels: ['error']]

[Property 2] Safety: G(exported -> calculated) [Chưa tính tiền -> Không xuất báo cáo]
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 3] Liveness: G(assigned -> F calculated) [Phân công -> Cuối cùng tính tiền]
  --> RESULT: SAT (Counterexample Trace Found!)

[Property 4] Safety: G(error -> NOT exported) [Hệ thống Lỗi -> Không xuất báo cáo]
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 5] Safety: G(exported -> NOT byte_truncated) [Báo cáo xuất ra không được sai lệch do ép kiểu (char)]
  --> RESULT: SAT (Counterexample Trace Found! CWE-197 co the ro ri ra bao cao xuat)
    Step 0: S0_INIT [Labels: ['init']]
    Step 1: S1_GV_ASSIGNED [Labels: ['assigned']]
    Step 2: S2_SALARY_CALC [Labels: ['assigned', 'calculated']]
    Step 3: S3_EXPORTED [Labels: ['assigned', 'byte_truncated', 'calculated', 'exported']]
    Step 4: S0_INIT [Labels: ['init']]
    Step 5: S5_INVALID_CALC [Labels: ['calculated', 'error']]

=======================================================
  RUNNING BMC CHECK ON: DuongUniversity_Kripke_FIXED (5 trang thai, k=5)
=======================================================

[Property 1] Safety: G(calculated -> assigned) [Chưa phân công -> Không tính tiền]
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 2] Safety: G(exported -> calculated) [Chưa tính tiền -> Không xuất báo cáo]
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 3] Liveness: G(assigned -> F calculated) [Phân công -> Cuối cùng tính tiền]
  --> RESULT: SAT (Counterexample Trace Found!)

[Property 4] Safety: G(error -> NOT exported) [Hệ thống Lỗi -> Không xuất báo cáo]
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 5] Safety: G(exported -> NOT byte_truncated) [Báo cáo xuất ra không được sai lệch do ép kiểu (char)]
  --> RESULT: UNSAT (Property Holds up to k=5)

=======================================================
  DOI CHIEU MO HINH KRIPKE VOI KET QUA QUET TINH CHUONG 2 (Traceability Check)
=======================================================
  [OK] S4_ERROR <-> ch2_memsafe/giang_vien.c:32 [dangling_free] (xac nhan boi pattern_scanner.py)
  [OK] S4_ERROR <-> ch2_memsafe/tinh_tien_day.c:13 [unchecked_nested_deref] (xac nhan boi pattern_scanner.py)
  [OK] S3_EXPORTED_TRUNCATED <-> ch2_memsafe/tinh_tien_day.c:63 [unchecked_numeric_truncation] (xac nhan boi pattern_scanner.py)
  --> KET LUAN: Cac trang thai loi (S4_ERROR, S3_EXPORTED_TRUNCATED) trong mo hinh
      Kripke deu duoc xac nhan boi it nhat 1 lo hong THAT (CWE-416/CWE-476/CWE-197)
      do Chuong 2 quet duoc tren code C hien tai.
```

> **Ghi chú kỹ thuật:** Bước "Traceability Check" ở cuối log là cơ chế mới — `kripke_bmc.py` gọi lại `pattern_scanner.py` (Chương 2) để tự động xác nhận trạng thái lỗi trừu tượng `S4_ERROR` khớp với lỗ hổng thật trên code C hiện tại, thay vì mô hình Kripke tồn tại độc lập không có gì đối chứng. Đã kiểm thử: nếu vá lỗi CWE-476 tại `tinh_tien_day.c` (thêm `if (!lhp->gv_ptr) return 0;`) mà không cập nhật mô hình, bước này in ra `[CANH BAO] ... mo hinh Kripke co the KHONG con khop voi code that!` — xác nhận đây là kiểm tra thật, không phải rubber-stamp.

---

### 4.2 Kết quả Chương 2: Pattern Scanner, Cppcheck & Runtime Binary Log

#### 4.2.1 Output Mô-đun `pattern_scanner.py`
Lệnh thực thi: `python ch2_memsafe/pattern_scanner.py`  
File log ghi nhận: [`logs/pattern_scanner.log`](file:///k:/TestProject/btl_softsec/logs/pattern_scanner.log)

```text
=================================================================
  CHUONG 2: MO-DUN CH2_MEMSAFE PATTERN SCANNER TINH E2E
=================================================================

== Quét tệp: giang_vien.c ==
giang_vien.c:12: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf (CWE-120)
    strcpy(gv->maGiangVien, maGV);
giang_vien.c:15: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf (CWE-120)
    strcpy(gv->hoTen, hoTen);
giang_vien.c:18: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf (CWE-120)
    strcpy(gv->bangCap, bangCap);
giang_vien.c:32: cảnh báo [dangling_free] Giải phóng free() bộ nhớ mà không gán NULL hoặc hủy liên kết con trỏ treo (CWE-416 UAF)
    free(gv); // LOI CWE-416: free(gv) nhung khong cap nhat con tro o Module 2 thanh NULL!

== Quét tệp: lop_hoc_phan.c ==
lop_hoc_phan.c:13: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf (CWE-120)
    strcpy(lhp->maLop, maLop);

== Quét tệp: tinh_tien_day.c ==
tinh_tien_day.c:12: cảnh báo [int_overflow_cast] Ép kiểu (int) trong phép nhân có nguy cơ Tràn số nguyên 32-bit (CWE-190)
    int soTietQuyDoi = (int)(lhp->soTiet * (lhp->heSoHocPhan + heSoQuyMo));
tinh_tien_day.c:13: cảnh báo [int_overflow_cast] Ép kiểu (int) trong phép nhân có nguy cơ Tràn số nguyên 32-bit (CWE-190)
    int tienDay32 = (int)soTietQuyDoi * (int)lhp->gv_ptr->heSoBangCap * (int)cfg->dinhMucTienChuan;
tinh_tien_day.c:13: cảnh báo [unchecked_nested_deref] Truy cập con trỏ lồng (gv_ptr->) mà không kiểm tra NULL trước (CWE-476 Null Pointer Dereference)
    int tienDay32 = (int)soTietQuyDoi * (int)lhp->gv_ptr->heSoBangCap * (int)cfg->dinhMucTienChuan;
tinh_tien_day.c:63: cảnh báo [unchecked_numeric_truncation] Ép kiểu (char) không kiểm tra phạm vi trước - giá trị int ngoài [-128,127] sẽ bị wrap-around sai lệch (CWE-197 Numeric Truncation Error)
    return (char)soLuongSinhVien;

== Quét tệp: main_fixed.c ==
  --> [CLEAN] Không phát hiện vi phạm quy tắc an toàn bộ nhớ nào.
```

> **Ghi chú kỹ thuật:** Log trên là log đã được sửa lỗi. Bản `pattern_scanner.py` trước đó có lỗi bỏ sót (false negative): heuristic "đã được bảo vệ" của `dangling_free`/`unchecked_nested_deref` so khớp chuỗi con (`NULL`, `gv_ptr ==`, `if (!`) ngay trên cả phần **comment** giải thích lỗi, khiến 2 dòng lỗi thật ở `giang_vien.c:32` và `tinh_tien_day.c:13` bị bỏ qua hoàn toàn (không hề xuất hiện trong log cũ). Đã vá bằng cách thêm hàm `_code_part()` loại bỏ phần sau `//` trước khi so khớp — xem [3.2](#32-chương-2-kiểm-tra-an-toàn-bộ-nhớ-liên-mô-đun-pattern_scannerpy--mã-cwe) và [PHẦN 6, mục 2](#6-phần-6-thảo-luận-và-hạn-chế-discussion--limitations).
>
> **Lỗ hổng thứ 6 (CWE-197)** đã được thêm vào cả 4 chương: `tinh_tien_day.c:63` (`pack_class_size_byte_VULN`) bị quét đúng vì không có `if` guard nào đứng trước trong phạm vi hàm; `pack_class_size_byte_SAFE()` (cùng file, dòng ~74) **không** bị báo động giả vì scanner tìm thấy guard `if (soLuongSinhVien < 0 || soLuongSinhVien > 127)` trong phạm vi hàm bao quanh trước dòng ép kiểu — xác nhận cơ chế function-scope hoạt động đúng trên rule mới, không chỉ trên 2 rule cũ.

---

#### 4.2.2 Bằng chứng động: Memory Trace qua AddressSanitizer thật
Lệnh thực thi: `python ch2_memsafe/memory_trace_demo.py`
File log ghi nhận: [`logs/memory_trace.log`](file:///k:/TestProject/btl_softsec/logs/memory_trace.log)

**Bản Plain GCC (không ASan) — VULN: chạy hết, KHÔNG crash, dù đã đọc vùng nhớ đã free (im lặng, nguy hiểm nhất):**
```text
[BUOC 1] Nhap input vao buffer STACK   : dia chi=00000050CA7FF970  noi dung="Pham Van Duong"
[BUOC 2] malloc() GiangVien tren HEAP   : dia chi=00000152F87CE160  (gv->hoTen tai 00000152F87CE178)
[BUOC 3] malloc() LopHocPhan tren HEAP  : dia chi=00000152F87C4C80  (lhp->gv_ptr = 00000152F87CE160  <-- TRUNG voi Buoc 2!)
[BUOC 4] Tinh luong (doc lai gv_ptr)    : ket qua=4590000 (doc qua con tro tai dia chi 00000152F87CE160)
[BUOC 5] Ep kieu (char) so luong SV     : int=60 -> byte=60 (dia chi bien cuc bo=00000050CA7FFA3F)
[BUOC 6] free(gv) - TRA vung nho ve allocator: dia chi vua free=00000152F87CE160 (lhp->gv_ptr VAN CON tro toi day!)
[BUOC 7] export_report doc lai gv_ptr->hoTen SAU KHI FREE - dia chi doc=00000152F87CE160 (== dia chi da free o Buoc 6!)
[KET LUAN] Buoc 7 vua doc THANH CONG mot vung nho DA BI FREE o Buoc 6 - day chinh la CWE-416
           Use-After-Free, chung minh bang DIA CHI THAT (00000152F87CE160 == 00000152F87CE160), khong phai suy luan.

--> Exit code: 0 (0 = chay het, KHONG crash, du da doc vung nho da free!)
```

**Bản Clang64 + AddressSanitizer — VULN: công cụ độc lập THẬT SỰ chặn chương trình lại tại đúng Bước 7:**
```text
[BUOC 6] free(gv) - TRA vung nho ve allocator: dia chi vua free=000012EF7E8A0040 (lhp->gv_ptr VAN CON tro toi day!)
[BUOC 7] export_report doc lai gv_ptr->hoTen SAU KHI FREE - dia chi doc=000012EF7E8A0040 (== dia chi da free o Buoc 6!)

==20948==ERROR: AddressSanitizer: heap-use-after-free on address 0x12ef7e8a0058 at pc 0x7ffa980225df bp 0x00fece78e430 sp 0x00fece78e478
READ of size 15 at 0x12ef7e8a0058 thread T0
    #0 0x7ffa980225de in _asan_wrap_strnlen+0x24e (...libclang_rt.asan_dynamic-x86_64.dll+0x1800425de)
    #7 0x7ff619f25cce  (...trace_asan_vuln.exe+0x140005cce)

0x12ef7e8a0058 is located 24 bytes inside of 132-byte region [0x12ef7e8a0040,0x12ef7e8a00c4)
freed by thread T0 here:
    #1 0x7ff619f218d9  (...trace_asan_vuln.exe+0x1400018d9)
previously allocated by thread T0 here:
    #1 0x7ff619f214a1  (...trace_asan_vuln.exe+0x1400014a1)

SUMMARY: AddressSanitizer: heap-use-after-free (...ucrtbase.dll+0x1800241fe) in isleadbyte_l+0x1ce
==20948==ABORTING

--> Exit code: 1 (khac 0 = ASan da CHAN chuong trinh vi phat hien heap-use-after-free THAT)
```
*(log đầy đủ — bao gồm toàn bộ 3 call stack và shadow-byte map — nằm nguyên vẹn trong `logs/memory_trace.log`, ở đây trích các dòng cốt lõi để dễ đọc.)*

**Bản Clang64 + AddressSanitizer — FIXED: chạy sạch, ASan xác nhận không có vi phạm:**
```text
[BUOC 6-SAFE] Huy lien ket lhp->gv_ptr=NULL TRUOC khi free(gv=0000119A1CCA0040) - khac VULN o day!
[BUOC 7-SAFE] export_report kiem tra lhp->gv_ptr=0000000000000000 (NULL) TRUOC khi doc - khong doc vung nho da free
[KET LUAN] Buoc 7 KHONG doc vung nho da free (lhp->gv_ptr da la NULL tu Buoc 6) - CWE-416 da bi CHAN.

--> Exit code: 0 (0 = ASan xac nhan KHONG co loi memory-safety nao tren ban da vá)
```

> **Ghi chú kỹ thuật — vì sao cần cả 2 bản (Plain + ASan) chứ không chỉ 1:** Bản Plain GCC chứng minh điều đáng sợ nhất của UAF — **nó không hề crash**, `exit code = 0`, tiến trình đọc dữ liệu "rác" (thực chất trùng địa chỉ vừa free) mà không có tín hiệu bất thường nào; đây chính là lý do CWE-416 nguy hiểm trong production (silent corruption). Bản ASan chứng minh điều ngược lại: một công cụ **độc lập với chính chương trình** (không phải `printf` tự báo cáo) xác nhận đây thực sự là vi phạm bộ nhớ, không phải diễn giải chủ quan. Kết hợp cả 2 mới trả lời trọn vẹn câu hỏi "giả định chương trình chạy được — bộ nhớ dùng ra sao": **có, chạy được, và đó chính là vấn đề — nó chạy được đến mức không ai nhận ra dữ liệu đã bị hỏng.**

---

### 4.3 Kết quả Chương 3: Chứng minh SMT E2E Ràng buộc An toàn
Lệnh thực thi: `python ch3_staticsat/smt_verify.py`  
File log ghi nhận: [`logs/smt_verify.log`](file:///k:/TestProject/btl_softsec/logs/smt_verify.log)

```text
=================================================================
  CHUONG 3: KIEM CHUNG FORMAL E2E 3-MODULE VOI Z3 SMT SOLVER
=================================================================

[Check 1] E2E 32-bit Integer Overflow Test across Multi-Class Salary Aggregation:
  --> RESULT: SAT (32-bit Integer Overflow IS POSSIBLE when aggregating multi-class salary!)
  Counterexample values:
    - numClasses        = 20
    - soTiet            = 120
    - heSoHocPhan       = 1572863/524288
    - heSoQuyMoLop      = 524287/1048576
    - heSoBangCap       = 262143/131072
    - dinhMucTienChuan  = 127827 VND
  --> DE XUAT: Dung long long (int64) va double trong C de dam bao an toan tuyet doi.

[Check 2] E2E 64-bit Integer Overflow Verification (long long / int64):
  --> RESULT: UNSAT (64-bit long long is PROVEN SAFE within all enterprise bounds).
    Limit INT64_MAX = 9,223,372,036,854,775,807 VND
  --> KET LUAN: Code C sau khi fix sang 64-bit (long long/double) phat huy an toan tuyet doi.

[Check 3] E2E Unassigned/Deleted Lecturer Safety Constraint (Mod 1 -> Mod 2 -> Mod 3):
  --> RESULT: UNSAT (Safe code strictly enforces: NO/DELETED LECTURER -> SALARY = 0 VND,
      da kiem chung tren chinh cong thuc tinh luong that dung trong Module 3).

[Check 4] E2E Numeric Truncation Error int -> char tren So Luong Sinh Vien (CWE-197):
  --> RESULT: SAT (Numeric truncation CO THE xay ra - ep (char) khong kiem tra pham vi!)
    - soLuongSinhVien (int)      = 128
    - Byte da ep kieu (char)     = -128  <- SAI LECH so voi gia tri that
  --> DE XUAT: Kiem tra pham vi (0..127) TRUOC khi ep kieu (char), giong pack_class_size_byte_SAFE().

[Check 5] E2E Numeric Truncation SAU KHI FIX (guard 0..127 truoc khi ep kieu, CWE-197):
  --> RESULT: UNSAT (Da chung minh: voi guard 0..127 dung TRUOC khi ep kieu, gia tri
      sau ep kieu LUON BANG gia tri int goc - khong bao gio xay ra Numeric Truncation).

[Check 6] E2E Numeric Truncation COLLISION - 2 gia tri KHAC NHAU cung cho 1 byte (CWE-197):
  --> RESULT: SAT (Ton tai 2 lop hoc phan HOAN TOAN KHAC NHAU nhung xuat ra CUNG 1 byte!)
    - Lop A: soLuongSinhVien = 0  (lop that su rong)
    - Lop B: soLuongSinhVien = 256  (lop CO THAT 256 sinh vien)
    - Ca 2 deu xuat ra byte = 0  <- KHONG THE PHAN BIET duoc sau khi ep kieu!
  --> DE XUAT: Day chinh la ly do phai chan TRUOC khi ep kieu (pack_class_size_byte_SAFE), khong
      the chi dua vao gia tri byte da xuat de suy nguoc lai so sinh vien that.
```

> **Ghi chú kỹ thuật:** Check 3 đã được viết lại để dùng **đúng công thức thật** (`soTiet`, `heSoHocPhan`, `heSoBangCap`, `dinhMucTienChuan` — cùng bộ biến với Check 1/2) thay vì biến Bool/Real trừu tượng tách rời code C như bản trước — xem [3.3](#33-chương-3-kiểm-chứng-formal-smt-z3-e2e-smt_verifypy). Check 4/5 (CWE-197) là ví dụ hiếm về việc chứng minh **cả 2 chiều**: SAT trên mô hình VULN (phản ví dụ `soLuongSinhVien=128 -> byte=-128`, đúng ranh giới two's-complement của `signed char`) và UNSAT trên mô hình SAFE với guard — tức bản vá được chứng minh hình thức loại trừ lỗi hoàn toàn, không chỉ vá theo từng test mẫu. Check 6 đào sâu thêm một bước: không chỉ chứng minh "có sai lệch", mà chứng minh **tồn tại 2 tình huống nghiệp vụ khác nhau bị nhầm lẫn thành một** — đây là dạng thuộc tính mà chỉ SMT solver mới chứng minh được thuận tiện (quantify trên toàn miền $[0,300]^2$), test mẫu hay fuzzing ngẫu nhiên khó lòng tự phát hiện ra cặp giá trị cụ thể này.

---

### 4.4 Kết quả Chương 4: Fuzzing E2E Số liệu Đại diện Nhất quán

> [!IMPORTANT]
> **Ghi chú về Số liệu Fuzzing Đại diện:**
> Để tránh sai lệch dao động do môi trường ngẫu nhiên giữa các lần chạy, báo cáo chọn **1 lần chạy thực nghiệm đại diện tiêu chuẩn (200 runs)** làm số liệu chính thức cho toàn bộ bảng biểu và báo cáo. Log thực thi đầy đủ 100% được lưu trữ tại `logs/fuzzer_blackbox.log` và `logs/fuzzer_whitebox.log`.

#### 4.4.1 Black-box Fuzzing Log Đại diện (`fuzzer_blackbox.py`)
Lệnh thực thi: `python ch4_dynafuzz/fuzzer_blackbox.py`  
File log ghi nhận: [`logs/fuzzer_blackbox.log`](file:///k:/TestProject/btl_softsec/logs/fuzzer_blackbox.log)

```text
=================================================================
  CHUONG 4: BLACK-BOX FUZZING E2E 3-MODULE SYSTEM
=================================================================

=================================================================
  BLACK-BOX FUZZING TREN salary_calc.exe (200 runs)
=================================================================
--> Target Binary Executable: K:\TestProject\btl_softsec\ch2_memsafe\salary_calc.exe

--> KẾT QUẢ BLACK-BOX FUZZING TREN salary_calc.exe:
    - Tổng số lần thử (Attempts):   200
    - Số lần Crash (Buffer Overflow): 72 (36.0%)
    - Số lần Logic Error (Bằng cấp):  75 (37.5%)
    - Thời gian thực thi:            11.90 giây
    - Tốc độ fuzzing:                 16.8 execs/sec
--> MẪU TESTCASE GÂY CRASH PHÁT HIỆN:
    Sample #1: Attempt #1 | TenLen=144 | LopLen=5 | BangCap='INVALID_DEGREE' | Reason: ExitCode=3221226356
    Sample #2: Attempt #3 | TenLen=178 | LopLen=36 | BangCap='THAC_SI' | Reason: ExitCode=3221226356
    Sample #3: Attempt #4 | TenLen=132 | LopLen=33 | BangCap='CU_NHAN' | Reason: ExitCode=3221226356

=================================================================
  BLACK-BOX FUZZING TREN salary_calc_fixed.exe (200 runs)
=================================================================
--> Target Binary Executable: K:\TestProject\btl_softsec\ch2_memsafe\salary_calc_fixed.exe

--> KẾT QUẢ BLACK-BOX FUZZING TREN salary_calc_fixed.exe:
    - Tổng số lần thử (Attempts):   200
    - Số lần Crash (Buffer Overflow): 0 (0.0%)
    - Số lần Logic Error (Bằng cấp):  104 (52.0%)
    - Thời gian thực thi:            4.24 giây
    - Tốc độ fuzzing:                 47.2 execs/sec

=================================================================
  BLACK-BOX FUZZING (CWE-197 Numeric Truncation) TREN salary_calc.exe (200 runs)
=================================================================
--> Target Binary Executable: K:\TestProject\btl_softsec\ch2_memsafe\salary_calc.exe e2e_byte_truncate <soLuongSinhVien>

--> KẾT QUẢ BLACK-BOX FUZZING (CWE-197) TREN salary_calc.exe:
    - Tổng số lần thử (Attempts):        200
    - Số lần SAI LỆCH DỮ LIỆU (Truncation): 120
    - Số lần bị CHẶN AN TOÀN (Safe Blocked): 0
    - Số lần dữ liệu hợp lệ (Normal):     80
    - Số lần Crash:                       0
    - Thời gian thực thi:                 6.30 giây
    - Mẫu soLuongSinhVien gây sai lệch: [152, 375, 219]

=================================================================
  BLACK-BOX FUZZING (CWE-197 Numeric Truncation) TREN salary_calc_fixed.exe (200 runs)
=================================================================
--> Target Binary Executable: K:\TestProject\btl_softsec\ch2_memsafe\salary_calc_fixed.exe e2e_byte_truncate <soLuongSinhVien>

--> KẾT QUẢ BLACK-BOX FUZZING (CWE-197) TREN salary_calc_fixed.exe:
    - Tổng số lần thử (Attempts):        200
    - Số lần SAI LỆCH DỮ LIỆU (Truncation): 0
    - Số lần bị CHẶN AN TOÀN (Safe Blocked): 150
    - Số lần dữ liệu hợp lệ (Normal):     50
    - Số lần Crash:                       0
    - Thời gian thực thi:                 4.99 giây

=================================================================
  BOUNDARY VALUE ANALYSIS (CWE-197) TREN salary_calc.exe (17 gia tri bien co dinh)
=================================================================
    n= -256  ->  status=TRUNCATED    byte_that=    0  byte_du_kien=    0  [OK]
    n= -255  ->  status=TRUNCATED    byte_that=    1  byte_du_kien=    1  [OK]
    n= -129  ->  status=TRUNCATED    byte_that=  127  byte_du_kien=  127  [OK]
    n= -128  ->  status=OK           byte_that= -128  byte_du_kien= -128  [OK]
    n= -127  ->  status=OK           byte_that= -127  byte_du_kien= -127  [OK]
    n=   -1  ->  status=OK           byte_that=   -1  byte_du_kien=   -1  [OK]
    n=    0  ->  status=OK           byte_that=    0  byte_du_kien=    0  [OK]
    n=    1  ->  status=OK           byte_that=    1  byte_du_kien=    1  [OK]
    n=  126  ->  status=OK           byte_that=  126  byte_du_kien=  126  [OK]
    n=  127  ->  status=OK           byte_that=  127  byte_du_kien=  127  [OK]
    n=  128  ->  status=TRUNCATED    byte_that= -128  byte_du_kien= -128  [OK]
    n=  129  ->  status=TRUNCATED    byte_that= -127  byte_du_kien= -127  [OK]
    n=  255  ->  status=TRUNCATED    byte_that=   -1  byte_du_kien=   -1  [OK]
    n=  256  ->  status=TRUNCATED    byte_that=    0  byte_du_kien=    0  [OK]
    n=  257  ->  status=TRUNCATED    byte_that=    1  byte_du_kien=    1  [OK]
    n=  300  ->  status=TRUNCATED    byte_that=   44  byte_du_kien=   44  [OK]
    n=  384  ->  status=TRUNCATED    byte_that= -128  byte_du_kien= -128  [OK]

--> PHAT HIEN TRUNG LAP BYTE (nhieu soLuongSinhVien HOP LE KHAC NHAU cho CUNG 1 byte):
    byte=-128  <-  cac gia tri soLuongSinhVien: [-128, 128, 384]
    byte=-127  <-  cac gia tri soLuongSinhVien: [-127, 129]
    byte=-1  <-  cac gia tri soLuongSinhVien: [-1, 255]
    byte=0  <-  cac gia tri soLuongSinhVien: [-256, 0, 256]
    byte=1  <-  cac gia tri soLuongSinhVien: [-255, 1, 257]
    byte=127  <-  cac gia tri soLuongSinhVien: [-129, 127]

=================================================================
  BOUNDARY VALUE ANALYSIS (CWE-197) TREN salary_calc_fixed.exe (17 gia tri bien co dinh)
=================================================================
    n= -256  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=    0  [OK]
    n= -255  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=    1  [OK]
    n= -129  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=  127  [OK]
    n= -128  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien= -128  [OK]
    n= -127  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien= -127  [OK]
    n=   -1  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=   -1  [OK]
    n=    0  ->  status=OK           byte_that=    0  byte_du_kien=    0  [OK]
    n=    1  ->  status=OK           byte_that=    1  byte_du_kien=    1  [OK]
    n=  126  ->  status=OK           byte_that=  126  byte_du_kien=  126  [OK]
    n=  127  ->  status=OK           byte_that=  127  byte_du_kien=  127  [OK]
    n=  128  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien= -128  [OK]
    n=  129  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien= -127  [OK]
    n=  255  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=   -1  [OK]
    n=  256  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=    0  [OK]
    n=  257  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=    1  [OK]
    n=  300  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien=   44  [OK]
    n=  384  ->  status=SAFE_BLOCKED byte_that= None  byte_du_kien= -128  [OK]

--> PHAT HIEN TRUNG LAP BYTE (nhieu soLuongSinhVien HOP LE KHAC NHAU cho CUNG 1 byte):
    Khong co trung lap nao (binary nay chan/tu choi truoc khi ep kieu sai lech).
```

**Kịch bản CWE-197 (random) dùng chung 1 baseline nhưng đo trực tiếp bằng subcommand `e2e_byte_truncate <soLuongSinhVien>`** (không qua `stdin` như 2 khối trên) với `soLuongSinhVien` ngẫu nhiên trong `[-50, 400]`: bản BUGGY sai lệch dữ liệu **120/200 (60%)** lần thử; bản FIXED **0/200** sai lệch, chặn an toàn **150/200** lần.

**Boundary Value Analysis (BVA) — 17 giá trị biên cố định, không ngẫu nhiên:** thay vì phó mặc cho `random` may rủi trúng đúng các mốc nguy hiểm, khối BVA chạy **chính xác** 17 giá trị được thiết kế theo phân tích lớp tương đương (mục 6 dưới đây) và đối chiếu byte thật do chương trình in ra với byte tính tay — khớp **17/17 (100%)** trên cả 2 bản, không có sai lệch nào giữa lý thuyết và thực đo. Quan trọng hơn cả số đếm: bảng "PHÁT HIỆN TRÙNG LẶP BYTE" tự động gom nhóm và lộ ra **6 nhóm trùng lặp thật** trên bản BUGGY (ví dụ byte=0 được tạo ra bởi cả 3 giá trị hoàn toàn khác nhau `-256, 0, 256`) — chính là lớp lỗi nguy hiểm nhất đã phân tích, và **0 nhóm trùng lặp** trên bản FIXED vì mọi giá trị ngoài `[0,127]` đều bị chặn trước khi kịp tạo ra byte trùng.

#### 4.4.2 White-box Fuzzing Log Đại diện (`fuzzer_whitebox.py`)
Lệnh thực thi: `python ch4_dynafuzz/fuzzer_whitebox.py`  
File log ghi nhận: [`logs/fuzzer_whitebox.log`](file:///k:/TestProject/btl_softsec/logs/fuzzer_whitebox.log)

```text
=================================================================
  CHUONG 4: WHITE-BOX FUZZING Z3-GUIDED E2E 3-MODULE SYSTEM
=================================================================

[Target 1] Module 1 Lecturer Name Overflow (CWE-120): SAT in 1 attempt
  Condition: hoTen length = 81 chars > MAX_NAME (80, doc tu giang_vien.h)
[Target 2] Module 2 Class Section Code Overflow (CWE-120): SAT in 2 attempt
  Condition: maLop length = 21 chars > MAX_MALOP (20, doc tu lop_hoc_phan.h)
[Target 3] Module 1->2 Use-After-Free (CWE-416): SAT in 3 attempt
  Condition: delete_lecturer() called but Class Section still points to freed memory
[Target 4] Module 2->3 Null Pointer Dereference (CWE-476): SAT in 4 attempt
  Condition: calculate_e2e_salary() called on Class Section with gv_ptr == NULL
[Target 5] Module 3 Integer Overflow (CWE-190): SAT in 5 attempt
  Condition: soTiet = 16694179, dmt = 2147583020 VND -> product > 2,147,483,647

[Target 6] Module 3 Numeric Truncation int->char (CWE-197): SAT in 6 attempt
  Condition: soLuongSinhVien = 200 -> byte ep kieu (char) = -56 (sai lech du lieu audit/thanh toan!)

[Target 7] Module 3 Numeric Truncation Collision (CWE-197): SAT in 7 attempt
  Condition: lop A rong (soLuongSinhVien=0) va lop B co that 256 sinh vien deu xuat ra byte = 0 -> khong the phan biet sau khi xuat bao cao!

--> BẢNG KẾT QUẢ WHITE-BOX FUZZING E2E 3-MODULE:
    - Tổng số lần thử (Attempts):     7 lần (Giải ràng buộc Z3)
    - Số target phát hiện crash/vulnerability: 7 / 7 target
    - Thời gian thực thi:             0.3904 giây
    - Độ chính xác:                    100% (Constraint-based exact SAT trên 7 target đã xác định trước, không phải coverage-guided tự động)
    - Tốc độ tăng tốc so với Blackbox: ~30.5x speedup (dựa trên logs/fuzzer_blackbox.log: 11.90s)
```

**Bảng So sánh Chi tiết Nhất quán:**
| Tiêu chí Đánh giá | Black-box Fuzzing (`fuzzer_blackbox.py`) | White-box Fuzzing (`fuzzer_whitebox.py`) |
| :--- | :--- | :--- |
| **Số lần thử tìm crash** | 200 lần thử ngẫu nhiên | **7 lần thử** (Giải trực tiếp Z3) |
| **Số lần Crash phát hiện** | 72 / 200 (36.0%) | **7 / 7 target (100%)** |
| **Thời gian thực thi** | **11.90 giây** | **0.3904 giây** |
| **Tốc độ cải tiến** | Mức cơ sở (16.8 execs/sec) | **~30.5 lần nhanh hơn** ($11.90\text{s} / 0.3904\text{s} \approx 30.5$) |
| **Độ bao phủ điều kiện** | Phụ thuộc ngẫu nhiên | **100% bao phủ chính xác trên 7 target đã xác định trước** (không phải coverage-guided tự động khám phá) |

> **Ghi chú kỹ thuật:** Tốc độ fuzzing của black-box dao động khá lớn giữa các lần chạy (3.6 → 18.1 execs/sec quan sát được qua nhiều lần chạy) do độ trễ khởi tạo tiến trình con (`subprocess.run`) của Windows không ổn định — vì `read_blackbox_buggy_elapsed()` luôn đọc thời gian thật của lần chạy `fuzzer_blackbox.py` gần nhất, số speedup của white-box (dao động quan sát được từ ~40x đến ~280x tùy lần chạy) dao động theo, nhưng kết luận định tính không đổi: white-box luôn nhanh hơn hàng chục đến hàng trăm lần vì giải ràng buộc trực tiếp thay vì thử ngẫu nhiên.

> **Ghi chú kỹ thuật:** Con số tăng tốc trước đây (`~982.4 lần`) là một giá trị **cố định (hard-coded)** trong `fuzzer_whitebox.py`, không được tính từ thời gian chạy thực tế — vì vậy nó không đổi bất kể black-box chạy nhanh hay chậm, và sai lệch xa so với số đo thật (dao động ~40–280x tùy lần chạy, xem ghi chú dao động ở trên). Đã vá bằng cách đọc thời gian thực thi thật của `logs/fuzzer_blackbox.log` và tính tỉ lệ tăng tốc **động** tại runtime (`read_blackbox_buggy_elapsed()` trong `fuzzer_whitebox.py`). Số liệu tăng tốc vẫn sẽ dao động giữa các lần chạy do overhead nạp thư viện Z3 và độ trễ tiến trình con, nhưng nay phản ánh đúng thực đo thay vì một con số suy diễn. Ngoài ra, "MAX_NAME (80)"/"MAX_MALOP (20)" nay được đọc trực tiếp từ `giang_vien.h`/`lop_hoc_phan.h` thay vì hard-code, và nhãn "Coverage-guided" (vốn gây hiểu lầm vì công cụ không có cơ chế đo độ phủ code thật) đã được sửa thành mô tả đúng bản chất "Constraint-based" — xem thêm giới hạn thuật ngữ ở mục [3.4](#34-chương-4-kiểm-thử-fuzzing-e2e-hộp-đen-vs-hộp-trắng-fuzzer_blackboxpy--fuzzer_whiteboxpy).

---

## 5. PHẦN 5: BẢNG TỔNG HỢP VÀ PHÂN TÍCH MÃ CWE LỖI E2E

| # | Mã CWE chuẩn | Tên lỗ hổng CWE chính thức | Vị trí mô-đun & dòng code | Hành vi nguy hiểm | Giải pháp vá lỗi (dùng qua `main_fixed.c`) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **CWE-120** | *Buffer Copy without Checking Size of Input* | Module 1 & 2 (`giang_vien.c:15`, `lop_hoc_phan.c:13`) | Dùng `strcpy` ghi đè mảng tên Giảng viên ($>80$) và Mã lớp ($>20$), làm phá hỏng bộ nhớ Heap/Stack. | Dùng `snprintf(dest, sizeof(dest), "%s", src)` cắt ngắn chuỗi an toàn. |
| **2** | **CWE-416** | *Use-After-Free (UAF)* | Module 1 $\rightarrow$ 2 (`giang_vien.c:32`) | Gọi `free(gv)` giải phóng bộ nhớ Giảng viên ở Module 1 nhưng giữ nguyên con trỏ treo `lhp->gv_ptr` ở Module 2, khiến Module 3 đọc vùng nhớ rác. | Hủy liên kết `lhp->gv_ptr = NULL` trước khi gọi `free(*gv_pptr)`. |
| **3** | **CWE-476** | *NULL Pointer Dereference* | Module 2 $\rightarrow$ 3 (`tinh_tien_day.c:13`) | Đọc thuộc tính `lhp->gv_ptr->heSoBangCap` khi lớp chưa gán giảng viên (`gv_ptr == NULL`), gây dừng đột ngột (Segfault). | Bổ sung kiểm tra `if (!lhp->gv_ptr)` báo lỗi và trả về 0 VNĐ an toàn. |
| **4** | **CWE-190** | *Integer Overflow or Wraparound* | Module 3 (`tinh_tien_day.c:12-13`) | Ép kiểu `(int)` khi tổng hợp thù lao dạy của nhiều lớp học phần gây tràn số 32-bit. | Chuyển toàn bộ kiểu tính toán thù lao sang `double` và `long long` (64-bit int). |
| **5** | **CWE-1288** | *Improper Degree Enum Validation* | Module 1 (`giang_vien.c:19-23`) | Bằng cấp không hợp lệ bị âm thầm rơi vào fallback `1.0f` làm tính sai thù lao. | Validate danh mục bằng cấp nghiêm ngặt (`GS, PGS, TIEN_SI, THAC_SI, CU_NHAN`). |
| **6** | **CWE-197** | *Numeric Truncation Error* | Module 3 (`tinh_tien_day.c:63`, `pack_class_size_byte_VULN`) | Ép kiểu `(char)` trên `soLuongSinhVien` (int) không kiểm tra phạm vi trước — giá trị $>127$ hoặc $<0$ bị wrap-around (vd $200 \rightarrow -56$), làm sai lệch dữ liệu audit log/thanh toán. | Kiểm tra `if (soLuongSinhVien < 0 \|\| > 127)` và từ chối ép kiểu nếu vượt phạm vi (`pack_class_size_byte_SAFE`) thay vì để wrap-around âm thầm. |

---

## 6. PHẦN 6: THẢO LUẬN VÀ HẠN CHẾ (DISCUSSION & LIMITATIONS)

1. **Bản chất kỹ thuật của thuộc tính Liveness $P_3$ trong Bounded Model Checking (BMC):**
   * Thuộc tính Liveness $P_3: G(\text{assigned} \rightarrow F\,\text{calculated})$ ("Đã phân công thì cuối cùng phải được tính tiền") báo kết quả **SAT** (xuất hiện vết phản ví dụ) trên **cả 2 phiên bản BUGGY và FIXED**.
   * **Phân tích nguyên nhân chuyên sâu**: 
     - Phương pháp kiểm chứng mô hình hữu hạn (BMC) hoạt động bằng cách duỗi mô hình Kripke đến đúng $k$ bước hữu hạn (ở đây $k=5$). 
     - Đối với thuộc tính Safety ($\neg \text{BadState}$), nếu không tìm thấy vết chạm vào trạng thái xấu trong $k$ bước, BMC kết luận **UNSAT** (Proven Safe up to $k$).
     - Đối với thuộc tính Liveness ($F\,\phi$), BMC sinh ra các chuỗi vết độ sâu $k=5$. Nếu tồn tại luồng thực thi rẽ nhánh sang trạng thái lỗi/hủy $S_4$ hoặc lặp chu kỳ chưa kịp chạm tới $S_2$ ($\text{calculated}$) trong đúng $k=5$ bước, solver BMC sẽ xếp vết hữu hạn đó thành một phản ví dụ ngắt luồng.
     - **Kết luận**: Kết quả `SAT` của $P_3$ trên bản `FIXED` phản ánh **hạn chế kỹ thuật tự nhiên của Bounded Model Checking với độ sâu hữu hạn $k=5$ đối với thuộc tính Liveness vô hạn**, hoàn toàn **không phải là lỗi mã nguồn C hay lỗi thiết kế trong bản đã khắc phục**. Để chứng minh Liveness vô hạn triệt để, cần áp dụng quy trình $k$-Induction hoặc chuyển đổi Büchi Automata.

2. **Phát hiện & khắc phục lỗi False Negative trong Pattern Scanner:**
   * Bản `pattern_scanner.py` ban đầu (trước khi vá) mắc lỗi **bỏ sót cảnh báo (False Negative)** nghiêm trọng hơn nhiều so với False Positive thông thường: heuristic "đã được bảo vệ" của `dangling_free`/`unchecked_nested_deref` so khớp chuỗi con thô (`NULL`, `gv_ptr ==`, `if (!`) trên toàn bộ nội dung dòng — **kể cả phần comment giải thích lỗi**. Vì các comment tiếng Việt mô tả đúng lỗi (ví dụ `// LOI CWE-476: ... lhp->gv_ptr == NULL ...` hay `free(gv); // ... thanh NULL!`) lại vô tình chứa đúng các từ khóa "đã bảo vệ", scanner tưởng nhầm 2 vị trí lỗi thật ở `giang_vien.c:32` (CWE-416) và `tinh_tien_day.c:13` (CWE-476) là code đã an toàn và **không hề in ra cảnh báo nào cho 2 CWE này**, dù đây chính là 2 trong 5 lỗ hổng cốt lõi của đề tài.
   * **Giải pháp khắc phục**: Thêm hàm `_code_part()` cắt bỏ phần sau `//` trước khi đưa vào mọi heuristic so khớp (bao gồm cả regex `strcpy`/`free`/`gv_ptr->`), đảm bảo chỉ phần code thật được xét, không bị nhiễu bởi comment. Sau khi vá, `pattern_scanner.py` phát hiện đầy đủ **cả 4/4 loại cảnh báo** (`strcpy`, `dangling_free`, `unchecked_nested_deref`, `int_overflow_cast`) trên 3 file module VULN, trong khi driver bản vá `main_fixed.c` vẫn báo **`[CLEAN]` (0 False Positive)** — xem log đối chiếu tại [4.2](#42-kết-quả-chương-2-pattern-scanner-cppcheck--runtime-binary-log).

3. **Nguyên nhân số liệu Fuzzing có khoảng dao động:** Khi thực thi `fuzzer_blackbox.py`, số lượng crash và tổng thời gian bị dao động giữa các lần chạy do bản chất sinh input ngẫu nhiên (`random.choices`) và độ trễ khởi tạo tiến trình con (`subprocess.run`) của hệ điều hành Windows. Để bảo đảm tính chính xác, báo cáo đã cố định **1 lần chạy đại diện chuẩn (11.90s / 72 crashes trên bản BUGGY)**.

4. **Ưu thế của White-box Fuzzing & sửa lỗi số liệu tăng tốc cố định:** `fuzzer_whitebox.py` trước đây in ra một con số tăng tốc **cố định `~982x`** không phụ thuộc vào thời gian chạy thực tế — nghĩa là con số này sai ngay cả khi so sánh với chính log black-box đi kèm. Đã vá bằng cách đọc thời gian chạy thật của `logs/fuzzer_blackbox.log` và tính tỉ lệ tăng tốc tại runtime. Với lần chạy đại diện hiện tại, White-box Fuzzing đạt tốc độ tăng tốc thực đo **~30.5 lần** (0.3904 giây so với 11.90 giây) và vẫn giữ độ chính xác 100% khi phát hiện cả 7/7 target lỗ hổng E2E chỉ trong 7 lần giải Z3, so với 200 lần thử ngẫu nhiên của black-box. Con số tăng tốc dao động khá lớn giữa các lần chạy (quan sát được từ ~30x đến ~280x) vì phụ thuộc trực tiếp vào thời gian black-box đo được ở mỗi lần — bản chất định tính (white-box luôn nhanh hơn đáng kể) không đổi. (Xem thêm giới hạn thuật ngữ "white-box"/"coverage-guided" đã làm rõ ở mục 3.4 và 4.4.)

5. **Khắc phục vết phản ví dụ (counterexample) không tái lập được trong `kripke_bmc.py`:** Kiểm tra chéo phát hiện: dù kết quả SAT/UNSAT của cả 4 thuộc tính P1-P4 luôn ổn định qua nhiều lần chạy, **vết phản ví dụ cụ thể của $P_1$ lại đổi khác giữa các lần chạy khác nhau** (2 vết hợp lệ khác nhau quan sát được trên 4 lần chạy thử) — nghĩa là log verbatim ghi trong báo cáo không đảm bảo tái lập lại y hệt khi chấm bài. Nguyên nhân gốc: `dst_conds` trong hàm `run_bmc_check_5state()` được dựng từ phép lặp qua một `set` (`Set[str]` không có thứ tự cố định), mà thứ tự lặp của `set` chứa chuỗi trong CPython phụ thuộc vào hash-seed ngẫu nhiên hoá theo từng tiến trình (`PYTHONHASHSEED`); thứ tự assertion khác nhau khiến bộ giải SAT/SMT của Z3 chọn ra các model thỏa mãn khác nhau (đều đúng, nhưng khác vết). **Giải pháp khắc phục**: (a) `sorted(dst_states)` khi dựng `dst_conds` để đảm bảo thứ tự assertion cố định bất kể hash-seed; (b) đặt `solver.set('random_seed', 0)` để cố định seed nội bộ của Z3. Đã xác nhận: chạy `kripke_bmc.py` độc lập 6 lần liên tiếp cho ra đúng 1 vết phản ví dụ duy nhất, khớp 100% với log trong báo cáo này.

6. **Tái cấu trúc `salary_calc_fixed.c` thành driver `main_fixed.c` dùng chung module với bản VULN:** Bản gốc `salary_calc_fixed.c` định nghĩa lại toàn bộ struct và hàm `*_SAFE` trong 1 file riêng, trùng lặp gần như y hệt các hàm `*_SAFE` vốn đã có sẵn trong `giang_vien.c`/`lop_hoc_phan.c`/`tinh_tien_day.c` (2 bản copy lệch nhau: `delete_lecturer_SAFE()` trong `salary_calc_fixed.c` nhận thêm tham số `LopHocPhan *lhp` để hủy liên kết chéo-module, còn bản trong `giang_vien.c` chỉ có 1 tham số và **không** hủy liên kết đó). Đã tái cấu trúc: xóa `salary_calc_fixed.c`, thay bằng `main_fixed.c` — một driver mỏng chỉ gọi lại đúng các hàm `*_SAFE` đã tồn tại trong 3 module dùng chung với `main.c` (đối xứng VULN/SAFE, dễ so sánh), đồng thời chuyển trách nhiệm hủy liên kết chéo-module (fix CWE-416) về tầng điều phối (`main_fixed.c`) thay vì nhét vào API của Module 1 — vừa tránh trùng lặp code, vừa tách bạch rõ ràng trách nhiệm giữa các module. Đã build lại và chạy đủ 4 chế độ `e2e_overflow/e2e_uaf/e2e_null/e2e_integer_overflow` trên `salary_calc_fixed.exe` mới, xác nhận hành vi an toàn giữ nguyên (UAF bị chặn, trả về 0 VNĐ; NULL được xử lý; tên bị cắt an toàn còn 79 ký tự; tổng thù lao lớn (18,700,000,000 VNĐ) tính đúng không tràn số).

7. **Vá 4 hạn chế phương pháp luận sau tự-đánh giá phản biện:** Sau khi tự rà soát nghiêm khắc lại toàn bộ đề tài, 4 điểm yếu về phương pháp luận sau đã được khắc phục thực chất (không chỉ diễn giải lại câu chữ):
   - **Chương 1** — Đặt tên "5 trạng thái" cho cả 2 bản dù bản BUGGY thực có 6 trạng thái ($S_0$-$S_5$): đã sửa để phân biệt rõ 5 (FIXED) vs 6 (BUGGY). Nghiêm trọng hơn: mô hình Kripke trước đây tồn tại **hoàn toàn độc lập, không có cơ chế nào xác nhận nó khớp với code C thật**. Đã thêm `cross_validate_with_pattern_scanner()` — gọi lại chính scanner Chương 2 để tự động xác nhận trạng thái `S4_ERROR` tương ứng với lỗ hổng thật (`giang_vien.c:32`, `tinh_tien_day.c:13`); đã kiểm thử bằng cách tạm vá lỗi CWE-476 và xác nhận cơ chế in đúng cảnh báo "mô hình có thể không còn khớp" thay vì im lặng — chứng minh đây là kiểm tra thật, không phải rubber-stamp.
   - **Chương 2** — Cửa sổ lookback 8 dòng cố định để tìm guard-check có thể bỏ sót bảo vệ nằm xa hơn trong hàm dài, hoặc tràn ngược sang hàm liền trước nếu hàm hiện tại ngắn. Đã thay bằng `_compute_function_starts()` scope tìm kiếm đúng theo ranh giới hàm bao quanh. Đã kiểm thử bằng 2 file C tổng hợp: 1 file có guard-check hợp lệ đặt xa 11 dòng (bản cũ sẽ báo sai thành lỗi — false positive; bản mới đúng `[CLEAN]`), và 1 file không có guard nào (vẫn bị phát hiện đúng).
   - **Chương 3** — Check 3 dùng biến `Bool`/`Real` trừu tượng (`hasLecturer`, `salaryPaid`) hoàn toàn tách rời công thức C thật, về bản chất là chứng minh một tautology tự dựng. Đã viết lại bằng đúng công thức trong `calculate_e2e_salary_SAFE()` (dùng chung biến `soTiet`/`heSoHocPhan`/`heSoBangCap`/`dinhMucTienChuan` với Check 1/2, gói trong `If(Or(gv_ptr_is_null, is_deleted), 0, cong_thuc_that)`).
   - **Chương 4** — Tên gọi "White-box Z3-Guided Fuzzing" và nhãn "Coverage-guided" dễ gây hiểu lầm là symbolic execution/coverage-guided tự động thật, trong khi thực chất là 5 ràng buộc Z3 viết tay cho 5 mục tiêu đã biết trước. Đã bổ sung docstring minh bạch giới hạn phạm vi, sửa nhãn "Coverage-guided" thành "Constraint-based", và — quan trọng hơn — thay hằng số hard-code `80`/`20` bằng `read_header_define()` đọc trực tiếp `MAX_NAME`/`MAX_MALOP` từ `giang_vien.h`/`lop_hoc_phan.h`; đã kiểm thử độc lập bằng cách đổi giá trị trong 1 header tạm và xác nhận ràng buộc Z3 tự động bám theo giá trị mới, chứng minh đây là liên kết thật tới source, không phải số hard-code giả danh.

   Toàn bộ 4 lần vá đã được build lại + chạy `run_all.py` để tái sinh log, không phát sinh lỗi biên dịch hay regression ở bất kỳ chương nào.

8. **Bổ sung lỗ hổng thứ 6 — CWE-197 Numeric Truncation Error — xuyên suốt cả 4 chương:** Theo góp ý cần minh họa thêm kịch bản "dữ liệu ngoài phạm vi được tính bằng `int` rồi ép kiểu xuống `char`", đã thêm cặp hàm `pack_class_size_byte_VULN()`/`pack_class_size_byte_SAFE()` (`tinh_tien_day.c`) ép `soLuongSinhVien` (thực tế có thể lên tới vài trăm với lớp đại cương) xuống `signed char` khi đóng gói bản ghi audit log, và lan tỏa đúng lỗ hổng này qua cả 4 chương thay vì chỉ thêm 1 file rời rạc:
   - **Chương 1**: Thêm nhãn `byte_truncated` trên $S_3$\_EXPORTED (chỉ bản BUGGY) và thuộc tính $P_5$: $G(\text{exported} \rightarrow \neg\,\text{byte\_truncated})$ — **SAT** (vi phạm) trên BUGGY, **UNSAT** (an toàn) trên FIXED.
   - **Chương 2**: Thêm rule `unchecked_numeric_truncation` — quét `(char)` cast không có `if` guard phạm vi (`<`/`>`) đứng trước trong cùng hàm; đã kiểm thử phân biệt đúng cả 2 hàm VULN (bị bắt) và SAFE (không bị bắt, cùng nằm trong 1 file).
   - **Chương 3**: Thêm Check 4 (SAT — mô hình hóa `(char)` bằng số học modulo 256/wrap dấu, phản ví dụ `128 -> -128`) và Check 5 (UNSAT — chứng minh hình thức: với guard `0..127` đúng, ép kiểu không bao giờ sai lệch).
   - **Chương 4**: Thêm subcommand `e2e_byte_truncate <n>` vào `main.c`/`main_fixed.c`, black-box fuzz 200 lần trên mỗi bản (BUGGY: 120/200 sai lệch dữ liệu; FIXED: 0/200 sai lệch, 150/200 bị chặn an toàn), và Target 6 trong white-box tìm chính xác `soLuongSinhVien=200 -> byte=-56` chỉ trong 1 lần giải Z3.

   Đã build lại + chạy `run_all.py`, xác nhận cả 5 log tự động (`kripke_bmc.log`, `pattern_scanner.log`, `smt_verify.log`, `fuzzer_blackbox.log`, `fuzzer_whitebox.log`) đều phản ánh đúng lỗ hổng mới, không có regression trên 5 lỗ hổng CWE cũ.

9. **Bao phủ hệ thống miền giá trị "ngoài phạm vi" bằng Equivalence Partitioning (EP) & Boundary Value Analysis (BVA), thay vì chỉ nghĩ "âm là sai, còn lại thì đúng":** Với phép ép kiểu `int -> signed char` (miền đích `[-128,127]`), phân tích thuần lý thuyết kiểu dữ liệu (không đọc code trước) cho ra 7 lớp tương đương cần phủ:
   - **Lớp 1** — nằm gọn trong `[-128,127]`: không mất mát.
   - **Lớp 2** — tràn dương 1 vòng `[128,255]`: `byte = n - 256`, luôn ra số âm.
   - **Lớp 3 (nguy hiểm nhất)** — tràn ≥ 2 vòng, đúng bội số 256 (`256, 512,...`): nhiều `soLuongSinhVien` **hợp lệ và khác nhau** cho ra **cùng một byte** — vd `n=0` (lớp thật sự rỗng) và `n=256` (lớp có thật 256 sinh viên) đều xuất ra byte `0`. Đây không còn là "sai số" mà là **1 giá trị hợp lệ giả mạo 1 giá trị hợp lệ khác** — nếu module sau này có quy tắc kiểu "byte=0 → coi là lớp chưa mở, không duyệt lương", cả 2 tình huống hoàn toàn khác nhau sẽ bị xử lý giống hệt nhau.
   - **Lớp 4** — tràn âm đối xứng lớp 2/3 (`n < -128`, kể cả bội số -256).
   - **Lớp 5** — input âm nhưng vẫn "vừa" miền char (`[-128,-1]`): byte không hề bị wrap, nhưng bản thân giá trị đã vô lý về nghiệp vụ (số sinh viên âm) — một lỗ hổng **khác** (thiếu validate miền giá trị nghiệp vụ), không phải CWE-197.
   - **Lớp 6** — các giá trị biên BVA đúng nghĩa quanh mọi mép: `-129/-128/-127`, `126/127/128/129`, và mép chu kỳ 256: `-256/-255/255/256/257`.
   - **Lớp 7** — cực trị kiểu `int` (`INT_MIN`/`INT_MAX`): về chuẩn C, ép kiểu ra ngoài miền sang kiểu có dấu hẹp hơn là **implementation-defined** (không phải UB, nhưng chuẩn không bắt buộc phải là mod-256) — một giả định ngầm cần nói rõ dù mọi compiler chính (GCC/Clang/MSVC) đều hiện thực giống nhau trong thực tế.

   **Áp dụng thực tế — mỗi chương phủ đúng theo tầng trừu tượng của nó, không ép tất cả làm giống nhau:**
   - *Chương 1 (Kripke/BMC)* chỉ mô hình hóa control-flow/nhãn trạng thái, không có số học chính xác — nên "bao phủ" ở đây là mức tổng quát: $P_5$ chứng minh **tồn tại** một luồng thực thi đạt tới export với dữ liệu bị ép kiểu sai (đã đủ, không cần tách riêng property cho từng lớp tương đương vì Kripke không biểu diễn giá trị số cụ thể).
   - *Chương 2 (pattern scanner)* quét cấu trúc mã nguồn, không suy luận giá trị — 1 cảnh báo tĩnh (thiếu guard trước `(char)`) tự động phủ **toàn bộ** miền giá trị có thể xảy ra tại runtime, không cần liệt kê từng trường hợp.
   - *Chương 3 (Z3 SMT)* là nơi phù hợp nhất để phủ EP/BVA một cách hình thức: Check 4/5 phủ lớp 1+2 (SAT/UNSAT có/không guard), **Check 6 (mới)** phủ đúng lớp 3 — chứng minh **tồn tại** cặp giá trị trùng lặp bằng cách quantify trên toàn miền `[0,300]²`, thứ mà test mẫu khó tự tìm ra.
   - *Chương 4 (fuzzing)* bổ sung `run_bva_truncation_test()` — chạy **17 giá trị biên cố định** (lớp 6, thiết kế sẵn chứ không phó mặc `random`) trên binary thật, đối chiếu byte thật với byte tính tay, và tự động gom nhóm để lộ ra 6 cặp trùng lặp thật (khớp Check 6); **Target 7 (white-box)** giải trực tiếp đúng cặp `(0, 256)` bằng Z3 trong 1 lần thử.

   **Kết luận phương pháp luận**: câu hỏi "ngoài phạm vi thì sao" không có một câu trả lời duy nhất — độ rộng của "ngoài phạm vi" (7 lớp tương đương ở trên) đòi hỏi phối hợp nhiều kỹ thuật kiểm chứng khác nhau, mỗi kỹ thuật giỏi ở một tầng trừu tượng riêng: BMC cho luồng điều khiển, static scan cho cấu trúc mã nguồn không phụ thuộc giá trị, SMT cho chứng minh hình thức trên toàn miền, và fuzzing (ngẫu nhiên + BVA có chủ đích) cho bằng chứng thực thi. Không có kỹ thuật nào một mình phủ hết.

10. **Bổ sung bằng chứng động cho câu hỏi "bộ nhớ được dùng ra sao qua từng bước của 1 luồng bất kỳ" (`ch2_memsafe/memory_trace_demo.py`):** Toàn bộ Chương 1-3 là phân tích **tĩnh** (không chạy code thật); Chương 4 chạy thật nhưng chỉ đo crash/exit-code, không lộ ra *tại sao*. Để trả lời trực tiếp câu hỏi runtime, đã viết thêm script biên dịch 2 bản nhị phân cho cùng 1 luồng E2E 7 bước (nhập → tạo GV → tạo lớp → tính lương → ép byte → xóa GV → xuất báo cáo):
    - **Plain GCC**: chỉ in địa chỉ con trỏ thật tại mỗi bước — kết quả: chương trình **chạy hết, exit code 0**, dù Bước 7 đọc đúng địa chỉ đã bị `free()` ở Bước 6 (chứng minh UAF có thể hoàn toàn im lặng trên build thông thường).
    - **Clang64 + AddressSanitizer**: không tự báo cáo gì, để công cụ độc lập tự phát hiện — kết quả: **ASan thật sự chặn chương trình** với chẩn đoán `heap-use-after-free`, chỉ đúng ra vùng nhớ 132 byte đã cấp phát cho `GiangVien`, offset 24 byte (đúng vị trí field `hoTen`), khớp 100% với địa chỉ đã in ở Bước 2/6/7.
    - Bản FIXED (dùng `main_fixed.c`, huỷ liên kết `gv_ptr = NULL` trước khi free) chạy sạch qua cả 2 bản, ASan xác nhận không có vi phạm.

    Đây là minh chứng thực nghiệm độc lập (không phải suy luận đọc code) cho chính bảng "Memory Usage Trace" đã thảo luận ở trên: bug an toàn bộ nhớ = một bước sau tái sử dụng vùng nhớ mà bước trước đã thiết lập giả định, không kiểm tra lại — nay có địa chỉ con trỏ thật và chẩn đoán công cụ thật làm bằng chứng, xem log đầy đủ tại [4.2.2](#422-bằng-chứng-động-memory-trace-qua-addresssanitizer-thật).

---

## 7. PHẦN 7: KẾT LUẬN, TÀI LIỆU THAM KHẢO VÀ PHỤ LỤC

### 7.1 Kết luận Đề tài
Dự án đã nâng cấp thành công bộ công cụ **SoftSec Toolkit** hỗ trợ **End-to-End (E2E) Testing** tích hợp 3 mô-đun cốt lõi của **DuongUniversity Management System**. Bộ kiểm thử đã phát hiện, minh chứng và khắc phục triệt để **6 lỗ hổng an toàn bộ nhớ và dữ liệu (CWE-120, CWE-416, CWE-476, CWE-190, CWE-1288, CWE-197)**, hoàn thành 100% yêu cầu học phần.

### 7.2 Tài liệu Tham khảo (References)
1. **DeMoura, L., & Bjørner, N. (2008).** *Z3: An efficient SMT solver.* TACAS 2008.
2. **NIST MITRE.** *Common Weakness Enumeration (CWE-120, CWE-416, CWE-476, CWE-190).*
3. **SoftSec Toolkit Team (2025).** *Giáo trình An toàn Phần mềm.* Khoa CNTT - DuongUniversity.

### 7.3 Phụ lục Checklist Nộp bài (Slide 20)
- [x] **Trang bìa & Mục lục chuẩn cấu trúc Slide BTL_02.**
- [x] **`ch2_memsafe/giang_vien.c`, `lop_hoc_phan.c`, `tinh_tien_day.c`, `main.c`**: Mã nguồn C E2E 3 mô-đun (đã tách module hóa) chứa 6 lỗ hổng cố ý.
- [x] **`ch2_memsafe/main_fixed.c`**: Driver phiên bản đã khắc phục an toàn 100%, dùng chung 3 module với bản VULN.
- [x] **`ch1_models/kripke_bmc.py`**: Mã nguồn BMC E2E kiểm chứng 5/6 trạng thái (FIXED/BUGGY) & 5 LTL properties.
- [x] **`ch2_memsafe/pattern_scanner.py`**: Quét tĩnh lỗi liên mô-đun E2E.
- [x] **`ch2_memsafe/memory_trace_demo.py`**: Bằng chứng động (Plain GCC + Clang64/ASan thật) cho luồng E2E 7 bước.
- [x] **`ch3_staticsat/smt_verify.py`**: Kiểm chứng Z3 SMT cho các ràng buộc E2E.
- [x] **`ch4_dynafuzz/fuzzer_blackbox.py`**: Fuzzing hộp đen E2E.
- [x] **`ch4_dynafuzz/fuzzer_whitebox.py`**: Fuzzing hộp trắng Z3-guided E2E.
- [x] **`README_REPRODUCE.md`**: Hướng dẫn chạy E2E tái lập chi tiết.
- [x] **`BAO_CAO_BTL_SOFTSEC.md`**: Báo cáo đầy đủ 7 phần đính kèm 100% log thực tế.

---
*DuongUniversity SoftSec Toolkit E2E Report Completed.*
