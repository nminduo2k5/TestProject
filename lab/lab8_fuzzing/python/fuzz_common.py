"""
Lab 8 - Ha tang chung cho 2 fuzzer (DuongUniversity - Module 3 Tinh tien day)
=============================================================================
Gom cac phan dung chung giua fuzzer hop den va hop trang:
  - Bien dich fuzz target bang Clang clang64 (+ASan +coverage), bundle DLL runtime.
  - Chay target, lay coverage TUNG LAN CHAY RIENG LE qua llvm-cov gcov.
  - Cac phep dot bien (mutation) va tu dien token (dictionary).

GHI CHU MOI TRUONG (giong Lab 3/Lab 6): GCC cua MSYS2 UCRT64 KHONG kem libasan
tren Windows -> dung Clang cua moi truong MSYS2 clang64 (co compiler-rt + ho tro
--coverage, doc bang llvm-cov gcov). Clang dat ten file coverage theo ten file
thuc thi: tinh_tien_day_fuzz.exe-tinh_tien_day_fuzz.gcda.
"""
from __future__ import annotations
import os
import random
import re
import string
import subprocess
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C_DIR = os.path.join(BASE, "c")
SEED_DIR = os.path.join(BASE, "seed_corpus")
CRASH_DIR = os.path.join(BASE, "crashes")

SRC = "tinh_tien_day_fuzz.c"
EXE = "tinh_tien_day_fuzz.exe"
GCDA = f"{EXE}-tinh_tien_day_fuzz.gcda"
GCNO = f"{EXE}-tinh_tien_day_fuzz.gcno"
GCOV = f"{SRC}.gcov"

CLANG64_BIN = r"C:\msys64\clang64\bin"
CLANG = os.path.join(CLANG64_BIN, "clang.exe")
LLVM_COV = os.path.join(CLANG64_BIN, "llvm-cov.exe")
RUNTIME_DLLS = [
    os.path.join(CLANG64_BIN, "libclang_rt.asan_dynamic-x86_64.dll"),
    os.path.join(CLANG64_BIN, "libc++.dll"),
]
CC = CLANG if os.path.exists(CLANG) else "gcc"

# Tu dien token: mo phong kien thuc "chung" mot tester hop den co the co tu tai lieu
# API noi bo (prefix GV:/LHP:), KHONG phai thong tin lay tu doc ma nguon C. Magic
# prefix "GVADM:" va co kich hoat "!" co mat nhu cac token roi rac - fuzzer phai tu
# GHEP chung dung thu tu + du dai moi cham duoc lo hong.
DICTIONARY = ["GVADM:", "GV:", "LHP:", "!", "A" * 36]
_MUT_CHARS = string.ascii_letters + string.digits + ":,!"


def _asan_env() -> dict:
    env = dict(os.environ)
    env["PATH"] = CLANG64_BIN + os.pathsep + env.get("PATH", "")
    return env


def build_target(with_coverage: bool = True):
    """Bien dich fuzz target bang Clang clang64 + ASan (+coverage neu can)."""
    for f in os.listdir(C_DIR):
        if f.endswith((".gcda", ".gcno", ".gcov")):
            os.remove(os.path.join(C_DIR, f))
    flags = ["-g", "-fsanitize=address", "-Wall", "-Wextra"]
    if with_coverage:
        flags.append("--coverage")
    subprocess.run([CC] + flags + ["-o", EXE, SRC], cwd=C_DIR, check=True)
    for dll in RUNTIME_DLLS:
        if os.path.exists(dll):
            import shutil
            shutil.copy2(dll, C_DIR)


def load_seeds() -> list[str]:
    seeds = []
    for fname in sorted(os.listdir(SEED_DIR)):
        with open(os.path.join(SEED_DIR, fname), encoding="utf-8") as f:
            seeds.append(f.read().strip())
    return seeds


def mutate(s: str, rng: random.Random, growth: bool = False) -> str:
    """Dot bien ngau nhien 1 chuoi. growth=True them phep 'noi khoi' (append_block)
    giup tang do dai nhanh - huu ich cho fuzzer hop trang cham nguong tran som hon."""
    chars = list(s)
    ops = ["insert_char", "delete_char", "replace_char", "splice_token", "splice_token"]
    if growth:
        ops += ["append_block"]
    op = rng.choice(ops)
    if op == "insert_char":
        chars.insert(rng.randint(0, len(chars)), rng.choice(_MUT_CHARS))
    elif op == "delete_char" and chars:
        del chars[rng.randint(0, len(chars) - 1)]
    elif op == "replace_char" and chars:
        chars[rng.randint(0, len(chars) - 1)] = rng.choice(_MUT_CHARS)
    elif op == "splice_token":
        pos = rng.randint(0, len(chars))
        chars[pos:pos] = list(rng.choice(DICTIONARY))
    elif op == "append_block":
        n = rng.randint(5, 30)
        chars += [rng.choice(string.ascii_uppercase) for _ in range(n)]
    return "".join(chars)


REBUILD_EVENTS: list[str] = []   # ghi nhan neu binary bi xoa giua chung (xem REPORT.md)


def _ensure_binary():
    """Tren may thuc hanh, binary doi khi bi mot tien trinh ngoai (phan mem bao mat) xoa giua
    luc fuzz. Khi do bien dich lai (KHONG xoa .gcno de giu dong bo coverage) va ghi nhan su kien."""
    exe = os.path.join(C_DIR, EXE)
    if os.path.exists(exe):
        return
    REBUILD_EVENTS.append(time.strftime("%H:%M:%S"))
    print(f"  [CANH BAO] {EXE} bi xoa boi tien trinh ngoai - bien dich lai (lan {len(REBUILD_EVENTS)})", flush=True)
    subprocess.run([CC, "-g", "-fsanitize=address", "-Wall", "-Wextra", "--coverage", "-o", EXE, SRC],
                   cwd=C_DIR, check=True)


def run_target(input_str: str, timeout: int = 5) -> subprocess.CompletedProcess | None:
    _ensure_binary()
    try:
        return subprocess.run([os.path.join(C_DIR, EXE), input_str], cwd=C_DIR,
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=_asan_env(), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None


def is_crash(proc: subprocess.CompletedProcess | None) -> bool:
    return proc is not None and proc.returncode != 0 and "AddressSanitizer" in (proc.stderr or "")


def run_and_coverage(input_str: str, timeout: int = 5):
    """Chay 1 lan co lap coverage (xoa .gcda truoc), tra ve (proc, frozenset dong da phu).
    Lan crash khong sinh .gcda (ASan abort truoc khi flush) -> tap dong rong, nhung van
    phat hien duoc crash qua is_crash()."""
    gcda = os.path.join(C_DIR, GCDA)
    if os.path.exists(gcda):
        os.remove(gcda)
    proc = run_target(input_str, timeout)
    covered = set()
    if proc is not None and os.path.exists(gcda):
        subprocess.run([LLVM_COV, "gcov", GCDA], cwd=C_DIR, capture_output=True, text=True, env=_asan_env())
        gpath = os.path.join(C_DIR, GCOV)
        if os.path.exists(gpath):
            with open(gpath, encoding="utf-8", errors="ignore") as f:
                for raw in f:
                    m = re.match(r"\s*(\S+):\s*(\d+):", raw)
                    if m and m.group(1) not in ("-", "", "#####", "====="):
                        covered.add(int(m.group(2)))
    return proc, frozenset(covered)


def save_crash(kind: str, idx: int, content: str) -> str:
    os.makedirs(CRASH_DIR, exist_ok=True)
    path = os.path.join(CRASH_DIR, f"{kind}_crash_{idx}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
