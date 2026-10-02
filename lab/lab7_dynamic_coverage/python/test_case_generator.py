"""
Lab 7 - Sinh Test Case Tu dong theo To hop Nhanh (Combinatorial Branch Coverage)
===================================================================================
He thong DuongUniversity Management System - Module 3: Tinh tien day
Chuong 4: 4.4 Tao duong thuc thi chuong trinh

Ky thuat: liet ke cac "lop tuong duong" (equivalence classes) cho tung tham so
dau vao cua calculate_salary(soTiet, heSoHocPhan, soLuongSinhVien, bangCap),
sau do sinh TICH DECARTES (Cartesian product) giua cac lop de dam bao MOI TO
HOP NHANH quan trong deu co it nhat 1 test case dai dien - moi to hop la mot
"duong thuc thi" (execution path) can duoc kiem thu theo tinh than 4.4.

expected_status() la mot ORACLE DOC LAP: viet lai dac ta (CON-5/11/12/13,
tab:range, nguong phe duyet) bang Python, KHONG goi code C - de tranh "kiem thu
chuong trinh bang chinh no" (neu oracle la chinh ham C thi moi test luon PASS,
ke ca khi C sai).

--extended: them lop bien soLuongSinhVien = 50 (dung tai nguong CON-11, KHONG
duoc he so quy mo vi dieu kien la '> 50') va 51 (ngay tren nguong) - Buoc 5.
"""
from __future__ import annotations
import argparse
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lop tuong duong cho tung tham so (nhan, gia tri dai dien)
SOTIET_CLASSES = [
    ("invalid_zero", 0),
    ("invalid_high", 501),          # CON-12: > 500
    ("valid_small", 30),
    ("valid_typical", 45),          # gia tri dung trong main.c
    ("valid_max", 500),             # bien tren, kich hoat APPROVAL voi GS/PGS/TIEN_SI
]
HESO_CLASSES = [
    ("invalid_zero", 0.0),
    ("invalid_negative", -0.5),
    ("valid_one", 1.0),
]
SV_CLASSES = [
    ("invalid_negative", -1),
    ("invalid_high", 301),          # tab:range: > 300
    ("valid_small", 30),            # <= 50: khong he so quy mo
    ("valid_large", 60),            # > 50: he so quy mo 0.2, audit byte OK
    ("valid_very_large", 200),      # > 127: audit byte bi tu choi (CWE-197)
]
SV_BOUNDARY_CLASSES = [             # Buoc 5 - lop tuong duong bo sung
    ("boundary_at_threshold", 50),  # == 50 -> KHONG quy mo (dieu kien '> 50')
    ("boundary_above_threshold", 51),
]
DEGREE_CLASSES = ["GS", "PGS", "TIEN_SI", "THAC_SI", "CU_NHAN", "KY_SU"]  # KY_SU = chuoi la

HE_SO_BANG_CAP = {"GS": 2.0, "PGS": 1.8, "TIEN_SI": 1.5, "THAC_SI": 1.2, "CU_NHAN": 1.0}
DINH_MUC = 85000
NGUONG_PHE_DUYET = 50_000_000


def expected_status(so_tiet: int, he_so: float, sv: int, bang_cap: str) -> str:
    """Oracle doc lap - mo phong lai DAC TA (khong phai code C)."""
    if so_tiet <= 0 or so_tiet > 500:
        return "INVALID_SOTIET"
    if he_so <= 0:
        return "INVALID_HESO"
    if sv < 0 or sv > 300:
        return "INVALID_SV"
    if bang_cap not in HE_SO_BANG_CAP:
        return "INVALID_DEGREE"
    he_so_quy_mo = 0.2 if sv > 50 else 0.0
    tien = so_tiet * (he_so + he_so_quy_mo) * HE_SO_BANG_CAP[bang_cap] * DINH_MUC
    if tien > NGUONG_PHE_DUYET:
        return "APPROVAL_REQUIRED"
    return "OK"


def generate_combinatorial_cases(extended: bool = False) -> list[dict]:
    sv_classes = SV_CLASSES + (SV_BOUNDARY_CLASSES if extended else [])
    cases = []
    for tlabel, so_tiet in SOTIET_CLASSES:
        for hlabel, he_so in HESO_CLASSES:
            for slabel, sv in sv_classes:
                for bang_cap in DEGREE_CLASSES:
                    status = expected_status(so_tiet, he_so, sv, bang_cap)
                    cases.append({
                        "soTiet": so_tiet, "heSoHocPhan": he_so, "soLuongSinhVien": sv,
                        "bangCap": bang_cap, "expected_status": status,
                        "equivalence_classes": f"soTiet={tlabel}, heSo={hlabel}, sv={slabel}, bangCap={bang_cap}",
                    })
    return cases


def save_csv(cases: list[dict], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["soTiet", "heSoHocPhan", "soLuongSinhVien", "bangCap", "expected_status"])
        for c in cases:
            w.writerow([c["soTiet"], c["heSoHocPhan"], c["soLuongSinhVien"], c["bangCap"], c["expected_status"]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended", action="store_true",
                        help="Them lop bien soLuongSinhVien = 50/51 (Buoc 5)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    cases = generate_combinatorial_cases(extended=args.extended)
    name = "salary_test_inputs_combinatorial_extended.csv" if args.extended \
        else "salary_test_inputs_combinatorial.csv"
    out_path = os.path.join(BASE, "dataset", name)
    save_csv(cases, out_path)

    n_sv = len(SV_CLASSES) + (len(SV_BOUNDARY_CLASSES) if args.extended else 0)
    print(f"Da sinh {len(cases)} test case to hop "
          f"({len(SOTIET_CLASSES)} soTiet x {len(HESO_CLASSES)} heSo x {n_sv} sv x {len(DEGREE_CLASSES)} bangCap).")
    from collections import Counter
    dist = Counter(c["expected_status"] for c in cases)
    print("Phan bo nhan ky vong (oracle):", dict(dist))
    if not args.quiet:
        for c in cases:
            print(f"  [{c['equivalence_classes']}] -> {c['expected_status']}")
    print(f"\nDa luu: {out_path}")
