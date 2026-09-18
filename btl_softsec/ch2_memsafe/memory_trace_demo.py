"""
ch2_memsafe/memory_trace_demo.py - Chung minh THAT (khong suy luan) rang bo nho "chay" qua
tung buoc cua 1 luong E2E bat ky se bi tai su dung/bypass o dau, gay ra CWE-416 that.

Bien dich 2 phien ban cho ca 2 driver (VULN/main.c va SAFE/main_fixed.c):
  1. Plain gcc (ucrt64)   - chi in dia chi con tro that qua 7 buoc, KHONG phat hien loi
                            (chung minh: UAF co the "im lang" tren build thong thuong).
  2. Clang64 + AddressSanitizer - phat hien that heap-use-after-free bang cong cu doc lap,
                            khong phai tu bao cao.

Tu dong luu toan bo output that vao ../logs/memory_trace.log
"""

import subprocess
import shutil
import os
import sys

GCC = r"C:\msys64\ucrt64\bin\gcc.exe"
CLANG = r"C:\msys64\clang64\bin\clang.exe"
ASAN_DLL = r"C:\msys64\clang64\bin\libclang_rt.asan_dynamic-x86_64.dll"
LIBCXX_DLL = r"C:\msys64\clang64\bin\libc++.dll"

SRC_COMMON = ["giang_vien.c", "lop_hoc_phan.c", "tinh_tien_day.c"]


def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def section(title):
    print(f"\n=================================================================")
    print(f"  {title}")
    print(f"=================================================================")


def main():
    ch2_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(ch2_dir)

    section("BUOC 1/4: Bien dich PLAIN GCC (khong ASan) - VULN + FIXED")
    plain_vuln = os.path.join(ch2_dir, "trace_plain_vuln.exe")
    plain_fixed = os.path.join(ch2_dir, "trace_plain_fixed.exe")
    r1 = run([GCC, "-Wall", "-g", "-o", plain_vuln] + [os.path.join(ch2_dir, s) for s in SRC_COMMON] + [os.path.join(ch2_dir, "main.c")])
    print(r1.stdout, r1.stderr)
    r2 = run([GCC, "-Wall", "-g", "-o", plain_fixed] + [os.path.join(ch2_dir, s) for s in SRC_COMMON] + [os.path.join(ch2_dir, "main_fixed.c")])
    print(r2.stdout, r2.stderr)

    section("BUOC 2/4: Bien dich CLANG64 + ADDRESSSANITIZER - VULN + FIXED")
    asan_vuln = os.path.join(ch2_dir, "trace_asan_vuln.exe")
    asan_fixed = os.path.join(ch2_dir, "trace_asan_fixed.exe")
    if os.path.exists(CLANG):
        r3 = run([CLANG, "-fsanitize=address", "-g", "-O0", "-o", asan_vuln] + [os.path.join(ch2_dir, s) for s in SRC_COMMON] + [os.path.join(ch2_dir, "main.c")])
        print(r3.stdout, r3.stderr)
        r4 = run([CLANG, "-fsanitize=address", "-g", "-O0", "-o", asan_fixed] + [os.path.join(ch2_dir, s) for s in SRC_COMMON] + [os.path.join(ch2_dir, "main_fixed.c")])
        print(r4.stdout, r4.stderr)
        if os.path.exists(ASAN_DLL):
            shutil.copy2(ASAN_DLL, ch2_dir)
        if os.path.exists(LIBCXX_DLL):
            shutil.copy2(LIBCXX_DLL, ch2_dir)
        asan_available = True
    else:
        print(f"[CANH BAO] Khong tim thay {CLANG} - bo qua phan ASan (chi con bang chung plain gcc).")
        asan_available = False

    section("BUOC 3/4: Chay PLAIN build - VULN (khong ASan, chi doi chieu dia chi)")
    rv = run([plain_vuln, "e2e_memory_trace"])
    print(rv.stdout)
    print(rv.stderr)
    print(f"--> Exit code: {rv.returncode} (0 = chay het, KHONG crash, du da doc vung nho da free!)")

    section("BUOC 3b/4: Chay PLAIN build - FIXED (khong ASan, doi chung)")
    rvf = run([plain_fixed, "e2e_memory_trace"])
    print(rvf.stdout)
    print(rvf.stderr)
    print(f"--> Exit code: {rvf.returncode}")

    if asan_available:
        section("BUOC 4/4: Chay ASAN build - VULN (phat hien that bang cong cu doc lap)")
        env = dict(os.environ)
        env["ASAN_OPTIONS"] = "halt_on_error=1"
        ra = run([asan_vuln, "e2e_memory_trace"], env=env)
        print(ra.stdout)
        print(ra.stderr)
        print(f"--> Exit code: {ra.returncode} (khac 0 = ASan da CHAN chuong trinh vi phat hien heap-use-after-free THAT)")

        section("BUOC 4b/4: Chay ASAN build - FIXED (phai chay sach, khong loi)")
        raf = run([asan_fixed, "e2e_memory_trace"], env=env)
        print(raf.stdout)
        print(raf.stderr)
        print(f"--> Exit code: {raf.returncode} (0 = ASan xac nhan KHONG co loi memory-safety nao tren ban da vá)")

    # Don dep file .exe/.dll tam (khong can giu lai, chi giu log)
    for f in [plain_vuln, plain_fixed, asan_vuln, asan_fixed,
              os.path.join(ch2_dir, "libclang_rt.asan_dynamic-x86_64.dll"),
              os.path.join(ch2_dir, "libc++.dll")]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except OSError:
                pass


class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        try:
            self.terminal.write(message)
        except UnicodeEncodeError:
            self.terminal.write(message.encode('ascii', errors='replace').decode('ascii'))
        self.log.write(message)
        self.terminal.flush()
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "memory_trace.log")
    sys.stdout = TeeLogger(log_file)
    print("=================================================================")
    print("  BANG CHUNG DONG (DYNAMIC): TRACE DIA CHI BO NHO THAT QUA 7 BUOC E2E")
    print("  (bo sung cho Chuong 2 - khong thay the pattern_scanner.py static)")
    print("=================================================================")
    main()
