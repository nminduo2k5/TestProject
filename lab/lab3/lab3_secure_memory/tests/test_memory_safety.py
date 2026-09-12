"""
Lab 3 - Bo test tu dong
=======================
1. Bien dich ca 2 phien ban (vulnerable / secure) voi AddressSanitizer.
2. Xac nhan vulnerable_inventory PHAT HIEN du 3 loai loi (overflow/uaf/leak).
3. Xac nhan secure_inventory KHONG co bat ky loi nao trong ca 3 kich ban.
4. Xac nhan risk_assessor.py cho ra ket qua khop voi baseline da luu.

GHI CHU MOI TRUONG (quan trong):
- GCC mac dinh cua MSYS2 UCRT64 (thuong nam san tren PATH) KHONG kem theo
  runtime libasan tren Windows -> "-fsanitize=address" se loi link. Script
  nay dung thang Clang cua moi truong MSYS2 "clang64" (co compiler-rt day
  du) de bien dich, xem CLANG_EXE ben duoi. Cai dat mot lan (neu chua co):
    pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld
- LeakSanitizer (phat hien memory leak cua ASan) KHONG duoc ho tro tren
  Windows o bat ky trinh bien dich nao (day la gioi han chinh thuc cua
  LLVM/compiler-rt, xem https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer
  - muc "Supported Platforms": chi Linux/macOS/NetBSD/Fuchsia, KHONG co
  Windows). Vi vay bai nay dung them mot "custom leak tracker" (dem that
  malloc/free qua atexit(), xem vulnerable_inventory.c/secure_inventory.c)
  de van xac nhan duoc CWE-401 tren Windows ma khong can LeakSanitizer.
"""
import json
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_DIR = os.path.join(BASE, "c")
sys.path.insert(0, os.path.join(BASE, "python"))

from risk_assessor import assess_all  # noqa: E402

CLANG64_BIN = r"C:\msys64\clang64\bin"
CLANG_EXE = os.path.join(CLANG64_BIN, "clang.exe")
# libclang_rt.asan_dynamic phu thuoc bac cau vao libc++.dll - phai bundle ca 2
# thi binary moi chay duoc, neu khong se loi STATUS_DLL_NOT_FOUND (0xC0000135).
RUNTIME_DLLS = [
    os.path.join(CLANG64_BIN, "libclang_rt.asan_dynamic-x86_64.dll"),
    os.path.join(CLANG64_BIN, "libc++.dll"),
]
CC = CLANG_EXE if os.path.exists(CLANG_EXE) else "gcc"


def _build(src_name: str, bin_name: str):
    subprocess.run(
        [CC, "-g", "-fsanitize=address", "-Wall", "-Wextra", "-o", bin_name, src_name],
        cwd=C_DIR, check=True,
    )
    # Bundle cac runtime DLL can thiet cung thu muc voi .exe de chay duoc
    # ngay, khong can sua PATH he thong.
    for dll in RUNTIME_DLLS:
        if os.path.exists(dll):
            shutil.copy2(dll, C_DIR)


def _run(bin_name: str, args: list[str]):
    return subprocess.run(
        [os.path.join(C_DIR, bin_name)] + args,
        cwd=C_DIR, capture_output=True, text=True,
    )


def setup_module(_module=None):
    if CC == "gcc":
        print("[CANH BAO] Khong tim thay Clang tai", CLANG64_BIN,
              "- dung gcc mac dinh, -fsanitize=address co the loi link tren Windows.\n"
              "  Cai dat: pacman -S mingw-w64-clang-x86_64-clang "
              "mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld")
    _build("vulnerable_inventory.c", "vulnerable_inventory")
    _build("secure_inventory.c", "secure_inventory")


def test_vulnerable_overflow_detected():
    proc = _run("vulnerable_inventory", ["overflow", "A" * 39])
    assert proc.returncode != 0
    assert "heap-buffer-overflow" in proc.stderr


def test_vulnerable_uaf_detected():
    proc = _run("vulnerable_inventory", ["uaf"])
    assert proc.returncode != 0
    assert "heap-use-after-free" in proc.stderr


def test_vulnerable_leak_detected():
    # LeakSanitizer khong duoc ho tro tren Windows (xem ghi chu dau file).
    # QUAN TRONG: dat ASAN_OPTIONS=detect_leaks=1 tren Windows khien ASan bao
    # loi cau hinh va ABORT TRUOC KHI main() chay (khong chi bo qua option),
    # nen KHONG duoc dat bien nay o day - chi dua vao custom leak tracker
    # (dem malloc/free that qua atexit()), hoat dong dung tren moi nen tang.
    proc = _run("vulnerable_inventory", ["leak"])
    assert "leaked" in proc.stderr or "CUSTOM-LEAK-TRACKER] 5 allocation(s) leaked" in proc.stderr


def test_secure_overflow_clean():
    proc = _run("secure_inventory", ["overflow", "A" * 39])
    assert proc.returncode == 0
    assert "ERROR" not in proc.stderr


def test_secure_uaf_clean():
    proc = _run("secure_inventory", ["uaf"])
    assert proc.returncode == 0
    assert "ERROR" not in proc.stderr


def test_secure_leak_clean():
    proc = _run("secure_inventory", ["leak"])
    assert proc.returncode == 0
    assert "leaked" not in proc.stderr
    assert "CUSTOM-LEAK-TRACKER] No leaks detected" in proc.stderr


def test_risk_assessment_matches_baseline():
    results = assess_all(os.path.join(BASE, "dataset", "vulnerabilities.json"))
    with open(os.path.join(BASE, "dataset", "expected_risk_baseline.json"), encoding="utf-8") as f:
        expected = json.load(f)
    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert r["id"] == e["id"]
        assert r["severity"] == e["severity"]
        assert abs(r["base_score"] - e["base_score"]) < 0.05


def test_critical_vuln_is_the_buffer_overflow():
    results = assess_all(os.path.join(BASE, "dataset", "vulnerabilities.json"))
    top = results[0]
    assert top["severity"] == "CRITICAL"
    assert top["cwe"] == "CWE-121"


if __name__ == "__main__":
    try:
        setup_module()
    except subprocess.CalledProcessError as e:
        print(f"[LOI BIEN DICH] Khong the build binary: {e}")
        print("  Kiem tra Clang da cai dat tai C:\\msys64\\clang64\\bin chua "
              "(pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld).")
        sys.exit(1)

    tests = [
        test_vulnerable_overflow_detected, test_vulnerable_uaf_detected,
        test_vulnerable_leak_detected, test_secure_overflow_clean,
        test_secure_uaf_clean, test_secure_leak_clean,
        test_risk_assessment_matches_baseline, test_critical_vuln_is_the_buffer_overflow,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} test da PASS")
