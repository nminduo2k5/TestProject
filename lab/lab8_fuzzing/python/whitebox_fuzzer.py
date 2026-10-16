"""
Lab 8 - Fuzzing Hop trang (White-box / Coverage-guided) - DuongUniversity Module 3
===================================================================================
Chuong 4: 4.6 Kiem thu hop trang (white-box fuzzing)

Y tuong (don gian hoa tu AFL - American Fuzzy Lop): moi khi mot dau vao moi lam
chuong trinh CHAY QUA MOT DONG LENH CHUA TUNG DUOC PHU truoc do ("new coverage"),
dau vao do duoc GIU LAI trong hang doi (queue) de tiep tuc dot bien - vi no da
chung minh la mot "huong di" co gia tri. Nguoc lai, input khong tao coverage moi
bi loai. Day la co che feedback loop bien fuzzing tu "mo mam" (blackbox) thanh
"co dinh huong" (whitebox) - hieu qua hon han khi lo hong nam sau nhieu lop nhanh
("GVADM:" -> "!" -> do dai > 15 trong tinh_tien_day_fuzz.c).

Do coverage tung lan chay RIENG LE: xoa .gcda truoc moi lan chay (khong tich luy),
goi llvm-cov gcov ngay sau de lay chinh xac tap dong lenh thuc thi trong lan do.
"""
from __future__ import annotations
import random
from collections import deque

from fuzz_common import (REBUILD_EVENTS, build_target, is_crash, load_seeds, mutate,
                         run_and_coverage, save_crash)


def havoc(s: str, rng: random.Random) -> str:
    """Giai doan 'havoc' cua AFL: XEP CHONG 1-4 phep dot bien lien tiep tren cung 1 chuoi
    thay vi chi 1 phep. Fuzzer coverage-guided thuc te lam vay de moi lan sinh con tao bien
    doi manh hon, tang toc 'leo' qua cac magic byte - day la mot phan cua loi the hop trang
    (ket hop VOI phan hoi coverage), khong phai thay the no."""
    n = rng.randint(1, 4)
    for _ in range(n):
        s = mutate(s, rng, growth=True)
    return s


def fuzz(iterations: int = 500, seed: int = 7, rebuild: bool = True) -> dict:
    if rebuild:
        build_target(with_coverage=True)
    rng = random.Random(seed)
    queue = deque(load_seeds())
    global_covered: set = set()
    crashes = []
    new_coverage_events = []

    it = 0
    while it < iterations and queue:
        parent = queue.pop()   # LIFO: uu tien khai thac SAU seed MOI phat hien (depth-first)
        for _ in range(8):     # energy scheduling don gian: 8 con / cha
            it += 1
            if it > iterations:
                break
            child = havoc(parent, rng)
            proc, lines = run_and_coverage(child)
            if proc is None:
                continue
            if is_crash(proc):
                path = save_crash("whitebox", len(crashes), child)
                crashes.append({"iteration": it, "input": child, "saved_to": path})
                continue   # input gay crash khong can dot bien tiep
            new_lines = lines - global_covered
            if new_lines:
                global_covered |= lines
                queue.append(child)   # "interesting": giu lai de dot bien tiep
                new_coverage_events.append({"iteration": it, "input": child, "new_lines": sorted(new_lines)})
        if not queue and it < iterations:   # het queue nhung con ngan sach -> nap lai seed
            queue.extend(load_seeds())

    return {"iterations_used": it, "seed": seed, "total_lines_covered": len(global_covered),
            "new_coverage_events": new_coverage_events, "crashes": crashes, "binary_rebuilds": len(REBUILD_EVENTS)}


if __name__ == "__main__":
    print("=================================================================")
    print("  LAB 8 - WHITE-BOX COVERAGE-GUIDED FUZZING (DuongUniversity Module 3)")
    print("=================================================================")
    r = fuzz(iterations=500, seed=7)
    print(f"\n[Ngan sach {r['iterations_used']} lan thu, seed=7]")
    print(f"  Tong so dong lenh da phu: {r['total_lines_covered']}")
    print(f"  Cac su kien 'coverage moi' (dan duong tim kiem tung buoc):")
    for e in r["new_coverage_events"]:
        print(f"    Lan {e['iteration']:3d}: input={e['input']!r:45s} -> phu them dong {e['new_lines']}")
    print(f"\n  So crash tim duoc: {len(r['crashes'])}")
    for c in r["crashes"]:
        print(f"    Lan {c['iteration']}: input={c['input']!r} -> {c['saved_to']}")
    if r["crashes"]:
        print(f"\n--> Fuzzer hop trang 'leo' qua tung lop nhanh (GVADM: -> GVADM:! -> do dai tran)")
        print(f"    nho phan hoi coverage, tim ra crash dau tien o lan thu {r['crashes'][0]['iteration']}.")
