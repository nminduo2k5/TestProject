"""
fuzzer_blackbox.py - Black-box Fuzzing cho DuongUniversity Salary Calc
Tự động lưu nhật ký thực thi vào logs/fuzzer_blackbox.log
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


def random_name(length):
    chars = string.ascii_letters + string.digits + ' _-@!#'
    return ''.join(random.choices(chars, k=length))


def random_bangcap():
    valid = ['GS', 'PGS', 'TIEN_SI', 'THAC_SI', 'CU_NHAN']
    invalid = ['XYZ', 'INVALID_DEGREE', 'A' * 30, '123', '', 'HACKER']
    return random.choice(valid + invalid)


def run_blackbox_fuzzing(num_iterations=200):
    print("=================================================================")
    print(f"  CHUONG 4: BLACK-BOX FUZZING TREN salary_calc.exe ({num_iterations} runs)")
    print("=================================================================\n")

    exe_path = os.path.join(os.path.dirname(__file__), "salary_calc.exe")
    if not os.path.exists(exe_path):
        exe_path = "salary_calc.exe"

    print(f"--> Target Binary Executable: {exe_path}")

    crashes = 0
    logic_errors = 0
    attempts = 0
    start_time = time.time()

    crash_samples = []

    for _ in range(num_iterations):
        attempts += 1

        name_len = random.randint(5, 180)
        name_input = random_name(name_len)
        bangcap_input = random_bangcap()

        input_bytes = f"{name_input}\n{bangcap_input}\n".encode('utf-8')

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
                    crash_samples.append((attempts, name_len, bangcap_input, f"ExitCode={res.returncode}"))
            elif bangcap_input not in ['GS', 'PGS', 'TIEN_SI', 'THAC_SI', 'CU_NHAN']:
                logic_errors += 1

        except subprocess.TimeoutExpired:
            crashes += 1
            if len(crash_samples) < 3:
                crash_samples.append((attempts, name_len, bangcap_input, "TimeoutExpired"))

    elapsed = time.time() - start_time

    print(f"\n--> BANG KET QUA BLACK-BOX FUZZING:")
    print(f"    - Tong so lan thu (Attempts):  {attempts}")
    print(f"    - So lan Crash (Buffer/EOF):   {crashes}")
    print(f"    - So lan Logic Error (BangCap): {logic_errors}")
    print(f"    - Tong thoi gian thuc thi:      {elapsed:.2f} giay")
    if elapsed > 0:
        print(f"    - Toc do fuzzing:               {attempts / elapsed:.1f} execs/sec\n")

    if crash_samples:
        print("--> MAU CAC TESTCASE GAY CRASH PHAT HIEN:")
        for idx, (att, nlen, cap, reason) in enumerate(crash_samples, 1):
            print(f"    Sample #{idx}: Attempt #{att} | Ten Do Dai={nlen} chars | BangCap='{cap}' | Nguyen Nhan: {reason}")
    print()


if __name__ == '__main__':
    log_file = os.path.join(os.path.dirname(__file__), "logs", "fuzzer_blackbox.log")
    sys.stdout = TeeLogger(log_file)
    run_blackbox_fuzzing(200)
