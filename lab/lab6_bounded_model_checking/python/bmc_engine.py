"""
Lab 6 - Dong co Bounded Model Checking (BMC) tu viet, dung Z3
================================================================
He thong DuongUniversity Management System - Module 2: Quan ly Lop hoc phan
Chuong 3: 3.5 Kiem chung mo hinh phan mem (Bounded Model Checking),
          3.6 Mo hinh bo nho, 3.7 Sap xep mo hinh bo nho

Doi tuong kiem chung: mang danhSachLop[MAX_LOP = 10] (toi da 10 lop hoc phan /
giang vien / hoc ky) va vong lap "xuat bang ke thu lao theo trang" doc
danhSachLop[base_index + i] voi i = 0..PAGE_SIZE-1 (PAGE_SIZE = 5). base_index
la offset trang do nguoi dung nhap (dau vao KHONG tin cay).

Y tuong BMC (Bounded Model Checking):
  1. "Mo cuon" (unwind) vong lap toi da k buoc (k = "bound").
  2. Tai moi buoc i = 0..k-1, sinh RA MOT BAN SAO cac dieu kien duong di
     (path condition) va cac assertion (khang dinh an toan, o day la
     "0 <= index < array_size") duoi dang cong thuc SMT.
  3. Dung SMT solver kiem tra: TON TAI mot phep gan gia tri bien dau vao
     (o day: base_index) sao cho MOT assertion nao do bi VI PHAM hay khong?
     - SAT  => tim thay loi (BUG), solver tra ve counterexample cu the
       ("nhan chung" - witness) de dua thang vao chuong trinh C that.
     - UNSAT (voi TOAN BO cac buoc unwind) => AN TOAN TRONG PHAM VI BOUND
       da cho - LUU Y: day KHONG phai chung minh an toan tuyet doi cho MOI
       so lan lap, chi la "an toan cho toi k buoc dau tien". Day la GIOI
       HAN CO BAN cua BMC, khac voi model checking day du (unbounded).
       Thi nghiem --bound-experiment ben duoi chung minh dieu nay bang log that.

Mo hinh bo nho (memory model) don gian dung o day: mang danhSachLop duoc bieu
dien tuong trung boi khoang chi so hop le [0, array_size), va viec "truy cap
danhSachLop[index]" duoc mo hinh hoa boi rang buoc "index phai thuoc khoang
nay" - day la mot dang don gian hoa cua Z3 Array theory (chi mo hinh hoa tinh
hop le cua chi so, khong mo hinh hoa gia tri soTiet/heSoHocPhan ben trong).

Cong thuc chi so (truong "index_formula" trong dataset):
  base_plus_i          : index = base_index + i          (BMC-01..04, phan trang)
  size_minus_i         : index = array_size - i          (BMC-05, dem nguoc SAI)
  size_minus_1_minus_i : index = array_size - 1 - i      (BMC-06, dem nguoc DUNG)
"""
from __future__ import annotations
import argparse
import copy
import json
import os
from z3 import Int, Solver, sat, And, Not

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_FORMULAS = {
    "base_plus_i": lambda base, size, i: base + i,
    "size_minus_i": lambda base, size, i: size - i,
    "size_minus_1_minus_i": lambda base, size, i: size - 1 - i,
}


def run_bmc(program: dict) -> dict:
    array_size = program["array_size"]
    unwind_bound = program["unwind_bound"]
    symbolic_base = program["symbolic_base"]
    precondition_max_base = program.get("precondition_max_base")
    formula = INDEX_FORMULAS[program.get("index_formula", "base_plus_i")]

    for i in range(unwind_bound):
        solver = Solver()

        if symbolic_base:
            base_index = Int("base_index")
            solver.add(base_index >= 0, base_index < array_size)  # gia dinh dau vao hop le
            if precondition_max_base is not None:
                # Tien dieu kien bo sung: gioi han base_index de dam bao an toan
                # trong pham vi unwind (day la "fix" tuong duong voi kiem tra
                # rang buoc truoc vong lap trong code C that - symbolic_safe()).
                solver.add(base_index <= precondition_max_base)
        else:
            base_index = program["fixed_base"] if program.get("fixed_base") is not None else 0

        index_expr = formula(base_index, array_size, i)  # buoc unwind thu i
        assertion_safe = And(index_expr >= 0, index_expr < array_size)

        # BMC hoi: TON TAI phep gan nao lam assertion SAI (vi pham) khong?
        solver.add(Not(assertion_safe))
        result = solver.check()

        if result == sat:
            model = solver.model()
            witness = {}
            if symbolic_base:
                witness["base_index"] = model[base_index].as_long() if model[base_index] is not None else None
                concrete_base = witness["base_index"]
            else:
                concrete_base = base_index
            witness["unwind_step_i"] = i
            witness["index_accessed"] = formula(concrete_base, array_size, i)
            return {
                "id": program["id"],
                "label": "UNSAFE",
                "violated_at_step": i,
                "witness": witness,
                "explanation": f"Tai buoc unwind i={i}, ton tai gia tri lam truy cap "
                                f"danhSachLop[index] voi index nam ngoai [0, {array_size}).",
            }

    return {
        "id": program["id"],
        "label": "SAFE",
        "violated_at_step": None,
        "witness": None,
        "explanation": f"Khong tim thay vi pham trong {unwind_bound} buoc unwind dau tien "
                        f"(SAFE-UP-TO-BOUND, khong phai chung minh an toan vo han).",
    }


