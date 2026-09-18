"""
ch4_dynafuzz/fuzzer_blackbox.py - Black-box Fuzzing cho DuongUniversity E2E 3-Module System
Tương thích hoàn toàn với softsec-toolkit/ch4_dynafuzz
Tự động lưu nhật ký thực thi vào ../logs/fuzzer_blackbox.log
"""

import subprocess
import random
import re
import string
import time
import os
import sys


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


def random_string(length):
    chars = string.ascii_letters + string.digits + ' _-@!#'
    return ''.join(random.choices(chars, k=length))


def random_bangcap():
    valid = ['GS', 'PGS', 'TIEN_SI', 'THAC_SI', 'CU_NHAN']
    invalid = ['XYZ', 'INVALID_DEGREE', 'A' * 30, '123', '', 'HACKER']
    return random.choice(valid + invalid)


def run_blackbox_fuzzing(exe_name, num_iterations=200):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exe_path = os.path.join(base_dir, "ch2_memsafe", exe_name)
    if not os.path.exists(exe_path):
        exe_path = os.path.join(base_dir, exe_name)
    if not os.path.exists(exe_path):
        exe_path = exe_name

    print(f"\n=================================================================")
    print(f"  BLACK-BOX FUZZING TREN {exe_name} ({num_iterations} runs)")
    print("=================================================================")
    print(f"--> Target Binary Executable: {exe_path}")

    crashes = 0
    logic_errors = 0
    attempts = 0
    start_time = time.time()
    crash_samples = []

    for _ in range(num_iterations):
        attempts += 1

        name_len = random.randint(5, 180)
        malop_len = random.randint(2, 50)
        name_input = random_string(name_len)
        bangcap_input = random_bangcap()
        malop_input = random_string(malop_len)

        # Multi-module 3 input lines: Mod 1 Name, Mod 1 Degree, Mod 2 Class Code
        input_bytes = f"{name_input}\n{bangcap_input}\n{malop_input}\n".encode('utf-8')

        try:
            res = subprocess.run(
                [exe_path],
                input=input_bytes,
                capture_output=True,
                timeout=1
            )

            if res.returncode != 0:
                crashes += 1
                if len(crash_samples) < 3:
                    crash_samples.append((attempts, name_len, malop_len, bangcap_input, f"ExitCode={res.returncode}"))
            elif bangcap_input not in ['GS', 'PGS', 'TIEN_SI', 'THAC_SI', 'CU_NHAN']:
                logic_errors += 1

        except subprocess.TimeoutExpired:
            crashes += 1
            if len(crash_samples) < 3:
                crash_samples.append((attempts, name_len, malop_len, bangcap_input, "TimeoutExpired"))

    elapsed = time.time() - start_time

    print(f"\n--> KẾT QUẢ BLACK-BOX FUZZING TREN {exe_name}:")
    print(f"    - Tổng số lần thử (Attempts):   {attempts}")
    print(f"    - Số lần Crash (Buffer Overflow): {crashes}")
    print(f"    - Số lần Logic Error (Bằng cấp):  {logic_errors}")
    print(f"    - Thời gian thực thi:            {elapsed:.2f} giây")
    if elapsed > 0:
        print(f"    - Tốc độ fuzzing:                 {attempts / elapsed:.1f} execs/sec")

    if crash_samples:
        print("--> MẪU TESTCASE GÂY CRASH PHÁT HIỆN:")
        for idx, (att, nlen, mlen, cap, reason) in enumerate(crash_samples, 1):
            print(f"    Sample #{idx}: Attempt #{att} | TenLen={nlen} | LopLen={mlen} | BangCap='{cap}' | Reason: {reason}")
    print()


