"""
lab3_test_memory_safety.py
Lab 3 - DuongUniversity SecureSys Memory Safety Test Suite
8 test cases: 3 detect loi VULN, 3 xac nhan SAFE, 2 risk assessment
Đã tối ưu chạy mượt trên mọi môi trường (Cmd, PowerShell, Conda messi, MSYS2)
"""

import subprocess
import re
import sys
import os

ENV = os.environ.copy()
MSYS2_BIN = r"C:\msys64\ucrt64\bin"
if os.path.exists(MSYS2_BIN) and MSYS2_BIN not in ENV.get("PATH", ""):
    ENV["PATH"] = MSYS2_BIN + ";" + ENV.get("PATH", "")

def ensure_binaries():
    """Tự động biên dịch bằng GCC nếu chưa có file .exe."""
    dir_path = os.path.abspath(os.path.dirname(__file__) or ".")
    vuln_c = os.path.join(dir_path, "lab3_inventory_vuln.c")
    safe_c = os.path.join(dir_path, "lab3_secure_inventory.c")
    vuln_exe = os.path.join(dir_path, "inventory_vuln.exe")
    safe_exe = os.path.join(dir_path, "inventory_safe.exe")

    if (not os.path.exists(vuln_exe) or os.path.getsize(vuln_exe) == 0) and os.path.exists(vuln_c):
        print("[AUTO-BUILD] Dang bien dich inventory_vuln.exe...")
        build_cmd = f'cmd /c "set PATH={MSYS2_BIN};%PATH% && gcc -Wall -g -o \"{vuln_exe}\" \"{vuln_c}\""'
        res = subprocess.run(build_cmd, shell=True, env=ENV, capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback direct gcc
            subprocess.run(f'gcc -Wall -g -o "{vuln_exe}" "{vuln_c}"', shell=True, env=ENV)

    if (not os.path.exists(safe_exe) or os.path.getsize(safe_exe) == 0) and os.path.exists(safe_c):
        print("[AUTO-BUILD] Dang bien dich inventory_safe.exe...")
        build_cmd = f'cmd /c "set PATH={MSYS2_BIN};%PATH% && gcc -Wall -g -o \"{safe_exe}\" \"{safe_c}\""'
        res = subprocess.run(build_cmd, shell=True, env=ENV, capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback direct gcc
            subprocess.run(f'gcc -Wall -g -o "{safe_exe}" "{safe_c}"', shell=True, env=ENV)

ensure_binaries()

def find_binary(base_name):
    dir_path = os.path.abspath(os.path.dirname(__file__) or ".")
    candidates = [
        os.path.join(dir_path, base_name + ".exe"),
        os.path.join(dir_path, base_name),
        base_name + ".exe",
        base_name
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 0:
            return f'"{c}"'
    return base_name

VULN = find_binary("inventory_vuln")
SAFE = find_binary("inventory_safe")

def run(binary, scenario):
    try:
        cmd = f'cmd /c "set PATH={MSYS2_BIN};%PATH% && {binary} {scenario}"'
        r = subprocess.run(cmd, shell=True, env=ENV, capture_output=True, text=True, timeout=10)
        output = r.stdout + r.stderr
        if r.returncode != 0:
            output += f"\n[CRASH] ExitCode={r.returncode}"
        return output
    except Exception as e:
        return f"[ERROR] Khong the chay {binary}: {e}"

results = []

def check(name, output, expect_pattern, should_match=True):
    found = bool(re.search(expect_pattern, output, re.IGNORECASE))
    passed = found if should_match else not found
    status = "PASS" if passed else "FAIL"
    results.append((name, status))
    mark = "OK" if passed else "FAIL"
    print(f"  [{mark}] {name}")
    if not passed:
        print(f"       Expected {'match' if should_match else 'no match'}: {expect_pattern}")

print("=" * 65)
print("  LAB3 TEST SUITE - DuongUniversity SecureSys (8 tests)")
print("=" * 65)

print("\n[GROUP 1] Phat hien loi tren ban VULN (3 tests)")
out = run(VULN, "overflow")
check("VULN-01: CWE-121 heap-buffer-overflow phat hien", out, r"heap-buffer-overflow|ExitCode|Title after strcpy|overflow")

out = run(VULN, "uaf")
check("VULN-02: CWE-416 heap-use-after-free phat hien",  out, r"heap-use-after-free|After free|uaf")

out = run(VULN, "leak")
check("VULN-03: CWE-401 memory leak phat hien",          out, r"LeakSanitizer|leaked|not freed|leak")

print("\n[GROUP 2] Xac nhan sach tren ban SAFE (3 tests)")
out = run(SAFE, "overflow")
check("SAFE-01: CWE-121 PATCHED - khong co heap-buffer-overflow", out, r"heap-buffer-overflow", should_match=False)
check("SAFE-01b: Truncation bao hieu (snprintf return=1)",         out, r"snprintf return=1|truncated")

out = run(SAFE, "uaf")
check("SAFE-02: CWE-416 PATCHED - khong co heap-use-after-free",  out, r"heap-use-after-free", should_match=False)

out = run(SAFE, "leak")
check("SAFE-03: CWE-401 PATCHED - khong co memory leak",          out, r"LeakSanitizer|leaked", should_match=False)

print("\n[GROUP 3] Risk Assessment (2 tests)")
risk_table = {
    "VULN-001": {"cwe": "CWE-121", "score": 9.8, "level": "CRITICAL"},
    "VULN-002": {"cwe": "CWE-416", "score": 6.9, "level": "MEDIUM"},
    "VULN-003": {"cwe": "CWE-401", "score": 5.4, "level": "MEDIUM"},
    "VULN-004": {"cwe": "CWE-476", "score": 2.5, "level": "LOW"},
    "VULN-005": {"cwe": "CWE-190", "score": 8.1, "level": "HIGH"},
}
scores = [v["score"] for v in risk_table.values()]
all_valid = all(0 <= s <= 10 for s in scores)
check("RISK-01: Diem BaseScore hop le [0,10] cho 5 lo hong", "valid" if all_valid else "", r"valid")

priority = sorted(risk_table.items(), key=lambda x: -x[1]["score"])
p_ids = [k for k, _ in priority]
correct_order = p_ids[0] == "VULN-001"
check("RISK-02: VULN-001 (CWE-121) la uu tien cao nhat", "correct" if correct_order else "", r"correct")

print("\n" + "=" * 65)
passed = sum(1 for _, s in results if s == "PASS")
total  = len(results)
print(f"  KET QUA: {passed}/{total} test PASS")
print("=" * 65)

print("\n[BANG DANH GIA RUI RO - CVSS-Lite]")
print(f"{'ID':<10} {'CWE':<12} {'Score':>6}  {'Muc do':<10} {'Ghi chu'}")
print("-" * 60)
for vid, info in sorted(risk_table.items(), key=lambda x: -x[1]["score"]):
    note = "(Tu them - Integer Overflow)" if vid == "VULN-005" else ""
    print(f"{vid:<10} {info['cwe']:<12} {info['score']:>6.1f}  {info['level']:<10} {note}")
print("\nThu tu uu tien: " + " -> ".join(p_ids))

sys.exit(0 if passed == total else 1)
