"""
Lab 8 - Fuzzing Hop den (Black-box Fuzzing) - DuongUniversity Module 3
======================================================================
Chuong 4: 4.5 Kiem thu hop den (black-box fuzzing)

Dac diem: fuzzer KHONG nhin thay ma nguon hay coverage cua target - chi quan sat
"co crash hay khong" tu ben ngoai. O day dung bien the thuc te hon "random tuyet
doi": corpus hat giong (seed_corpus) + tu dien token (DICTIONARY) roi DOT BIEN
ngau nhien (chen/xoa/thay ky tu, ghep token). Van la hop den vi KHONG dung
coverage feedback de dan duong - chi dua vao may man + kho ngu.

Doi voi fuzz target DuongUniversity, lo hong nam sau 2 lop nhanh long nhau
("GVADM:" -> "!" -> payload du dai): fuzzer hop den gan nhu khong the ghep ngau
nhien dung ca 2 lop + do dai trong ngan sach thap -> minh hoa diem yeu cua no.
"""
from __future__ import annotations
import random

from fuzz_common import (REBUILD_EVENTS, build_target, is_crash, load_seeds,
                         mutate, run_target, save_crash)


def fuzz(iterations: int = 3000, seed: int = 42, rebuild: bool = True) -> dict:
    if rebuild:
        build_target(with_coverage=True)  # coverage bat de cong bang ve toc do voi whitebox
    rng = random.Random(seed)
    corpus = load_seeds()
    crashes = []
    reached_gvadm = 0  # dem so lan "tinh co" cham duoc nhanh magic (chi de thong ke)

    for i in range(iterations):
        candidate = mutate(rng.choice(corpus), rng)
        proc = run_target(candidate)
        if proc is None:
            continue
        if candidate.startswith("GVADM:"):
            reached_gvadm += 1
        if is_crash(proc):
            path = save_crash("blackbox", len(crashes), candidate)
            crashes.append({"iteration": i, "input": candidate, "saved_to": path})
        if rng.random() < 0.05:   # thinh thoang them mau khong-crash vao corpus (tang da dang)
            corpus.append(candidate)

    return {"iterations": iterations, "seed": seed, "corpus_final_size": len(corpus),
            "reached_gvadm_prefix": reached_gvadm, "crashes": crashes, "binary_rebuilds": len(REBUILD_EVENTS)}


if __name__ == "__main__":
    print("=================================================================")
    print("  LAB 8 - BLACK-BOX FUZZING (DuongUniversity Module 3 Tinh tien day)")
    print("=================================================================")
    for iters in (1000, 3000, 5000):
        r = fuzz(iterations=iters, seed=42, rebuild=(iters == 1000))
        print(f"\n[Ngan sach {iters} lan thu, seed=42]")
        print(f"  Corpus cuoi cung        : {r['corpus_final_size']} mau")
        print(f"  So lan cham nhanh GVADM: : {r['reached_gvadm_prefix']}")
        print(f"  So crash tim duoc        : {len(r['crashes'])}")
        for c in r["crashes"][:5]:
            print(f"    Lan {c['iteration']}: input={c['input']!r} -> {c['saved_to']}")
    print("\n--> Nhan xet: voi ngan sach thap (1000), fuzzer hop den thuong tim duoc 0 crash")
    print("    vi phai ghep ngau nhien dung 'GVADM:' + '!' + payload du dai (>=16). Tang ngan")
    print("    sach len 5000+ co the tinh co tim ra (nho dictionary ho tro), nhung cham hon han")
    print("    fuzzer hop trang (xem whitebox_fuzzer.py).")
