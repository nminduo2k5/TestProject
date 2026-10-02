"""
Lab 6 - Bo test tu dong (DuongUniversity - Module 2 danhSachLop[MAX_LOP])
==========================================================================
5 test theo de bai + 2 test bo sung cho BMC-05/BMC-06 tu them:
1. Dong co BMC (Python/Z3) cho ket qua khop ky vong tren toan bo 6 chuong trinh.
2. Nhan chung BMC-03 (base_index=9) phai THUC SU lam chuong trinh C crash duoi ASan.
3. safe_full_scan  : chay sach, khong loi ASan.
4. symbolic_safe (base=9) : bi TU CHOI o tien dieu kien (khong crash).
5. symbolic_safe (base=3) : chay sach.
6. (bo sung) BMC-05: nhan chung (i=0, index=10) khop ASan crash cua symbolic_reverse.
7. (bo sung) BMC-06: symbolic_reverse_fixed chay sach.

GHI CHU MOI TRUONG (giong Lab 3): GCC cua MSYS2 UCRT64 KHONG kem libasan tren
Windows -> dung Clang cua moi truong MSYS2 clang64 (co compiler-rt) va bundle
2 DLL runtime canh file .exe. Can python co z3-solver (vd Anaconda).
"""
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_DIR = os.path.join(BASE, "c")
sys.path.insert(0, os.path.join(BASE, "python"))

from bmc_engine import run_all  # noqa: E402

DATASET = os.path.join(BASE, "dataset", "bmc_programs.json")
SRC = "lop_hoc_phan_access.c"
EXE = "lop_hoc_phan_access.exe"

CLANG64_BIN = r"C:\msys64\clang64\bin"
CLANG_EXE = os.path.join(CLANG64_BIN, "clang.exe")
RUNTIME_DLLS = [
    os.path.join(CLANG64_BIN, "libclang_rt.asan_dynamic-x86_64.dll"),
    os.path.join(CLANG64_BIN, "libc++.dll"),
]
CC = CLANG_EXE if os.path.exists(CLANG_EXE) else "gcc"

_built = False


def _build():
    global _built
    if _built:
        return
    if CC == "gcc":
        print("[CANH BAO] Khong tim thay Clang tai", CLANG64_BIN,
              "- dung gcc, -fsanitize=address co the loi link tren Windows.")
    subprocess.run([CC, "-g", "-fsanitize=address", "-Wall", "-Wextra", "-o", EXE, SRC],
                   cwd=C_DIR, check=True)
    for dll in RUNTIME_DLLS:
        if os.path.exists(dll):
            shutil.copy2(dll, C_DIR)
    _built = True


def _run(args: list[str]):
    _build()
    return subprocess.run([os.path.join(C_DIR, EXE)] + args,
                          cwd=C_DIR, capture_output=True, text=True)


def test_bmc_results_match_expectation():
    results = run_all(DATASET)
    mismatches = [r for r in results if not r["matches_expectation"]]
    assert not mismatches, f"BMC sai lech ky vong: {[m['id'] for m in mismatches]}"
    assert len(results) == 6


def test_bmc03_witness_matches_c_runtime_bug():
    """Nhan chung cua BMC-03 (base_index=9) phai la gia tri THUC SU gay loi
    khi chay chuong trinh C tuong ung - buoc 'doi chieu' tinh <-> dong."""
    results = {r["id"]: r for r in run_all(DATASET)}
    witness = results["BMC-03-UNSAFE-SYMBOLIC-OFFSET"]["witness"]
    base_index = witness["base_index"]
    proc = _run(["symbolic_unsafe", str(base_index)])
    assert proc.returncode != 0, "Chuong trinh C phai crash voi base_index tu nhan chung BMC"
    assert "AddressSanitizer" in proc.stderr
    assert "stack-buffer-overflow" in proc.stderr


def test_c_safe_full_scan_no_crash():
    proc = _run(["safe_full_scan"])
    assert proc.returncode == 0
    assert "AddressSanitizer" not in proc.stderr
    assert "TONG THU LAO HOC KY" in proc.stdout


def test_c_symbolic_safe_with_precondition_rejects_bad_input():
    proc = _run(["symbolic_safe", "9"])
    assert proc.returncode == 0
    assert "TU CHOI" in proc.stderr
    assert "AddressSanitizer" not in proc.stderr


def test_c_symbolic_safe_with_valid_input_runs_clean():
    proc = _run(["symbolic_safe", "3"])
    assert proc.returncode == 0
    assert "AddressSanitizer" not in proc.stderr
    assert "danhSachLop[7]" in proc.stdout   # 3 + 4 = 7 la lop cuoi cua trang


def test_bmc05_reverse_witness_matches_c_runtime_bug():
    results = {r["id"]: r for r in run_all(DATASET)}
    r = results["BMC-05-UNSAFE-REVERSE-COUNTDOWN"]
    assert r["violated_at_step"] == 0
    assert r["witness"]["index_accessed"] == 10
    proc = _run(["symbolic_reverse"])
    assert proc.returncode != 0
    assert "AddressSanitizer" in proc.stderr


def test_bmc06_reverse_fixed_runs_clean():
    results = {r["id"]: r for r in run_all(DATASET)}
    assert results["BMC-06-SAFE-REVERSE-COUNTDOWN-FIXED"]["label"] == "SAFE"
    proc = _run(["symbolic_reverse_fixed"])
    assert proc.returncode == 0
    assert "AddressSanitizer" not in proc.stderr
    assert "danhSachLop[9]" in proc.stdout and "danhSachLop[5]" in proc.stdout


if __name__ == "__main__":
    tests = [
        test_bmc_results_match_expectation, test_bmc03_witness_matches_c_runtime_bug,
        test_c_safe_full_scan_no_crash, test_c_symbolic_safe_with_precondition_rejects_bad_input,
        test_c_symbolic_safe_with_valid_input_runs_clean,
        test_bmc05_reverse_witness_matches_c_runtime_bug, test_bmc06_reverse_fixed_runs_clean,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} test da PASS")
    sys.exit(0 if passed == len(tests) else 1)
