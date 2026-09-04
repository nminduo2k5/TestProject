"""
smt_verify.py - Formal Verification of Salary Calculation using Z3 SMT Solver
Tự động lưu nhật ký thực thi vào logs/smt_verify.log
"""

import sys
import os
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


def run_smt_verification():
    print("=================================================================")
    print("  CHUONG 3: KIEM CHUNG FORMAL VOI Z3 SMT SOLVER (DuongUniversity)")
    print("=================================================================\n")

    soTiet       = Int('soTiet')
    heSoHocPhan  = Real('heSoHocPhan')
    heSoQuyMoLop = Real('heSoQuyMoLop')
    heSoBangCap  = Real('heSoBangCap')
    dmt          = Int('dmt')

    INT32_MAX = 2**31 - 1
    INT64_MAX = 2**63 - 1

    print("[Check 1A] Overflow Test on Unbounded Accumulation / Multi-class Semester Total:")
    s_unbound = Solver()
    s_unbound.add(soTiet >= 1, soTiet <= 2000)
    s_unbound.add(heSoHocPhan >= 0.5, heSoHocPhan <= 3.0)
    s_unbound.add(heSoQuyMoLop >= 0.1, heSoQuyMoLop <= 0.5)
    s_unbound.add(heSoBangCap >= 1.0, heSoBangCap <= 2.0)
    s_unbound.add(dmt >= 50000, dmt <= 500000)

    soTietQuyDoi_a = soTiet * (heSoHocPhan + heSoQuyMoLop)
    tienDay_a = soTietQuyDoi_a * heSoBangCap * dmt

    s_unbound.add(tienDay_a > INT32_MAX)
    res_a = s_unbound.check()

    if res_a == sat:
        print("  --> RESULT: SAT (32-bit Integer Overflow IS POSSIBLE on semester total accumulation!)")
        m = s_unbound.model()
        print("  Counterexample values:")
        print(f"    - soTiet           = {m[soTiet]}")
        print(f"    - heSoHocPhan      = {m[heSoHocPhan]}")
        print(f"    - heSoQuyMoLop     = {m[heSoQuyMoLop]}")
        print(f"    - heSoBangCap      = {m[heSoBangCap]}")
        print(f"    - dinhMucTienChuan = {m[dmt]} VND")
        print("  --> DE XUAT: Dung long (int64) hoac double trong C de dam bao an toan tuyet doi.\n")
    else:
        print("  --> RESULT: UNSAT\n")

    print("[Check 1B] Overflow Test on Single Class Bounds (soTiet <= 500, dmt <= 200,000 VND):")
    s_bound = Solver()
    s_bound.add(soTiet >= 1,       soTiet <= 500)
    s_bound.add(heSoHocPhan >= 0.5, heSoHocPhan <= 3.0)
    s_bound.add(heSoQuyMoLop >= 0.1, heSoQuyMoLop <= 0.5)
    s_bound.add(heSoBangCap >= 1.0,  heSoBangCap <= 2.0)
    s_bound.add(dmt >= 50000,      dmt <= 200000)

    soTietQuyDoi_b = soTiet * (heSoHocPhan + heSoQuyMoLop)
    tienDay_b = soTietQuyDoi_b * heSoBangCap * dmt

    s_bound.add(tienDay_b > INT32_MAX)
    res_b = s_bound.check()

    if res_b == sat:
        print("  --> RESULT: SAT")
    else:
        print("  --> RESULT: UNSAT (Single class fits within 32-bit integer).")
        max_single = 500 * (3.0 + 0.5) * 2.0 * 200000
        print(f"    Max single class tienDay = {int(max_single):,} VND (< 2,147,483,647)\n")

    print("[Check 2] 64-bit Integer Overflow Verification (long / int64):")
    s_64 = Solver()
    s_64.add(soTiet >= 1, soTiet <= 5000)
    s_64.add(heSoHocPhan >= 0.5, heSoHocPhan <= 5.0)
    s_64.add(heSoQuyMoLop >= 0.1, heSoQuyMoLop <= 2.0)
    s_64.add(heSoBangCap >= 1.0, heSoBangCap <= 3.0)
    s_64.add(dmt >= 50000, dmt <= 2000000)

    soTietQuyDoi_64 = soTiet * (heSoHocPhan + heSoQuyMoLop)
    tienDay_64 = soTietQuyDoi_64 * heSoBangCap * dmt

    s_64.add(tienDay_64 > INT64_MAX)
    res_64 = s_64.check()

    if res_64 == sat:
        print("  --> RESULT: SAT")
    else:
        print("  --> RESULT: UNSAT (64-bit long is PROVEN SAFE within all enterprise bounds).")
        print(f"    Limit INT64_MAX = {INT64_MAX:,} VND")
        print("  --> KET LUAN: Code C sau khi fix sang 64-bit (long long/double) phat huy an toan tuyet doi.\n")


if __name__ == '__main__':
    log_file = os.path.join(os.path.dirname(__file__), "logs", "smt_verify.log")
    sys.stdout = TeeLogger(log_file)
    run_smt_verification()
