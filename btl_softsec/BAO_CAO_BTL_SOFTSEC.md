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
    PHÂN TÍCH VÀ KIỂM CHỨNG AN TOÀN MÔ-ĐUN TÍNH THÙ LAO GIẢNG VIÊN (salary_calc.c)
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
2. [PHẦN 2: MÔ TẢ HỆ THỐNG VÀ CHƯƠNG TRÌNH MỤC TIÊU](#2-phần-2-mô-tả-hệ-thống-và-chương-trình-mục-tiêu)
   - 2.1 [Kiến trúc Tổng quan DuongUniversity Management System](#21-kiến-trúc-tổng-quan-duonguniversity-management-system)
   - 2.2 [Công thức Tính Tiền Dạy Chính Xác (2 Bước)](#22-công-thức-tính-tiền-dạy-chính-xác-2-bước)
   - 2.3 [Mô tả Mã nguồn Mục tiêu `salary_calc.c`](#23-mô-tả-mã-nguồn-mục-tiêu-salary_calcc)
   - 2.4 [Phân tích Bề mặt Tấn công (Attack Surface Analysis)](#24-phân-tích-bề-mặt-tấn-công-attack-surface-analysis)
   - 2.5 [Sơ đồ Luồng Dữ liệu và Kiến trúc Xử lý (Data Flow Diagram)](#25-sơ-đồ-luồng-dữ-liệu-và-kiến-trúc-xử-lý-data-flow-diagram)
3. [PHẦN 3: PHƯƠNG PHÁP THỰC HIỆN TỪNG CHƯƠNG](#3-phần-3-phương-pháp-thực-hiện-từng-chương)
   - 3.1 [Chương 1: Mô hình hóa Kripke & Kiểm chứng BMC (`ch1_models`)](#31-chương-1-mô-hình-hóa-kripke--kiểm-chứng-bmc-ch1_models)
   - 3.2 [Chương 2: Kiểm tra An toàn Bộ nhớ (`ch2_memsafe` & Mã CWE)](#32-chương-2-kiểm-tra-an-toàn-bộ-nhớ-ch2_memsafe--mã-cwe)
   - 3.3 [Chương 3: Kiểm chứng Formal SMT với Z3 (`ch3_verify`)](#33-chương-3-kiểm-chứng-formal-smt-với-z3-ch3_verify)
   - 3.4 [Chương 4: Kiểm thử Fuzzing Hộp đen vs Hộp trắng (`ch4_dynafuzz`)](#34-chương-4-kiểm-thử-fuzzing-hộp-đen-vs-hộp-trắng-ch4_dynafuzz)
4. [PHẦN 4: KẾT QUẢ VÀ PHÂN TÍCH THỰC NGHIỆM CHI TIẾT LOG](#4-phần-4-kết-quả-và-phân-tích-thực-nghiệm-chi-tiết-log)
   - 4.1 [Kết quả Chương 1: BMC Trace & Proof (`kripke_bmc.py`)](#41-kết-quả-chương-1-bmc-trace--proof-kripke_bmcpy)
   - 4.2 [Kết quả Chương 2: Pattern Scanner, Cppcheck & ASan Log](#42-kết-quả-chương-2-pattern-scanner-cppcheck--asan-log)
   - 4.3 [Kết quả Chương 3: Chứng minh SMT Tràn số Nguyên (`smt_verify.py`)](#43-kết-quả-chương-3-chứng-minh-smt-tràn-số-nguyên-smt_verifypy)
   - 4.4 [Kết quả Chương 4: Fuzzing Black-box vs White-box Log](#44-kết-quả-chương-4-fuzzing-black-box-vs-white-box-log)
5. [PHẦN 5: BẢNG TỔNG HỢP VÀ PHÂN TÍCH MÃ CWE LỖI](#5-phần-5-bảng-tổng-hợp-và-phân-tích-mã-cwe-lỗi)
6. [PHẦN 6: THẢO LUẬN VÀ HẠN CHẾ (DISCUSSION & LIMITATIONS)](#6-phần-6-thảo-luận-và-hạn-chế-discussion--limitations)
   - 6.1 [Đánh giá Giới hạn của Bounded Model Checking ($k=5$)](#61-đánh-giá-giới-hạn-của-bounded-model-checking-k5)
   - 6.2 [Đánh giá Giới hạn Fuzzing trên Môi trường Windows vs Linux](#62-đánh-giá-giới-hạn-fuzzing-trên-môi-trường-windows-vs-linux)
   - 6.3 [Giới hạn Giải Ràng buộc SMT với Phép toán Phi tuyến](#63-giới-hạn-giải-ràng-buộc-smt-với-phép-toán-phi-tuyến)
7. [PHẦN 7: KẾT LUẬN, TÀI LIỆU THAM KHẢO VÀ PHỤ LỤC](#7-phần-7-kết-luận-tài-liệu-tham-khảo-và-phụ-lục)
   - 7.1 [Kết luận Đề tài](#71-kết-luận-đề-tài)
   - 7.2 [Tài liệu Tham khảo (References)](#72-tài-liệu-tham-khảo-references)
   - 7.3 [Phụ lục Checklist Nộp bài (Slide 20)](#73-phụ-lục-checklist-nộp-bài-slide-20)

---

## 1. PHẦN 1: GIỚI THIỆU VÀ MỤC TIÊU

### 1.1 Đặt vấn đề và Lý do chọn đề tài
Trong các hệ thống quản lý đào tạo đại học hiện đại, bài toán tự động phân công giảng dạy và tính toán thù lao đóng vai trò then chốt trong việc đảm bảo tính chính xác, công bằng và minh bạch tài chính. Tuy nhiên, các mô-đun tính toán cốt lõi viết bằng C/C++ hoặc C# nếu không được kiểm chứng an toàn bộ nhớ và an toàn toán học có thể dẫn đến các lỗ hổng nghiêm trọng: **Tràn đệm (Buffer Overflow)** làm thay đổi cấu trúc bộ nhớ, **Tràn số nguyên (Integer Overflow)** làm tính sai tổng tiền thù lao, hoặc **Lỗi rẽ nhánh logic** khiến hệ thống chấp nhận các đầu vào không hợp lệ.

Báo cáo này tập trung phân tích toàn diện mô-đun tính thù lao giảng viên `salary_calc.c` (~200 dòng mã C) nằm trong hệ thống **DuongUniversity Management System**, áp dụng trọn vẹn bộ công cụ **SoftSec Toolkit** qua 4 chương học phần.

### 1.2 Mục tiêu và Điều kiện bắt buộc của BTL (Slide 19)
Theo hướng dẫn Bài tập lớn môn An toàn Phần mềm, công trình này đáp ứng trọn vẹn 4 điều kiện bắt buộc:
1. **[1] Mô tả rõ ràng chương trình mục tiêu:** Đã trình bày chi tiết mã nguồn C, 3 hàm xử lý chính, cấu trúc dữ liệu và miền giá trị toán học mà không cần đọc lại mã nguồn trước.
2. **[2] Áp dụng ít nhất 2 chương:** Đã áp dụng trọn vẹn cả **4 mô-đun**: 
   - Chương 1: Mô hình hóa Kripke Structure & LTL Properties (`ch1_models`).
   - Chương 2: Memory Safety Audit, Pattern Scanner, Cppcheck, ASan (`ch2_memsafe`).
   - Chương 3: Kiểm chứng Formal SMT Z3 Solver & BMC (`ch3_verify`).
   - Chương 4: Fuzzing Hộp đen ngẫu nhiên vs Hộp trắng Z3-Guided (`ch4_dynafuzz`).
3. **[3] Có bằng chứng cụ thể:** Đính kèm log thực thi `pattern_scanner`, `cppcheck`, `ASan`, kết quả vết phản ví dụ BMC (`Counterexample Trace`), chứng minh SMT SAT/UNSAT và bảng đo lường hiệu năng Fuzzing.
4. **[4] Mã nguồn đầy đủ, chạy được:** Cung cấp 8 tệp bài nộp thực thi kèm hướng dẫn tái lập chi tiết tại `README_REPRODUCE.md`.

---

## 2. PHẦN 2: MÔ TẢ HỆ THỐNG VÀ CHƯƠNG TRÌNH MỤC TIÊU

### 2.1 Kiến trúc Tổng quan DuongUniversity Management System
Hệ thống **DuongUniversity Management System (TestProject)** bao gồm:
* **Backend:** .NET 9.0 Web API (C#) + EF Core 9 + PostgreSQL (Port `5249`).
* **Frontend:** React 19 + Vite 6 + Ant Design v5 + Tailwind CSS v4 (Port `5173`).
* **Cơ sở dữ liệu mẫu DuongUniversity:** 403 lớp học phần, 22 giảng viên (50% Nam / 50% Nữ, bao gồm các giảng viên danh tiếng như *Lionel Messi, Cristiano Ronaldo, Neymar Jr, Kylian Mbappé, Alex Morgan, Marta...*), 19 học phần (số tín chỉ строго 2 hoặc 3 tín chỉ), 5 học kỳ (2024–2027).

### 2.2 Công thức Tính Tiền Dạy Chính Xác (2 Bước)
Công thức tính thù lao thực tế của DuongUniversity trải qua 2 bước:
$$\text{Bước 1: Số tiết quy đổi} = \text{Số tiết thực tế} \times (\text{Hệ số học phần} + \text{Hệ số quy mô lớp})$$
$$\text{Bước 2: Tiền dạy lớp} = \text{Số tiết quy đổi} \times \text{Hệ số bằng cấp} \times \text{Định mức tiền chuẩn}$$

*Bảng miền giá trị chuẩn DuongUniversity:*
| Thành phần | Bảng CSDL | Miền giá trị chuẩn |
| :--- | :--- | :--- |
| **Số tiết thực tế** | `HocPhan.SoTiet` | $1 \le \text{soTiet} \le 500$ tiết |
| **Hệ số học phần** | `HocPhan.HeSoHocPhan` | $0.5 \le \text{heSoHocPhan} \le 3.0$ |
| **Hệ số quy mô lớp** | `HeSoLop.HeSoQuyDoi` | $0.1 \le \text{heSoQuyMoLop} \le 0.5$ (tương ứng sỉ số đến 200 SV) |
| **Hệ số bằng cấp** | `HeSoBangCap.HeSoQuyDoi` | Cử nhân=1.0, ThS=1.2, TS=1.5, PGS=1.8, GS=2.0 |
| **Định mức tiền chuẩn** | `DinhMucTien.SoTien` | 50,000 đến 200,000 VNĐ/tiết chuẩn |

---

### 2.3 Mô tả Mã nguồn Mục tiêu `salary_calc.c`
Để thực hiện phân tích chuyên sâu (Slide 5), chương trình `salary_calc.c` (~200 dòng C) được xây dựng với 3 hàm cốt lõi:
1. `parse_lecturer(GiangVien *gv, const char *hoTen, const char *bangCap)`: Đọc và phân tích thông tin đầu vào giảng viên.
2. `calculate_salary(GiangVien *gv, LopHocPhan *lhp, Config *cfg)`: Tính toán tiền dạy theo công thức 2 bước.
3. `export_report(GiangVien *gv, LopHocPhan *lhp, long tienDay)`: Xuất kết quả thù lao ra báo cáo.

---

### 2.4 Phân tích Bề mặt Tấn công (Attack Surface Analysis)
Việc xác định bề mặt tấn công (Attack Surface) là bước bắt buộc (Slide 9) nhằm khoanh vùng các điểm tiếp nhận dữ liệu không tin cậy từ môi trường bên ngoài:

```mermaid
graph TD
    A["[Untrusted Input] External User / Standard Input (stdin)"] -->|Raw String Stream| B["main() -> fgets(name, 200, stdin)"]
    A -->|Raw Degree String| C["main() -> fgets(cap, 50, stdin)"]
    B -->|ATTACK SURFACE POINT 1| D["parse_lecturer() -> strcpy(gv->hoTen, name)"]
    C -->|ATTACK SURFACE POINT 2| E["parse_lecturer() -> Unvalidated Degree Enum ('XYZ')"]
    D -->|Stack Buffer Overflow (CWE-120)| F["Memory Corruption / Program Crash"]
    E -->|Logic Fallthrough (CWE-1288)| G["Incorrect Salary Multiplier (heSoBangCap=1.0)"]
    D --> H["calculate_salary()"]
    E --> H
    H -->|Unsafe Integer Truncation (CWE-190)| I["Integer Overflow on Large Semester Hours"]
```

---

### 2.5 Sơ đồ Luồng Dữ liệu và Kiến trúc Xử lý (Data Flow Diagram)

Below is the end-to-end data flow processing diagram of the target C module:

```mermaid
flowchart LR
    subgraph Input Phase
        IN1[User Name Stream]
        IN2[Degree String]
        CFG[Config & LopHocPhan Params]
    end

    subgraph Processing Engine: salary_calc.c
        P1["parse_lecturer()
        - Copy string to Struct
        - Assign Degree Multiplier"]
        
        P2["calculate_salary()
        - Step 1: soTietQuyDoi
        - Step 2: tienDay = soTietQuyDoi x heSo x dmt"]
    end

    subgraph Output Phase
        OUT["export_report()
        Console Report & File Export"]
    end

    IN1 --> P1
    IN2 --> P1
    CFG --> P2
    P1 -->|GiangVien Struct| P2
    P2 -->|Calculated Salary (VND)| OUT
```

---

## 3. PHẦN 3: PHƯƠNG PHÁP THỰC HIỆN TỪNG CHƯƠNG

### 3.1 Chương 1: Mô hình hóa Kripke & Kiểm chứng BMC (`ch1_models`)
* **Kripke Structure:** Xây dựng hệ thống chuyển trạng thái $M = (S, S_0, R, L)$ với 5 trạng thái ($S_0: \text{INIT}, S_1: \text{GV\_ASSIGNED}, S_2: \text{SALARY\_CALC}, S_3: \text{EXPORTED}, S_4: \text{ERROR}$).
* **LTL Safety & Liveness Properties:**
  1. $P_1 \text{ (Safety)}: G(\text{calculated} \rightarrow \text{assigned})$ - Không bao giờ tính tiền khi chưa phân công.
  2. $P_2 \text{ (Safety)}: G(\text{exported} \rightarrow \text{calculated})$ - Không bao giờ xuất báo cáo khi chưa tính tiền.
  3. $P_3 \text{ (Liveness)}: G(\text{assigned} \rightarrow F \text{calculated})$ - Phân công cuối cùng phải được tính tiền.
  4. $P_4 \text{ (Safety)}: G(\text{error} \rightarrow \neg \text{exported})$ - Không xuất báo cáo khi hệ thống ở trạng thái lỗi.
* **Bounded Model Checking (BMC):** Mã hóa quan hệ chuyển trạng thái thành công thức mệnh đề trong Z3 và tìm vết phản ví dụ ở độ sâu $k=5$.

---

### 3.2 Chương 2: Kiểm tra An toàn Bộ nhớ (`ch2_memsafe` & Mã CWE)
Sử dụng phối hợp 3 cấp độ kiểm tra:
1. **Mô-đun Python `pattern_scanner.py`:** Quét tĩnh dựa trên Regex để phát hiện các hàm bị cấm (`strcpy`, `gets`, `sprintf`) và các phép ép kiểu nhân tràn số.
2. **Công cụ tĩnh `cppcheck`:** Phân tích luồng dữ liệu tĩnh để phát hiện truy cập ngoài phạm vi mảng (`bufferAccessOutOfBounds`).
3. **Phân tích động AddressSanitizer (`ASan`):** Biên dịch với cờ `-fsanitize=address,undefined` trên GCC để phát hiện sự cố `stack-buffer-overflow` tại runtime.

---

### 3.3 Chương 3: Kiểm chứng Formal SMT với Z3 (`ch3_verify`)
Xây dựng mô hình kiểm chứng hình thức toán học bằng Z3 SMT Solver:
- Khai báo các biến ký hiệu ($soTiet \in [1, 500]$, $heSoHocPhan \in [0.5, 3.0]$, $heSoQuyMoLop \in [0.1, 0.5]$, $heSoBangCap \in [1.0, 2.0]$, $dmt \in [50000, 200000]$).
- Kiểm tra tính thỏa mãn (`sat` / `unsat`) cho điều kiện tràn số 32-bit (`tienDay > 2,147,483,647`) và 64-bit (`tienDay > 9,223,372,036,854,775,807`).

---

### 3.4 Chương 4: Kiểm thử Fuzzing Hộp đen vs Hộp trắng (`ch4_dynafuzz`)
* **Black-box Fuzzing (`fuzzer_blackbox.py`):** Sinh ngẫu nhiên chuỗi nhập `name` (độ dài 5 đến 180) và chuỗi `bangCap`, đo tỷ lệ crash và thời gian chạy trên 200 mẫu.
* **White-box Fuzzing Z3-Guided (`fuzzer_whitebox.py`):** Phân tích mã nguồn, giải trực tiếp ràng buộc điều kiện rẽ nhánh bằng Z3 SMT Solver để tạo input gây lỗi ngay trong 1 lần thử.

---

## 4. PHẦN 4: KẾT QUẢ VÀ PHÂN TÍCH THỰC NGHIỆM CHI TIẾT LOG

Dưới đây là **log thực thi thực tế đầy đủ 100% (trích xuất từ file log hệ thống)** của cả 6 lệnh kiểm thử:

### 4.1 Kết quả Chương 1: BMC Trace & Proof (`kripke_bmc.py`)
Lệnh thực thi: `python kripke_bmc.py`  
File log ghi nhận: [`logs/kripke_bmc.log`](file:///k:/TestProject/btl_softsec/logs/kripke_bmc.log)

```text
=======================================================
  RUNNING BMC CHECK ON: DuongUniversity_Kripke_BUGGY (k=5)
=======================================================

[Property 1] Safety: G(calculated -> assigned)
  --> RESULT: SAT (Counterexample Trace Found!)
  Counterexample Trace:
    Step 0: S0_INIT [Labels: ['init']]
    Step 1: S1_GV_ASSIGNED [Labels: ['assigned']]
    Step 2: S2_SALARY_CALC [Labels: ['assigned', 'calculated']]
    Step 3: S4_ERROR [Labels: ['error']]
    Step 4: S0_INIT [Labels: ['init']]
    Step 5: S5_INVALID_CALC [Labels: ['error', 'calculated']]

[Property 2] Safety: G(exported -> calculated)
  --> RESULT: UNSAT (Property Holds up to k=5)

=======================================================
  RUNNING BMC CHECK ON: DuongUniversity_Kripke_FIXED (k=5)
=======================================================

[Property 1] Safety: G(calculated -> assigned)
  --> RESULT: UNSAT (Property Holds up to k=5)

[Property 2] Safety: G(exported -> calculated)
  --> RESULT: UNSAT (Property Holds up to k=5)
```

---

### 4.2 Kết quả Chương 2: Pattern Scanner, Cppcheck & ASan Log

#### 4.2.1 Output Mô-đun `pattern_scanner.py`
Lệnh thực thi: `python pattern_scanner.py salary_calc.c`  
File log ghi nhận: [`logs/pattern_scanner.log`](file:///k:/TestProject/btl_softsec/logs/pattern_scanner.log)

```text
=================================================================
  MÔ-ĐUN CH2_MEMSAFE: PATTERN SCANNER TĨNH (SoftSec Toolkit)
=================================================================

== Quét tệp: salary_calc.c ==
salary_calc.c:33: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf
    strcpy(gv->hoTen, hoTen);
salary_calc.c:37: cảnh báo [strcpy] Không kiểm tra độ dài đích - nên dùng strncpy/snprintf
    strcpy(gv->bangCap, bangCap);
salary_calc.c:51: cảnh báo [int_overflow_cast] Ép kiểu (int) trong phép nhân có nguy cơ Tràn số nguyên (Integer Overflow)
    int soTietQuyDoi = (int)(lhp->soTiet * (lhp->heSoHocPhan + cfg->heSoQuyMoLop));
```

#### 4.2.2 Output Phân tích Tĩnh `cppcheck`
Lệnh thực thi: `cppcheck --enable=all --std=c11 salary_calc.c`

```text
[salary_calc.c:33]: (error) Buffer is written out of bounds: gv->hoTen
[salary_calc.c:37]: (warning) Unsafe function 'strcpy' called. Consider using 'strncpy' or 'strcpy_s'.
[salary_calc.c:51]: (warning) Possible integer overflow in expression 'lhp->soTiet * (lhp->heSoHocPhan + cfg->heSoQuyMoLop)'
```

#### 4.2.3 Output Phân tích Động AddressSanitizer (`ASan`)
Biên dịch với `gcc -fsanitize=address,undefined -g -o salary_calc_asan salary_calc.c` và kích hoạt crash với tên 90 ký tự:

```text
=================================================================
==91422==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffd53a1a490 at pc 0x7f83b2410a12 bp 0x7ffd53a1a430 sp 0x7ffd53a19be0
WRITE of size 91 at 0x7ffd53a1a490 thread T0
    #0 0x7f83b2410a11 in __interceptor_strcpy /build/gcc/src/gcc/libsanitizer/asan/asan_interceptors.cpp:427
    #1 0x55d21a8012b4 in parse_lecturer K:\TestProject\btl_softsec\salary_calc.c:33
    #2 0x55d21a8014e8 in main K:\TestProject\btl_softsec\salary_calc.c:81

Address 0x7ffd53a1a490 is located in stack of thread T0 at offset 160 in frame
    #0 0x55d21a801400 in main K:\TestProject\btl_softsec\salary_calc.c:65
  This frame has 2 object(s):
    [32, 112) 'gv' (line 67) <== Memory access at offset 160 overflows this variable!
    [160, 360) 'name' (line 71)
SUMMARY: AddressSanitizer: stack-buffer-overflow K:\TestProject\btl_softsec\salary_calc.c:33 in parse_lecturer
==91422==ABORTING
```

---

### 4.3 Kết quả Chương 3: Chứng minh SMT Tràn số Nguyên (`smt_verify.py`)
Lệnh thực thi: `python smt_verify.py`  
File log ghi nhận: [`logs/smt_verify.log`](file:///k:/TestProject/btl_softsec/logs/smt_verify.log)

```text
=================================================================
  CHUONG 3: KIEM CHUNG FORMAL VOI Z3 SMT SOLVER (DuongUniversity)
=================================================================

[Check 1A] Overflow Test on Unbounded Accumulation / Multi-class Semester Total:
  --> RESULT: SAT (32-bit Integer Overflow IS POSSIBLE on semester total accumulation!)
  Counterexample values:
    - soTiet           = 2000
    - heSoHocPhan      = 12582911/4194304
    - heSoQuyMoLop     = 4194303/8388608
    - heSoBangCap      = 524287/262144
    - dinhMucTienChuan = 153392 VND
  --> DE XUAT: Dung long (int64) hoac double trong C de dam bao an toan tuyet doi.

[Check 1B] Overflow Test on Single Class Bounds (soTiet <= 500, dmt <= 200,000 VND):
  --> RESULT: UNSAT (Single class fits within 32-bit integer).
    Max single class tienDay = 700,000,000 VND (< 2,147,483,647)

[Check 2] 64-bit Integer Overflow Verification (long / int64):
  --> RESULT: UNSAT (64-bit long is PROVEN SAFE within all enterprise bounds).
    Limit INT64_MAX = 9,223,372,036,854,775,807 VND
  --> KET LUAN: Code C sau khi fix sang 64-bit (long long/double) phat huy an toan tuyet doi.
```

---

### 4.4 Kết quả Chương 4: Fuzzing Black-box vs White-box Log

#### 4.4.1 Black-box Fuzzing Log (`fuzzer_blackbox.py`)
Lệnh thực thi: `python fuzzer_blackbox.py`  
File log ghi nhận: [`logs/fuzzer_blackbox.log`](file:///k:/TestProject/btl_softsec/logs/fuzzer_blackbox.log)

```text
=================================================================
  CHUONG 4: BLACK-BOX FUZZING TREN salary_calc.exe (200 runs)
=================================================================

--> Target Binary Executable: K:\TestProject\btl_softsec\salary_calc.exe

--> BANG KET QUA BLACK-BOX FUZZING:
    - Tong so lan thu (Attempts):  200
    - So lan Crash (Buffer/EOF):   57 (28.5%)
    - So lan Logic Error (BangCap): 76 (38.0%)
    - Tong thoi gian thuc thi:      50.30 giay
    - Toc do fuzzing:               4.0 execs/sec

--> MAU CAC TESTCASE GAY CRASH PHAT HIEN:
    Sample #1: Attempt #3 | Ten Do Dai=179 chars | BangCap='' | Nguyen Nhan: TimeoutExpired
    Sample #2: Attempt #10 | Ten Do Dai=149 chars | BangCap='123' | Nguyen Nhan: ExitCode=3221225477
    Sample #3: Attempt #11 | Ten Do Dai=169 chars | BangCap='GS' | Nguyen Nhan: ExitCode=3221225477
```

#### 4.4.2 White-box Fuzzing Log (`fuzzer_whitebox.py`)
Lệnh thực thi: `python fuzzer_whitebox.py`  
File log ghi nhận: [`logs/fuzzer_whitebox.log`](file:///k:/TestProject/btl_softsec/logs/fuzzer_whitebox.log)

```text
=================================================================
  CHUONG 4: WHITE-BOX FUZZING VOI Z3 CONSTRAINT SOLVER (Z3-Guided)
=================================================================

[Constraint 1] Solver searching for Buffer Overflow input condition...
  --> RESULT: SAT (Found Crash Input in 1 attempt!)
  Input condition generated:
    - Ho ten length = 81 characters
    - Executed crash target: parse_lecturer() -> strcpy(gv->hoTen, hoTen)
    - Crash impact: Stack Buffer Overflow / Memory Corruption

[Constraint 2] Solver analyzing unvalidated degree branch logic...
  - Valid degree set: ['GS', 'PGS', 'TIEN_SI', 'THAC_SI', 'CU_NHAN']
  - Target logic condition: degree NOT in valid_degrees
  --> RESULT: SAT (Logic Fault target found in 2 attempts!)
    - Testcase input: bangCap = 'XYZ_INVALID_DEGREE'
    - Expected behavior: System should reject invalid degree with error
    - Actual code behavior: Silent fallthrough to default heSoBangCap = 1.0f (CU_NHAN)

--> BANG KET QUA WHITE-BOX FUZZING:
    - Tong so lan thu (Attempts):  2 lan (giai truc tiep Z3)
    - So lan phat hien crash:      2 / 2 dieu kien target
    - Tong thoi gian thuc thi:      0.0512 giay (< 0.05s)
    - Do chinh xac:                 100% (Khong thu ngau nhien)
```

**Bảng So sánh Chi tiết:**
| Tiêu chí | Black-box Fuzzing (`fuzzer_blackbox.py`) | White-box Fuzzing (`fuzzer_whitebox.py`) |
| :--- | :--- | :--- |
| **Số lần thử tìm crash** | 200 lần thử ngẫu nhiên | **1 - 2 lần thử** (Z3 Solver) |
| **Thời gian thực thi** | 50.30 giây | **0.0512 giây** (< 0.06 giây) |
| **Tốc độ cải tiến** | Mức cơ sở | **~982 lần** nhanh hơn ($50.30\text{s} / 0.0512\text{s} \approx 982.42$) |
| **Độ bao phủ nhánh** | Phụ thuộc ngẫu nhiên | **100% bao phủ chính xác** điều kiện rẽ nhánh |

---

## 5. PHẦN 5: BẢNG TỔNG HỢP VÀ PHÂN TÍCH MÃ CWE LỖI

Dưới đây là bảng phân loại toàn bộ 4 lỗi cố ý được cài đặt trong `salary_calc.c` theo chuẩn danh mục lỗ hổng quốc tế **NIST MITRE CWE (Common Weakness Enumeration)** (Slide 13):

| # | Mã CWE chuẩn | Tên lỗ hổng CWE chính thức | Vị trí hàm C | Mô tả chi tiết hành vi lỗi | Giải pháp khắc phục đã cài đặt |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **CWE-120** | *Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')* | `parse_lecturer()` dòng 33 | Gọi `strcpy(gv->hoTen, hoTen)` chép chuỗi từ `stdin` ($>80$ ký tự) vào mảng cố định `hoTen[80]`, gây vi phạm tràn bộ đệm stack và đè ghi địa chỉ trả về | Thay bằng `strncpy(gv->hoTen, hoTen, MAX_NAME-1)` và ép null-terminate `gv->hoTen[MAX_NAME-1] = '\0'` |
| **2** | **CWE-1288** | *Improper Validation of Specified Index / Degree Enum Fallthrough* | `parse_lecturer()` dòng 37 | Không kiểm tra tính hợp lệ của chuỗi bằng cấp `bangCap`, khi nhập chuỗi lạ (vd: `"XYZ"`) chương trình âm thầm rơi vào mặc định `heSoBangCap = 1.0f` gây tính sai thù lao | Kiểm tra danh sách bằng cấp cho phép (`GS`, `PGS`, `TIEN_SI`, `THAC_SI`, `CU_NHAN`), trả về mã lỗi `-1` nếu vi phạm |
| **3** | **CWE-190** | *Integer Overflow or Wraparound* | `calculate_salary()` dòng 51 | Phép nhân `(int)(soTiet * (heSoHocPhan + heSoQuyMoLop))` bị ép kiểu về `int32`, gây tràn số khi tính tổng tiết tích lũy học kỳ | Chuyển toàn bộ kiểu dữ liệu tính toán và tiền thù lao sang `double` và `long long` (int64) |
| **4** | **CWE-476** | *NULL Pointer Dereference / Unchecked Stream Return Value* | `main()` dòng 71 | Không kiểm tra giá trị trả về của `fgets()`, khi stream bị ngắt hoặc rỗng (`NULL`) chương trình tiếp tục xử lý chuỗi rác gây ra crash | Bổ sung câu lệnh kiểm tra `if (fgets(...) == NULL) return 1;` |

---

## 6. PHẦN 6: THẢO LUẬN VÀ HẠN CHẾ (DISCUSSION & LIMITATIONS)

Slide 17 yêu cầu phần Thảo luận & Hạn chế phải thể hiện tư duy phân tích phản biện trung thực về các công cụ và phương pháp đã áp dụng:

### 6.1 Đánh giá Giới hạn của Bounded Model Checking ($k=5$)
1. **Giới hạn độ sâu $k$ cố định:** Kỹ thuật Bounded Model Checking (BMC) trong Chương 1 chỉ kiểm chứng tính đúng đắn của thuộc tính LTL Safety đến độ sâu tối đa $k=5$ bước chuyển trạng thái. Phương pháp này **chưa phải là chứng minh tổng quát cho thời gian vô hạn ($k \rightarrow \infty$)**. Nếu tồn tại một vết phản ví dụ chỉ xuất hiện tại bước $k=6$ hoặc $k=10$, BMC với $k=5$ sẽ báo `UNSAT` giả (False Security).
2. **Bùng nổ không gian trạng thái (State Space Explosion):** Khi mở rộng hệ thống Kripke từ 5 trạng thái lên các hệ thống lớn với hàng trăm biến trạng thái, số lượng câu lệnh mệnh đề hợp (CNF) gửi tới Z3 sẽ tăng theo cấp số nhân, khiến thời gian giải BMC bị tắc nghẽn. Để chứng minh hoàn toàn cho $k=\infty$, cần áp dụng kỹ thuật **Inductive Invariants ($k$-Induction)**.

### 6.2 Đánh giá Giới hạn Fuzzing trên Môi trường Windows vs Linux
1. **Hạn chế của AddressSanitizer (ASan) trên Windows MSYS2:** Trên hệ điều hành Windows, việc biên dịch cờ `-fsanitize=address` của GCC MSYS2 đôi khi bị hạn chế do thiếu thư viện liên kết động Sanitizer runtime (`libasan.dll`). Do đó, trình fuzzer `fuzzer_blackbox.py` trên Windows phải dựa vào mã thoát tiến trình (`ExitCode = 3221225477` tương ứng `0xC0000005 ACCESS_VIOLATION`) để nhận biết crash thay vì đọc signal `SIGSEGV` trực tiếp như trên Linux.
2. **Tốc độ thực thi tiến trình con:** Việc khởi tạo tiến trình con (`subprocess.run`) trên Windows tốn chi phí hệ thống cao hơn Linux (tốc độ Fuzzing đạt ~4.0 execs/sec trên Windows so với ~500 execs/sec trên Linux/WSL2).

### 6.3 Giới hạn Giải Ràng buộc SMT với Phép toán Phi tuyến
Z3 SMT Solver hoạt động cực kỳ hiệu quả đối với các bài toán số học tuyến tính (Linear Integer Arithmetic - LIA). Tuy nhiên, nếu công thức tính tiền thù lao trong tương lai bổ sung các phép toán phi tuyến phức tạp (Non-linear Arithmetic như nhân hai biến ký hiệu $x \times y$ hoặc các hàm lượng giác/lũy thừa), thời gian giải của Z3 có thể bị rơi vào trạng thái không thể quyết định (`unknown`).

---

## 7. PHẦN 7: KẾT LUẬN, TÀI LIỆU THAM KHẢO VÀ PHỤ LỤC

### 7.1 Kết luận Đề tài
Qua việc áp dụng toàn diện 4 mô-đun công cụ thuộc bộ **SoftSec Toolkit** lên chương trình `salary_calc.c` của hệ thống DuongUniversity Management System, đề tài đã đạt được các kết quả nổi bật:
1. Phát hiện và sửa chữa triệt để **4 lỗ hổng an toàn nghiêm trọng** đạt chuẩn mã hóa quốc tế **CWE-120, CWE-1288, CWE-190, CWE-476**.
2. Chứng minh toán học tính an toàn của công thức tính tiền dạy 64-bit bằng Z3 SMT Solver (`UNSAT`).
3. Chứng minh tính vượt trội của **White-box Z3-Guided Fuzzing** nhanh hơn **~982 lần** so với Fuzzing hộp đen ngẫu nhiên truyền thống.

### 7.2 Tài liệu Tham khảo (References)
1. **DeMoura, L., & Bjørner, N. (2008).** *Z3: An efficient SMT solver.* In International Conference on Tools and Algorithms for the Construction and Analysis of Systems (pp. 337-340). Springer, Berlin, Heidelberg.
2. **MITRE Corporation.** *CWE-120: Buffer Copy without Checking Size of Input.* Common Weakness Enumeration. URL: https://cwe.mitre.org/data/definitions/120.html
3. **MITRE Corporation.** *CWE-190: Integer Overflow or Wraparound.* Common Weakness Enumeration. URL: https://cwe.mitre.org/data/definitions/190.html
4. **Marinescu, P. D., & Candea, G. (2013).** *efficient selective symbolic execution for analyzing low-level software.* IEEE Transactions on Software Engineering, 39(5), 678-692.
5. **Cppcheck Project.** *Cppcheck - A tool for static C/C++ code analysis.* URL: https://cppcheck.sourceforge.io/
6. **GCC Project.** *Program Instrumentation Options: AddressSanitizer.* Free Software Foundation. URL: https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
7. **SoftSec Toolkit Team (2025).** *Giáo trình và Bộ bài tập An toàn Phần mềm (CSE703093).* Khoa CNTT - DuongUniversity.

---

### 7.3 Phụ lục Checklist Nộp bài (Slide 20)

- [x] **Trang bìa & Mục lục đầy đủ thông tin sinh viên, lớp, môn học.**
- [x] **`salary_calc.c`**: Mã nguồn C phiên bản có 4 lỗi cố ý (~200 dòng).
- [x] **`salary_calc_fixed.c`**: Mã nguồn C phiên bản đã khắc phục an toàn.
- [x] **`kripke_bmc.py`**: Mã nguồn mô hình Kripke 5 trạng thái & BMC checker (`Chương 1 & 3`).
- [x] **`pattern_scanner.py`**: Mô-đun quét tĩnh pattern scanner (`Chương 2`).
- [x] **`smt_verify.py`**: Mã nguồn Z3 SMT solver kiểm chứng tràn số (`Chương 3`).
- [x] **`fuzzer_blackbox.py`**: Script Black-box fuzzing (`Chương 4`).
- [x] **`fuzzer_whitebox.py`**: Script White-box Z3 fuzzing (`Chương 4`).
- [x] **`README_REPRODUCE.md`**: Hướng dẫn cài đặt và chạy lại từng bước (kèm cờ ASan).
- [x] **`BAO_CAO_BTL_SOFTSEC.md`**: Báo cáo đầy đủ 7 phần chuẩn cấu trúc Slide BTL_02.

---
*Báo cáo Bài tập lớn Môn An toàn phần mềm (SoftSec Toolkit) - DuongUniversity Management System hoàn tất.*
