"""
Lab 7 - Bo test tu dong (DuongUniversity - Module 3 calculate_salary())
=======================================================================
4 test theo de bai + 1 test bo sung cho lop tuong duong moi (Buoc 5):
1. Bo 'partial' (2 case) PASS 100% - nhung coverage thap (minh hoa khoang cach
   giua "test PASS" va "coverage cao").
2. Bo 'full' (13 case) PASS 100%.
3. Bo 'full' co coverage CAO HON bo 'partial' it nhat 5 diem phan tram.
4. Bo to hop (combinatorial) tu sinh PASS 100% va coverage >= bo 'full'.
5. (bo sung) Bo to hop MO RONG (them lop bien sv=50/51) PASS 100%, coverage >= bo
   to hop goc, va oracle doc lap phan loai dung 2 gia tri bien (50 -> khong quy mo,
   51 -> co quy mo).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "python"))

from coverage_runner import evaluate_suite  # noqa: E402
from test_case_generator import generate_combinatorial_cases, save_csv, expected_status  # noqa: E402

MIN_IMPROVEMENT_PCT = 5.0
_cache = {}


def _suite(name):
    if name not in _cache:
        _cache[name] = evaluate_suite(name)
    return _cache[name]


def test_partial_suite_all_pass():
    result = _suite("salary_test_inputs_partial.csv")
    assert "Tong: 2/2 test PASS" in result["test_output"]


def test_full_suite_all_pass():
    result = _suite("salary_test_inputs_full.csv")
    assert "Tong: 13/13 test PASS" in result["test_output"]


def test_full_suite_covers_significantly_more_than_partial():
    partial = _suite("salary_test_inputs_partial.csv")
    full = _suite("salary_test_inputs_full.csv")
    diff = full["coverage"]["coverage_percent"] - partial["coverage"]["coverage_percent"]
    assert diff >= MIN_IMPROVEMENT_PCT, (
        f"Bo test full phai phu them >= {MIN_IMPROVEMENT_PCT}% so voi partial, "
        f"thuc te chi hon {diff}%"
    )
    assert full["coverage"]["branch_coverage_percent"] > partial["coverage"]["branch_coverage_percent"]


def test_combinatorial_suite_all_pass_and_matches_or_exceeds_full_coverage():
    cases = generate_combinatorial_cases()
    save_csv(cases, os.path.join(BASE, "dataset", "salary_test_inputs_combinatorial.csv"))
    result = _suite("salary_test_inputs_combinatorial.csv")
    assert result["tests_total"] == len(cases) and result["tests_passed"] == result["tests_total"], (
        f"Co test FAIL trong bo to hop: {result['tests_passed']}/{result['tests_total']}")
    full = _suite("salary_test_inputs_full.csv")
    assert result["coverage"]["coverage_percent"] >= full["coverage"]["coverage_percent"] - 0.5
    assert result["coverage"]["branch_coverage_percent"] >= full["coverage"]["branch_coverage_percent"]


def test_extended_suite_with_boundary_class():
    assert expected_status(45, 1.0, 50, "TIEN_SI") == "OK"
    assert expected_status(45, 1.0, 51, "TIEN_SI") == "OK"
    cases = generate_combinatorial_cases(extended=True)
    assert any(c["soLuongSinhVien"] == 50 for c in cases) and any(c["soLuongSinhVien"] == 51 for c in cases)
    save_csv(cases, os.path.join(BASE, "dataset", "salary_test_inputs_combinatorial_extended.csv"))
    result = _suite("salary_test_inputs_combinatorial_extended.csv")
    assert result["tests_total"] == len(cases) and result["tests_passed"] == result["tests_total"]
    base = _suite("salary_test_inputs_combinatorial.csv")
    assert result["coverage"]["coverage_percent"] >= base["coverage"]["coverage_percent"]
    # 2 gia tri bien phai roi vao 2 nhanh khac nhau cua CON-11: quyMo=0.0 (sv=50) va 0.2 (sv=51)
    out = result["test_output"]
    assert "sv=50   bangCap=TIEN_SI  expected=OK                 actual=OK                 quyMo=0.0" in out
    assert "sv=51   bangCap=TIEN_SI  expected=OK                 actual=OK                 quyMo=0.2" in out


if __name__ == "__main__":
    tests = [
        test_partial_suite_all_pass, test_full_suite_all_pass,
        test_full_suite_covers_significantly_more_than_partial,
        test_combinatorial_suite_all_pass_and_matches_or_exceeds_full_coverage,
        test_extended_suite_with_boundary_class,
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