def run_blackbox_fuzzing_truncation(exe_name, num_iterations=200):
    """Black-box fuzzing rieng cho lo hong CWE-197 (Numeric Truncation int->char): goi truc
    tiep subcommand `e2e_byte_truncate <soLuongSinhVien>` (khong qua stdin nhu cac test khac)
    voi soLuongSinhVien ngau nhien, bao gom ca gia tri ngoai pham vi char [0,127], roi doc
    stdout that de dem so lan xay ra sai lech du lieu ([TRUNCATION DETECTED]) hoac bi chan
    an toan ([SAFE BLOCKED]) - khong doan so lieu, hoan toan tu ket qua thuc thi that."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exe_path = os.path.join(base_dir, "ch2_memsafe", exe_name)
    if not os.path.exists(exe_path):
        exe_path = exe_name

    print(f"\n=================================================================")
    print(f"  BLACK-BOX FUZZING (CWE-197 Numeric Truncation) TREN {exe_name} ({num_iterations} runs)")
    print("=================================================================")
    print(f"--> Target Binary Executable: {exe_path} e2e_byte_truncate <soLuongSinhVien>")

    truncation_detected = 0
    safe_blocked = 0
    normal = 0
    crashes = 0
    attempts = 0
    start_time = time.time()
    truncation_samples = []

    for _ in range(num_iterations):
        attempts += 1
        # Pham vi rong: bao gom ca gia tri am, hop le (0..127), va vuot xa 127 (lop dai cuong)
        so_luong = random.randint(-50, 400)

        try:
            res = subprocess.run(
                [exe_path, "e2e_byte_truncate", str(so_luong)],
                capture_output=True,
                timeout=1,
                text=True
            )
            out = res.stdout

            if res.returncode != 0:
                crashes += 1
            elif "[TRUNCATION DETECTED]" in out:
                truncation_detected += 1
                if len(truncation_samples) < 3:
                    truncation_samples.append(so_luong)
            elif "[SAFE BLOCKED]" in out:
                safe_blocked += 1
            else:
                normal += 1

        except subprocess.TimeoutExpired:
            crashes += 1

    elapsed = time.time() - start_time

    print(f"\n--> KẾT QUẢ BLACK-BOX FUZZING (CWE-197) TREN {exe_name}:")
    print(f"    - Tổng số lần thử (Attempts):        {attempts}")
    print(f"    - Số lần SAI LỆCH DỮ LIỆU (Truncation): {truncation_detected}")
    print(f"    - Số lần bị CHẶN AN TOÀN (Safe Blocked): {safe_blocked}")
    print(f"    - Số lần dữ liệu hợp lệ (Normal):     {normal}")
    print(f"    - Số lần Crash:                       {crashes}")
    print(f"    - Thời gian thực thi:                 {elapsed:.2f} giây")
    if truncation_samples:
        print(f"    - Mẫu soLuongSinhVien gây sai lệch: {truncation_samples}")
    print()


# Bo gia tri bien (Boundary Value Analysis) THIET KE SAN cho pham vi soLuongSinhVien -> char,
# thay vi cho random.randint() may rui trung: bao gom ca 2 canh cua moi mep chu ky 256
# (-256/-255, -129/-128/-127, 126/127/128/129, 255/256/257) va vai gia tri "lop dai cuong"
# thuc te (300, 384) - dam bao LUON kiem tra dung cac diem chet nguoi (dac biet la cac diem
# TRUNG LAP byte voi 1 gia tri hop le KHAC), khong phu thuoc may man cua random.
BVA_SO_LUONG_SINH_VIEN = [-256, -255, -129, -128, -127, -1, 0, 1, 126, 127, 128, 129, 255, 256, 257, 300, 384]


def _expected_byte(n):
    """Mo phong (char) cast bang so hoc modulo 256 + wrap dau, DUNG cong thuc da dung trong
    smt_verify.py Check 4/5/6 - de doi chieu voi byte THAT do chinh binary in ra."""
    raw = n % 256
    return raw - 256 if raw > 127 else raw


def run_bva_truncation_test(exe_name):
    """Chay DUNG BVA_SO_LUONG_SINH_VIEN (khong ngau nhien) tren binary that, doc byte THAT tu
    stdout, roi gom nhom theo byte ket qua de lo ra cac CAP GIA TRI TRUNG LAP (vd 0 va 256 cung
    cho byte=0) - lop nguy hiem nhat cua CWE-197 vi No khong bieu hien bang crash hay so am ma
    bang viec 1 gia tri hop le "gia mao" 1 gia tri hop le khac."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exe_path = os.path.join(base_dir, "ch2_memsafe", exe_name)
    if not os.path.exists(exe_path):
        exe_path = exe_name

    print(f"\n=================================================================")
    print(f"  BOUNDARY VALUE ANALYSIS (CWE-197) TREN {exe_name} ({len(BVA_SO_LUONG_SINH_VIEN)} gia tri bien co dinh)")
    print("=================================================================")

    byte_to_inputs = {}
    for n in BVA_SO_LUONG_SINH_VIEN:
        expected = _expected_byte(n)
        try:
            res = subprocess.run(
                [exe_path, "e2e_byte_truncate", str(n)],
                capture_output=True, timeout=1, text=True
            )
            out = res.stdout
            m = re.search(r"Byte da ep kieu \(char\) = (-?\d+)", out)
            actual_byte = int(m.group(1)) if m else None
            if "[SAFE BLOCKED]" in out:
                status = "SAFE_BLOCKED"
            elif "[TRUNCATION DETECTED]" in out:
                status = "TRUNCATED"
            else:
                status = "OK"
            match_mark = "OK" if (actual_byte is None or actual_byte == expected) else "MISMATCH!"
            print(f"    n={n:>5}  ->  status={status:<12} byte_that={str(actual_byte):>5}  byte_du_kien={expected:>5}  [{match_mark}]")
            if actual_byte is not None:
                byte_to_inputs.setdefault(actual_byte, []).append(n)
        except subprocess.TimeoutExpired:
            print(f"    n={n:>5}  ->  TIMEOUT/CRASH")

    collisions = {b: ns for b, ns in byte_to_inputs.items() if len(ns) > 1}
    print(f"\n--> PHAT HIEN TRUNG LAP BYTE (nhieu soLuongSinhVien HOP LE KHAC NHAU cho CUNG 1 byte):")
    if collisions:
        for b, ns in sorted(collisions.items()):
            print(f"    byte={b}  <-  cac gia tri soLuongSinhVien: {sorted(ns)}  (KHONG THE PHAN BIET duoc sau khi xuat bao cao!)")
    else:
        print(f"    Khong co trung lap nao (binary nay chan/tu choi truoc khi ep kieu sai lech).")
    print()


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "fuzzer_blackbox.log")
    sys.stdout = TeeLogger(log_file)
    print("=================================================================")
    print("  CHUONG 4: BLACK-BOX FUZZING E2E 3-MODULE SYSTEM")
    print("=================================================================")
    run_blackbox_fuzzing("salary_calc.exe", 200)
    run_blackbox_fuzzing("salary_calc_fixed.exe", 200)
    run_blackbox_fuzzing_truncation("salary_calc.exe", 200)
    run_blackbox_fuzzing_truncation("salary_calc_fixed.exe", 200)
    run_bva_truncation_test("salary_calc.exe")
    run_bva_truncation_test("salary_calc_fixed.exe")
