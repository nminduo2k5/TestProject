"""
Lab 8 - Bo test tu dong (DuongUniversity - Module 3 Tinh tien day)
==================================================================
4 test theo de bai + 1 test bo sung:
1. Dong lenh hop le (GV:/LHP:/GVADM khong co '!') KHONG crash.
2. Input crash da biet ("GVADM:!" + payload dai) lam ASan bao loi.
3. Fuzzer HOP TRANG (coverage-guided) tim duoc >= 1 crash trong ngan sach 500 lan thu
   (seed co dinh de tai lap), moi crash phai bat dau bang magic "GVADM:!".
4. Fuzzer HOP DEN, voi ngan sach 1000 lan thu (seed co dinh), KHONG tim duoc crash nao.
5. (bo sung) File crash cua hop trang duoc luu trong crashes/ va CHAY LAI van crash
   (input da luu la bang chung tai lap duoc, khong phai ngau nhien).

GHI CHU MOI TRUONG: dung Clang clang64 (ASan + --coverage), doc coverage bang llvm-cov
gcov. Can python co the chay subprocess (Anaconda / MSYS2 deu duoc, khong can z3).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "python"))

from fuzz_common import build_target, is_crash, run_target  # noqa: E402
from blackbox_fuzzer import fuzz as blackbox_fuzz  # noqa: E402
from whitebox_fuzzer import fuzz as whitebox_fuzz  # noqa: E402

WB_SEED, WB_BUDGET = 7, 500
BB_SEED, BB_BUDGET = 42, 1000

_wb_cache = {}


def _whitebox():
    if "r" not in _wb_cache:
        _wb_cache["r"] = whitebox_fuzz(iterations=WB_BUDGET, seed=WB_SEED)
    return _wb_cache["r"]


def test_normal_inputs_do_not_crash():
    build_target(with_coverage=True)
    for arg in ["GV:NguyenVanA", "LHP:CNTT2024_01", "GVADM:xinchao", "GVADM:" + "A" * 40, "BAT_KY"]:
        proc = run_target(arg)
        assert proc is not None and proc.returncode == 0, f"Input hop le khong duoc crash: {arg!r}"


def test_known_crash_input_triggers_asan():
    build_target(with_coverage=True)
    proc = run_target("GVADM:!" + "A" * 30)
    assert is_crash(proc), "GVADM:! + payload dai phai lam ASan bao loi"
    assert "stack-buffer-overflow" in proc.stderr


def test_whitebox_fuzzer_finds_crash_within_budget():
    r = _whitebox()
    assert len(r["crashes"]) >= 1, f"Fuzzer hop trang phai tim >= 1 crash trong {WB_BUDGET} lan thu"
    for c in r["crashes"]:
        assert c["input"].startswith("GVADM:!"), c["input"]


def test_blackbox_fuzzer_fails_within_same_budget():
    r = blackbox_fuzz(iterations=BB_BUDGET, seed=BB_SEED)
    assert len(r["crashes"]) == 0, (
        f"Fuzzer hop den (khong coverage feedback) KHONG duoc tim thay crash trong {BB_BUDGET} lan thu")


def test_saved_crash_files_reproduce():
    r = _whitebox()
    assert r["crashes"], "can it nhat 1 crash da luu"
    build_target(with_coverage=True)
    for c in r["crashes"]:
        assert os.path.exists(c["saved_to"])
        with open(c["saved_to"], encoding="utf-8") as f:
            saved = f.read()
        assert saved == c["input"]
        assert is_crash(run_target(saved)), f"Input da luu khong tai lap crash: {c['saved_to']}"


if __name__ == "__main__":
    tests = [
        test_normal_inputs_do_not_crash, test_known_crash_input_triggers_asan,
        test_whitebox_fuzzer_finds_crash_within_budget, test_blackbox_fuzzer_fails_within_same_budget,
        test_saved_crash_files_reproduce,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}", flush=True)
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}", flush=True)
    print(f"\n{passed}/{len(tests)} test da PASS")
    sys.exit(0 if passed == len(tests) else 1)
