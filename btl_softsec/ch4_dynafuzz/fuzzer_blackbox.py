"""
ch4_dynafuzz/fuzzer_blackbox.py - Black-box Fuzzing cho DuongUniversity E2E 3-Module System
Tương thích hoàn toàn với softsec-toolkit/ch4_dynafuzz
Tự động lưu nhật ký thực thi vào ../logs/fuzzer_blackbox.log
"""

import subprocess
import random
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


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "fuzzer_blackbox.log")
    sys.stdout = TeeLogger(log_file)
    print("=================================================================")
    print("  CHUONG 4: BLACK-BOX FUZZING E2E 3-MODULE SYSTEM")
    print("=================================================================")
    run_blackbox_fuzzing("salary_calc.exe", 200)
    run_blackbox_fuzzing("salary_calc_fixed.exe", 200)
