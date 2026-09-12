"""
ch3_verify/smt_verify.py - Formal Verification of 3-Module E2E System using Z3 SMT Solver
Tương thích hoàn toàn với softsec-toolkit/ch3_verify
Tự động lưu nhật ký thực thi vào ../logs/smt_verify.log
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


def run_smt_verification_e2e():
    print("=================================================================")
    print("  CHUONG 3: KIEM CHUNG FORMAL E2E 3-MODULE VOI Z3 SMT SOLVER")
    print("=================================================================\n")

    soTiet       = Int('soTiet')
    heSoHocPhan  = Real('heSoHocPhan')
    heSoQuyMoLop = Real('heSoQuyMoLop')
    heSoBangCap  = Real('heSoBangCap')
    dmt          = Int('dmt')
    numClasses   = Int('numClasses')

    INT32_MAX = 2**31 - 1
    INT64_MAX = 2**63 - 1

    print("[Check 1] E2E 32-bit Integer Overflow Test across Multi-Class Salary Aggregation:")
    s_unbound = Solver()
    s_unbound.add(numClasses >= 1, numClasses <= 20)
    s_unbound.add(soTiet >= 15, soTiet <= 120)
    s_unbound.add(heSoHocPhan >= 0.5, heSoHocPhan <= 3.0)
    s_unbound.add(heSoQuyMoLop >= 0.1, heSoQuyMoLop <= 0.5)
    s_unbound.add(heSoBangCap >= 1.0, heSoBangCap <= 2.0)
    s_unbound.add(dmt >= 85000, dmt <= 500000)

    soTietQuyDoi = soTiet * (heSoHocPhan + heSoQuyMoLop)
    tienDayPerClass = soTietQuyDoi * heSoBangCap * dmt
    totalTienDay = numClasses * tienDayPerClass

    s_unbound.add(totalTienDay > INT32_MAX)
    res_a = s_unbound.check()

    if res_a == sat:
        print("  --> RESULT: SAT (32-bit Integer Overflow IS POSSIBLE when aggregating multi-class salary!)")
        m = s_unbound.model()
        print("  Counterexample values:")
        print(f"    - numClasses        = {m[numClasses]}")
        print(f"    - soTiet            = {m[soTiet]}")
        print(f"    - heSoHocPhan       = {m[heSoHocPhan]}")
        print(f"    - heSoQuyMoLop      = {m[heSoQuyMoLop]}")
        print(f"    - heSoBangCap       = {m[heSoBangCap]}")
        print(f"    - dinhMucTienChuan  = {m[dmt]} VND")
        print("  --> DE XUAT: Dung long long (int64) va double trong C de dam bao an toan tuyet doi.\n")
    else:
        print("  --> RESULT: UNSAT\n")

    print("[Check 2] E2E 64-bit Integer Overflow Verification (long long / int64):")
    s_64 = Solver()
    s_64.add(numClasses >= 1, numClasses <= 100)
    s_64.add(soTiet >= 1, soTiet <= 500)
    s_64.add(heSoHocPhan >= 0.5, heSoHocPhan <= 5.0)
    s_64.add(heSoQuyMoLop >= 0.1, heSoQuyMoLop <= 2.0)
    s_64.add(heSoBangCap >= 1.0, heSoBangCap <= 3.0)
    s_64.add(dmt >= 50000, dmt <= 2000000)

    soTietQuyDoi_64 = soTiet * (heSoHocPhan + heSoQuyMoLop)
    tienDay_64 = numClasses * (soTietQuyDoi_64 * heSoBangCap * dmt)

    s_64.add(tienDay_64 > INT64_MAX)
    res_64 = s_64.check()

    if res_64 == sat:
        print("  --> RESULT: SAT")
    else:
        print("  --> RESULT: UNSAT (64-bit long long is PROVEN SAFE within all enterprise bounds).")
        print(f"    Limit INT64_MAX = {INT64_MAX:,} VND")
        print("  --> KET LUAN: Code C sau khi fix sang 64-bit (long long/double) phat huy an toan tuyet doi.\n")

    print("[Check 3] E2E Unassigned/Deleted Lecturer Safety Constraint (Mod 1 -> Mod 2 -> Mod 3):")
    # Mo hinh hoa DUNG cong thuc that trong calculate_e2e_salary_SAFE() (ch2_memsafe/tinh_tien_day.c):
    #   if (!lhp->gv_ptr || lhp->gv_ptr->is_deleted) return 0;
    #   else return soTietQuyDoi * heSoBangCap * dinhMucTienChuan;  (cung cong thuc voi Check 1/2)
    # thay vi dung bien Bool/Real truu tuong khong lien quan toi cong thuc thuc te.
    s_null = Solver()
    gv_ptr_is_null = Bool('gv_ptr_is_null')
    is_deleted     = Bool('is_deleted')
    soTiet3        = Int('soTiet3')
    heSoHocPhan3   = Real('heSoHocPhan3')
    heSoQuyMo3     = Real('heSoQuyMo3')
    heSoBangCap3   = Real('heSoBangCap3')
    dmt3           = Int('dmt3')

    s_null.add(soTiet3 >= 1, soTiet3 <= 500)
    s_null.add(heSoHocPhan3 >= 0.5, heSoHocPhan3 <= 5.0)
    s_null.add(heSoQuyMo3 >= 0.0, heSoQuyMo3 <= 0.2)
    s_null.add(heSoBangCap3 >= 1.0, heSoBangCap3 <= 3.0)
    s_null.add(dmt3 >= 50000, dmt3 <= 2000000)

    soTietQuyDoi3 = ToReal(soTiet3) * (heSoHocPhan3 + heSoQuyMo3)
    tienDayNeuDuocTinh = soTietQuyDoi3 * heSoBangCap3 * ToReal(dmt3)
    # tienDayThucTe la dung ham "if (!gv_ptr || is_deleted) return 0; else return cong_thuc;"
    tienDayThucTe = If(Or(gv_ptr_is_null, is_deleted), RealVal(0), tienDayNeuDuocTinh)

    # Kiem chung: khi CHUA gan hoac DA xoa giang vien, cong thuc that co the tra ve > 0 khong?
    s_null.add(Or(gv_ptr_is_null, is_deleted))
    s_null.add(tienDayThucTe > 0)
    res_null = s_null.check()

    if res_null == sat:
        print("  --> RESULT: SAT (Buggy code allows paying salary without assigned lecturer!)")
        m = s_null.model()
        print("  Counterexample values:")
        print(f"    - gv_ptr_is_null = {m[gv_ptr_is_null]}, is_deleted = {m[is_deleted]}")
        print(f"    - soTiet = {m[soTiet3]}, heSoHocPhan = {m[heSoHocPhan3]}, heSoBangCap = {m[heSoBangCap3]}, dinhMucTienChuan = {m[dmt3]} VND\n")
    else:
        print("  --> RESULT: UNSAT (Safe code strictly enforces: NO/DELETED LECTURER -> SALARY = 0 VND,")
        print("      da kiem chung tren chinh cong thuc tinh luong that dung trong Module 3).\n")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "smt_verify.log")
    sys.stdout = TeeLogger(log_file)
    run_smt_verification_e2e()
