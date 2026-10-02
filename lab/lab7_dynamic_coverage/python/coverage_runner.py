"""
Lab 7 - Do Do phu Ma (Code Coverage) va Theo doi Thuc thi Chuong trinh
=========================================================================
He thong DuongUniversity Management System - Module 3: Tinh tien day
Chuong 4: 4.2 Phu ma nguon (code coverage), 4.3 Theo doi thuc thi chuong trinh,
          4.4 Tao duong thuc thi chuong trinh

Module nay:
  1. Bien dich tinh_tien_day_coverage.c voi co --coverage (sinh .gcno/.gcda).
  2. Chay CLI voi mot bo du lieu test dau vao (CSV), thu duoc PASS/FAIL cho
     tung test case.
  3. Chay gcov -b de tinh % DONG LENH duoc thuc thi (statement coverage) VA
     % NHANH (branch coverage), dong thoi bao cao cac dong CHUA duoc phu
     (candidate cho "duong thuc thi" chua duoc kiem thu - muc tieu cua 4.4).
  4. So sanh coverage giua cac bo test: "partial" (2 case), "full" (13 case),
     "combinatorial" (tu sinh tu lop tuong duong) va "combinatorial_extended"
     (them lop bien 50/51 - Buoc 5) de minh hoa truc quan: PASS 100% KHONG
     noi len chat luong kiem thu.

Moi truong: gcc + gcov cua MSYS2 UCRT64 (co san tren PATH), khong can clang.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_DIR = os.path.join(BASE, "c")
SRC = "tinh_tien_day_coverage.c"
OBJ = "tinh_tien_day_coverage.o"
EXE = "tinh_tien_day_cli.exe"
GCOV_FILE = SRC + ".gcov"

SUITES = [
    "salary_test_inputs_partial.csv",
    "salary_test_inputs_full.csv",
    "salary_test_inputs_combinatorial.csv",
    "salary_test_inputs_combinatorial_extended.csv",
]


def clean_coverage_artifacts():
    for fname in os.listdir(C_DIR):
        if fname.endswith((".gcda", ".gcno", ".gcov", ".o")) or fname == EXE:
            os.remove(os.path.join(C_DIR, fname))


def build_instrumented():
    subprocess.run(
        ["gcc", "-Wall", "-Wextra", "-std=c11", "--coverage", "-DSALARY_CLI_MAIN",
         "-c", SRC, "-o", OBJ],
        cwd=C_DIR, check=True,
    )
    subprocess.run(["gcc", "--coverage", "-o", EXE, OBJ], cwd=C_DIR, check=True)


def run_test_suite(csv_path: str) -> str:
    proc = subprocess.run([os.path.join(C_DIR, EXE), csv_path],
                          cwd=C_DIR, capture_output=True, text=True)
    return proc.stdout


def compute_coverage() -> dict:
    gcov_proc = subprocess.run(["gcov", "-b", SRC], cwd=C_DIR, capture_output=True, text=True)
    # Branch coverage lay tu stdout cua gcov -b:
    #   Branches executed:91.67% of 48
    #   Taken at least once:70.83% of 48
    branches_total = branches_taken = None
    m = re.search(r"Taken at least once:\s*([\d.]+)% of (\d+)", gcov_proc.stdout)
    if m:
        pct, n = float(m.group(1)), int(m.group(2))
        branches_total = n
        branches_taken = round(n * pct / 100.0)

    gcov_file = os.path.join(C_DIR, GCOV_FILE)
    total = covered = 0
    uncovered = []
    if os.path.exists(gcov_file):
        with open(gcov_file, encoding="utf-8", errors="ignore") as f:
            for raw in f:
                m = re.match(r"\s*(\S+):\s*(\d+):(.*)", raw)
                if not m:
                    continue
                count_str, lineno, code = m.groups()
                if count_str in ("-", ""):
                    continue
                total += 1
                if count_str.startswith("#####") or count_str.startswith("====="):
                    uncovered.append((int(lineno), code.strip()))
                else:
                    covered += 1
    pct = round(100.0 * covered / total, 2) if total else 0.0
    bpct = round(100.0 * branches_taken / branches_total, 2) if branches_total else None
    return {
        "lines_total": total, "lines_covered": covered, "coverage_percent": pct,
        "branches_total": branches_total, "branches_taken": branches_taken,
        "branch_coverage_percent": bpct,
        "uncovered_lines": uncovered,
    }


def evaluate_suite(csv_name: str) -> dict:
    clean_coverage_artifacts()
    build_instrumented()
    csv_path = os.path.join(BASE, "dataset", csv_name)
    output = run_test_suite(csv_path)
    cov = compute_coverage()
    m = re.search(r"Tong: (\d+)/(\d+) test PASS", output)
    passed, total = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return {"suite": csv_name, "test_output": output, "tests_passed": passed,
            "tests_total": total, "coverage": cov}


def print_suite(res: dict, show_cases: bool = True):
    cov = res["coverage"]
    if show_cases:
        print(res["test_output"])
    else:
        print(f"(an {res['tests_total']} dong chi tiet) Tong: {res['tests_passed']}/{res['tests_total']} test PASS\n")
    print(f"Line coverage  : {cov['coverage_percent']}% "
          f"({cov['lines_covered']}/{cov['lines_total']} dong)")
    if cov["branch_coverage_percent"] is not None:
        print(f"Branch coverage: {cov['branch_coverage_percent']}% "
              f"({cov['branches_taken']}/{cov['branches_total']} nhanh 'taken at least once')")
    if cov["uncovered_lines"]:
        print("Cac dong CHUA duoc kiem thu:")
        for lineno, code in cov["uncovered_lines"]:
            print(f"  Dong {lineno}: {code}")


if __name__ == "__main__":
    results = {}
    labels = {
        SUITES[0]: "PARTIAL (khong day du, 2 case)",
        SUITES[1]: "FULL (day du, 13 case)",
        SUITES[2]: "COMBINATORIAL (tu sinh tu lop tuong duong)",
        SUITES[3]: "COMBINATORIAL_EXTENDED (them lop bien sv=50/51 - Buoc 5)",
    }
    for suite in SUITES:
        if not os.path.exists(os.path.join(BASE, "dataset", suite)):
            print(f"[BO QUA] {suite} chua ton tai - chay python/test_case_generator.py truoc.")
            continue
        print(f"\n############ BO TEST {labels[suite]} ############")
        res = evaluate_suite(suite)
        print_suite(res, show_cases=(res["tests_total"] <= 20))
        key = suite.replace("salary_test_inputs_", "").replace(".csv", "")
        results[key] = {"tests_passed": res["tests_passed"], "tests_total": res["tests_total"],
                        "coverage": res["coverage"]}

    print("\n=== BANG SO SANH ===")
    print(f"{'Bo test':<24}{'So case':>8}{'PASS':>8}{'Line cov':>11}{'Branch cov':>12}")
    for key, r in results.items():
        c = r["coverage"]
        print(f"{key:<24}{r['tests_total']:>8}{r['tests_passed']:>8}"
              f"{c['coverage_percent']:>10}%{str(c['branch_coverage_percent']):>11}%")

    out_path = os.path.join(BASE, "dataset", "coverage_comparison_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nKet qua da luu: {out_path}")
    sys.exit(0)
