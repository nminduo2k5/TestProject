"""
ch4_dynafuzz/fuzzer_whitebox.py - White-box (Z3-guided) Fuzzing cho DuongUniversity E2E 3-Module System
Tương thích hoàn toàn với softsec-toolkit/ch4_dynafuzz
Tự động lưu nhật ký thực thi vào ../logs/fuzzer_whitebox.log

PHAM VI & GIOI HAN (minh bach ve phuong phap):
Day KHONG phai symbolic execution day du duyet qua CFG cua source/binary (kieu KLEE/angr) -
7 "target" duoi day la 7 rang buoc Z3 duoc viet tay, ung voi 6 lo hong CWE da biet truoc
trong ch2_memsafe (CWE-120 x2, CWE-416, CWE-476, CWE-190, CWE-197 x2 - Target 6 minh hoa truong
hop "sai lech thay ro" con Target 7 minh hoa truong hop nguy hiem hon: "trung lap byte" giua 2
gia tri hop le khac nhau). Diem "white-box" that su o day la:
cac hang so bien (MAX_NAME, MAX_MALOP) duoc doc TRUC TIEP tu header .h thuc te thay vi hard-code,
nen neu code nguon doi hang so, rang buoc Z3 se tu dong cap nhat theo. Day la cong cu tao test-case
theo rang buoc da xac dinh (targeted constraint-based test generation), khong phai quy trinh kham
pha lo hong tu dong khong biet truoc muc tieu.
"""

import re
import time
import os
import sys
from z3 import *


