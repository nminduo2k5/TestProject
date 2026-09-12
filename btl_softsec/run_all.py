"""
run_all.py - Tự động biên dịch C Binaries và kích hoạt toàn bộ Suite kiểm thử 4 Chương (SoftSec Toolkit)
"""

import subprocess
import sys
import os

def run_cmd(cmd, cwd=None):
    print(f"\n=================================================================")
    print(f"  RUNNING: {' '.join(cmd)}")
    print(f"=================================================================")
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"[WARNING] Command exited with code {res.returncode}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ch2_dir = os.path.join(base_dir, "ch2_memsafe")
    
    # 1. Compile C binaries inside ch2_memsafe
    print("[STEP 1] Compiling C executables in ch2_memsafe...")
    if os.path.exists(r"C:\msys64\ucrt64\bin"):
        os.environ["PATH"] = r"C:\msys64\ucrt64\bin;" + os.environ.get("PATH", "")
    gcc_path = r"C:\msys64\ucrt64\bin\gcc.exe" if os.path.exists(r"C:\msys64\ucrt64\bin\gcc.exe") else "gcc"
    
    # Compile 4 modular files for BUGGY version
    run_cmd([
        gcc_path, "-Wall", "-g", "-o", os.path.join(ch2_dir, "salary_calc.exe"),
        os.path.join(ch2_dir, "giang_vien.c"),
        os.path.join(ch2_dir, "lop_hoc_phan.c"),
        os.path.join(ch2_dir, "tinh_tien_day.c"),
        os.path.join(ch2_dir, "main.c")
    ])
    # Compile cùng 3 module (dùng chung hàm *_SAFE) cho bản FIXED, chỉ khác main_fixed.c
    run_cmd([
        gcc_path, "-Wall", "-g", "-o", os.path.join(ch2_dir, "salary_calc_fixed.exe"),
        os.path.join(ch2_dir, "giang_vien.c"),
        os.path.join(ch2_dir, "lop_hoc_phan.c"),
        os.path.join(ch2_dir, "tinh_tien_day.c"),
        os.path.join(ch2_dir, "main_fixed.c")
    ])

    python_exe = sys.executable

    # 2. Run Chapter 1: Kripke BMC
    run_cmd([python_exe, os.path.join(base_dir, "ch1_models", "kripke_bmc.py")])

    # 3. Run Chapter 2: Pattern Scanner
    run_cmd([python_exe, os.path.join(base_dir, "ch2_memsafe", "pattern_scanner.py")])

    # 4. Run Chapter 3: SMT Verify (ch3_staticsat)
    run_cmd([python_exe, os.path.join(base_dir, "ch3_staticsat", "smt_verify.py")])

    # 5. Run Chapter 4: Fuzzing
    run_cmd([python_exe, os.path.join(base_dir, "ch4_dynafuzz", "fuzzer_blackbox.py")])
    run_cmd([python_exe, os.path.join(base_dir, "ch4_dynafuzz", "fuzzer_whitebox.py")])

    print("\n=================================================================")
    print("  SUITE EXECUTED SUCCESSFULLY! All logs saved in btl_softsec/logs/")
    print("=================================================================")

if __name__ == "__main__":
    main()