def load_programs(dataset_path: str) -> list[dict]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)["programs"]


def run_all(dataset_path: str) -> list[dict]:
    results = []
    for prog in load_programs(dataset_path):
        r = run_bmc(prog)
        r["expected_label"] = prog["expected_label"]
        r["matches_expectation"] = (r["label"] == prog["expected_label"])
        r["description"] = prog["description"]
        results.append(r)
    return results


def print_report(results: list[dict]):
    for r in results:
        mark = "OK" if r["matches_expectation"] else "SAI LECH KY VONG!"
        print(f"[{r['id']}] {r['description']}")
        print(f"  Ket qua BMC : {r['label']}  (ky vong: {r['expected_label']})  [{mark}]")
        print(f"  Giai thich  : {r['explanation']}")
        if r["witness"]:
            print(f"  Nhan chung  : {r['witness']}")
        print()


def bound_experiment(dataset_path: str, reduced_bound: int = 5) -> list[dict]:
    """Buoc 4 cua de bai: giam unwind_bound xuong nho hon array_size va chay lai.
    Chung minh bang log that rang BMC bao SAFE cho BMC-02 (off-by-one THAT) khi
    bound = 5 < 11 -> 'SAFE up to bound' KHONG dong nghia voi an toan tuyet doi."""
    out = []
    for prog in load_programs(dataset_path):
        if prog["id"].startswith(("BMC-01", "BMC-02")):
            p = copy.deepcopy(prog)
            original_bound = p["unwind_bound"]
            p["unwind_bound"] = reduced_bound
            r = run_bmc(p)
            r["original_bound"] = original_bound
            r["reduced_bound"] = reduced_bound
            r["expected_label_with_full_bound"] = prog["expected_label"]
            r["false_negative"] = (prog["expected_label"] == "UNSAFE" and r["label"] == "SAFE")
            out.append(r)
    return out


def print_bound_experiment(rows: list[dict]):
    print("=== THI NGHIEM GIOI HAN BMC: giam unwind_bound (Buoc 4) ===")
    for r in rows:
        print(f"[{r['id']}] bound {r['original_bound']} -> {r['reduced_bound']}: "
              f"BMC bao {r['label']} (ky vong voi bound day du: {r['expected_label_with_full_bound']})"
              + ("   <-- FALSE NEGATIVE: loi off-by-one o buoc i=10 nam NGOAI 5 buoc da unwind"
                 if r["false_negative"] else ""))
    print("Ket luan: 'SAFE up to bound k' chi dam bao k buoc dau; vong lap that chay 11 buoc"
          " nen loi tai i=10 bi bo sot. Phai chon k >= so lan lap thuc te (hoac dung k-induction).\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab 6 BMC engine (DuongUniversity - danhSachLop)")
    parser.add_argument("--bound-experiment", action="store_true",
                        help="Chay thi nghiem giam unwind_bound (Buoc 4 cua de bai)")
    parser.add_argument("--reduced-bound", type=int, default=5)
    args = parser.parse_args()

    dataset_path = os.path.join(BASE, "dataset", "bmc_programs.json")

    if args.bound_experiment:
        rows = bound_experiment(dataset_path, args.reduced_bound)
        print_bound_experiment(rows)
        out_path = os.path.join(BASE, "dataset", "bmc_bound_experiment.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"Ket qua da luu: {out_path}")
        raise SystemExit(0)

    results = run_all(dataset_path)
    print_report(results)

    out_path = os.path.join(BASE, "dataset", "bmc_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    n_ok = sum(1 for r in results if r["matches_expectation"])
    print(f"Tong ket: {n_ok}/{len(results)} chuong trinh khop ky vong.")
    print(f"Ket qua da luu: {out_path}")