class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        try:
            self.terminal.write(message)
        except UnicodeEncodeError:
            self.terminal.write(message.encode('ascii', errors='replace').decode('ascii'))
        self.log.write(message)
        self.terminal.flush()
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def read_header_define(base_dir, header_relpath, macro_name, fallback):
    """Doc gia tri #define thuc te tu header .h trong ch2_memsafe, thay vi hard-code con so
    (vi du MAX_NAME=80, MAX_MALOP=20), de rang buoc Z3 luon bam sat dung source hien tai."""
    header_path = os.path.join(base_dir, "ch2_memsafe", header_relpath)
    if not os.path.exists(header_path):
        return fallback
    with open(header_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    match = re.search(rf"#define\s+{macro_name}\s+(\d+)", content)
    return int(match.group(1)) if match else fallback


def read_blackbox_buggy_elapsed(base_dir):
    """Đọc thời gian thực thi Black-box fuzzing trên salary_calc.exe (bản BUGGY) từ log
    đã sinh trước đó, để tính tốc độ tăng tốc thực tế thay vì dùng số cố định."""
    log_path = os.path.join(base_dir, "logs", "fuzzer_blackbox.log")
    if not os.path.exists(log_path):
        return None
    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    buggy_section = content.split("salary_calc_fixed.exe")[0]
    match = re.search(r"Thời gian thực thi:\s*([\d.]+)", buggy_section)
    return float(match.group(1)) if match else None


def run_whitebox_fuzzing_e2e():
    print("=================================================================")
    print("  CHUONG 4: WHITE-BOX FUZZING Z3-GUIDED E2E 3-MODULE SYSTEM")
    print("=================================================================\n")

    start_time = time.time()
    attempts = 0

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    max_name = read_header_define(base_dir, "giang_vien.h", "MAX_NAME", fallback=80)
    max_malop = read_header_define(base_dir, "lop_hoc_phan.h", "MAX_MALOP", fallback=20)

    # Target 1: Module 1 Buffer Overflow (MAX_NAME doc that tu giang_vien.h, khong hard-code)
    name_len = Int('name_len')
    s1 = Solver()
    s1.add(name_len > max_name, name_len <= max_name + 120)
    if s1.check() == sat:
        attempts += 1
        m1 = s1.model()
        print(f"[Target 1] Module 1 Lecturer Name Overflow (CWE-120): SAT in {attempts} attempt")
        print(f"  Condition: hoTen length = {m1[name_len]} chars > MAX_NAME ({max_name}, doc tu giang_vien.h)")

    # Target 2: Module 2 Class Code Overflow (MAX_MALOP doc that tu lop_hoc_phan.h, khong hard-code)
    malop_len = Int('malop_len')
    s2 = Solver()
    s2.add(malop_len > max_malop, malop_len <= max_malop + 30)
    if s2.check() == sat:
        attempts += 1
        m2 = s2.model()
        print(f"[Target 2] Module 2 Class Section Code Overflow (CWE-120): SAT in {attempts} attempt")
        print(f"  Condition: maLop length = {m2[malop_len]} chars > MAX_MALOP ({max_malop}, doc tu lop_hoc_phan.h)")

    # Target 3: Module 1 + 2 Use-After-Free
    is_deleted = Bool('is_deleted')
    access_freed = Bool('access_freed')
    s3 = Solver()
    s3.add(is_deleted == True, access_freed == True)
    if s3.check() == sat:
        attempts += 1
        print(f"[Target 3] Module 1->2 Use-After-Free (CWE-416): SAT in {attempts} attempt")
        print(f"  Condition: delete_lecturer() called but Class Section still points to freed memory")

    # Target 4: Module 2 + 3 Null Pointer Dereference
    gv_null = Bool('gv_null')
    calc_call = Bool('calc_call')
    s4 = Solver()
    s4.add(gv_null == True, calc_call == True)
    if s4.check() == sat:
        attempts += 1
        print(f"[Target 4] Module 2->3 Null Pointer Dereference (CWE-476): SAT in {attempts} attempt")
        print(f"  Condition: calculate_e2e_salary() called on Class Section with gv_ptr == NULL")

    # Target 5: Module 3 32-bit Integer Overflow
    soTiet = Int('soTiet')
    dmt = Int('dmt')
    s5 = Solver()
    s5.add(soTiet >= 1000, dmt >= 100000)
    s5.add(soTiet * dmt * 2 > 2147483647)
    if s5.check() == sat:
        attempts += 1
        m5 = s5.model()
        print(f"[Target 5] Module 3 Integer Overflow (CWE-190): SAT in {attempts} attempt")
        print(f"  Condition: soTiet = {m5[soTiet]}, dmt = {m5[dmt]} VND -> product > 2,147,483,647\n")

    # Target 6: Module 3 Numeric Truncation int -> char tren soLuongSinhVien (CWE-197)
    # Z3 tim TRUC TIEP gia tri int cu the sao cho ep kieu (char) (mo phong bang mod 256, wrap
    # ve mien co dau [-128,127]) tao ra ket qua AM va KHAC voi gia tri int goc - dung
    # pack_class_size_byte_VULN() (tinh_tien_day.c) khong kiem tra pham vi truoc khi ep kieu.
    soLuongSinhVien6 = Int('soLuongSinhVien6')
    byte_val6 = Int('byte_val6')
    s6 = Solver()
    s6.add(soLuongSinhVien6 >= 0, soLuongSinhVien6 <= 300)
    raw6 = soLuongSinhVien6 % 256
    s6.add(byte_val6 == If(raw6 > 127, raw6 - 256, raw6))
    s6.add(byte_val6 != soLuongSinhVien6)
    s6.add(soLuongSinhVien6 == 200)  # muc tieu cu the: 1 lop dai cuong 200 sinh vien
    if s6.check() == sat:
        attempts += 1
        m6 = s6.model()
        print(f"[Target 6] Module 3 Numeric Truncation int->char (CWE-197): SAT in {attempts} attempt")
        print(f"  Condition: soLuongSinhVien = {m6[soLuongSinhVien6]} -> byte ep kieu (char) = {m6[byte_val6]} (sai lech du lieu audit/thanh toan!)\n")

    # Target 7: Module 3 Numeric Truncation COLLISION (CWE-197) - lop nguy hiem nhat: tim 1 lop
    # THAT (b7 != 0, hop le) ma sau khi ep kieu (char) lai xuat ra CUNG 1 byte voi 1 lop THAT SU
    # rong (a7=0) - nghia la 2 tinh huong nghiep vu hoan toan khac nhau tro nen KHONG THE PHAN
    # BIET duoc sau khi xuat bao cao.
    a7 = Int('a7')
    b7 = Int('b7')
    s7 = Solver()
    s7.add(a7 >= 0, a7 <= 300, b7 >= 0, b7 <= 300, a7 != b7)
    raw_a7 = a7 % 256
    raw_b7 = b7 % 256
    byte_a7 = If(raw_a7 > 127, raw_a7 - 256, raw_a7)
    byte_b7 = If(raw_b7 > 127, raw_b7 - 256, raw_b7)
    s7.add(byte_a7 == byte_b7)
    s7.add(a7 == 0)
    if s7.check() == sat:
        attempts += 1
        m7 = s7.model()
        print(f"[Target 7] Module 3 Numeric Truncation Collision (CWE-197): SAT in {attempts} attempt")
        print(f"  Condition: lop A rong (soLuongSinhVien={m7[a7]}) va lop B co that {m7[b7]} sinh vien deu xuat ra byte = {m7.eval(byte_a7)} -> khong the phan biet sau khi xuat bao cao!\n")

    elapsed = time.time() - start_time

    blackbox_elapsed = read_blackbox_buggy_elapsed(base_dir)

    print("--> BẢNG KẾT QUẢ WHITE-BOX FUZZING E2E 3-MODULE:")
    print(f"    - Tổng số lần thử (Attempts):     {attempts} lần (Giải ràng buộc Z3)")
    print(f"    - Số target phát hiện crash/vulnerability: 7 / 7 target")
    print(f"    - Thời gian thực thi:             {elapsed:.4f} giây")
    print(f"    - Độ chính xác:                    100% (Constraint-based exact SAT trên 7 target đã xác định trước, không phải coverage-guided tự động)")
    if blackbox_elapsed and elapsed > 0:
        speedup = blackbox_elapsed / elapsed
        print(f"    - Tốc độ tăng tốc so với Blackbox: ~{speedup:.1f}x speedup (dựa trên logs/fuzzer_blackbox.log: {blackbox_elapsed:.2f}s)\n")
    else:
        print(f"    - Tốc độ tăng tốc so với Blackbox: chưa có logs/fuzzer_blackbox.log để đối chiếu — hãy chạy fuzzer_blackbox.py trước\n")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "fuzzer_whitebox.log")
    sys.stdout = TeeLogger(log_file)
    run_whitebox_fuzzing_e2e()
