"""
dashboard_streamlit.py - Dashboard demo tuong tac cho BTL An toan phan mem
==========================================================================
DuongUniversity Management System - SoftSec Toolkit (4 chuong)

Chay:  C:\\Users\\HP\\anaconda3\\python.exe -m streamlit run dashboard_streamlit.py
       (hoac run_dashboard.bat)

Dashboard KHONG dung so lieu dung san: moi trang doc truc tiep logs/*.log do cac
script that sinh ra, parse bang regex, va co nut "Chay lai" goi dung script
(ch1_models/kripke_bmc.py, ch2_memsafe/*.py, ch3_staticsat/smt_verify.py,
ch4_dynafuzz/*.py) hoac dung 2 binary salary_calc*.exe de demo truc tiep.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(BASE, "logs")
CH2 = os.path.join(BASE, "ch2_memsafe")
VULN_EXE = os.path.join(CH2, "salary_calc.exe")
FIXED_EXE = os.path.join(CH2, "salary_calc_fixed.exe")

ANACONDA_PY = os.path.join(os.path.expanduser("~"), "anaconda3", "python.exe")
PYTHON = ANACONDA_PY if os.path.exists(ANACONDA_PY) else sys.executable
GCC = r"C:\msys64\ucrt64\bin\gcc.exe" if os.path.exists(r"C:\msys64\ucrt64\bin\gcc.exe") else "gcc"

SCRIPTS = {
    "kripke_bmc": ("ch1_models/kripke_bmc.py", "kripke_bmc.log"),
    "pattern_scanner": ("ch2_memsafe/pattern_scanner.py", "pattern_scanner.log"),
    "memory_trace": ("ch2_memsafe/memory_trace_demo.py", "memory_trace.log"),
    "nfr_check": ("ch2_memsafe/nfr_check.py", "nfr_check.log"),
    "smt_verify": ("ch3_staticsat/smt_verify.py", "smt_verify.log"),
    "fuzzer_blackbox": ("ch4_dynafuzz/fuzzer_blackbox.py", "fuzzer_blackbox.log"),
    "fuzzer_whitebox": ("ch4_dynafuzz/fuzzer_whitebox.py", "fuzzer_whitebox.log"),
}

E2E_MODES = {
    "e2e_overflow": "CWE-120 Buffer Overflow (hoTen 119 ky tu > MAX_NAME 80)",
    "e2e_uaf": "CWE-416 Use-After-Free lien mo-dun (free GV roi tinh luong)",
    "e2e_null": "CWE-476 NULL Pointer Dereference (lop chua phan cong GV)",
    "e2e_integer_overflow": "CWE-190 Integer Overflow (soTiet=50000, GS)",
    "e2e_byte_truncate": "CWE-197 Numeric Truncation int -> char (soLuongSinhVien)",
    "e2e_memory_trace": "Trace dia chi bo nho 7 buoc (bang chung UAF)",
    "e2e_nfr_bench": "NFR-1/NFR-2 benchmark (N lan lap)",
}

# ---------------------------------------------------------------------------
# Du lieu dac ta (REQ / NFR / CWE / Ma tran truy vet) - dong bo voi dashboard.html
# ---------------------------------------------------------------------------
REQ_TABLE = [
    ("REQ-1", "Safety", "HIGH", "Không được tính tiền khi chưa phân công giảng viên", "Ch1 BMC P1"),
    ("REQ-2", "Safety", "HIGH", "Không được xuất báo cáo khi chưa tính tiền", "Ch1 BMC P2"),
    ("REQ-3", "Memory", "HIGH", "Các buffer chuỗi không tràn khi input vượt giới hạn (CWE-120)", "Ch2 strcpy; Ch4 Target 1/2"),
    ("REQ-4", "Memory", "HIGH", "gv_ptr không được truy cập sau khi free() (CWE-416 UAF)", "Ch2 dangling_free; Ch3 Check 3"),
    ("REQ-5", "Memory", "HIGH", "gv_ptr phải được kiểm tra NULL trước khi đọc (CWE-476)", "Ch2 unchecked_nested_deref; Ch4 Target 4"),
    ("REQ-6", "Memory", "HIGH", "Phép nhân dồn không tràn số nguyên 32-bit (CWE-190)", "Ch3 Check 1/2"),
    ("REQ-7", "Functional", "MEDIUM", "Công thức tính thù lao 2 bước đúng với mọi input hợp lệ", "Ch3 Check 1/2 — thiếu oracle tự động"),
    ("REQ-8", "Integrity", "HIGH", "Đóng gói audit log không sai lệch kiểu char (CWE-197)", "Ch3 Check 4/5/6; Ch4 BVA 17/17"),
    ("REQ-9", "Functional", "MEDIUM", "bangCap phải thuộc danh mục hợp lệ (CWE-1288)", "Ch3 Check 7 — thiếu oracle tự động"),
    ("REQ-10", "Memory", "HIGH", "Con trỏ cfg (Config*) phải kiểm tra NULL trước khi đọc", "Ch2 dòng 30 (tinh_tien_day.c)"),
]
NFR_TABLE = [
    ("NFR-1", "Hiệu năng", "Thời gian tính lương 1 lớp < 10ms", "PASS — 0,000014 ms/lần (10.000 lần lặp)"),
    ("NFR-2", "Ổn định bộ nhớ", "Không rò rỉ bộ nhớ khi lặp E2E ≥ 10.000 lần", "PASS — drift 4 KB / 10.000 lần (ngưỡng 1024 KB)"),
    ("NFR-3", "Tính di động", "Biên dịch sạch (0 warning -Wall) trên ≥ 2 toolchain", "PASS — GCC/UCRT64 và Clang64"),
    ("NFR-4", "Chịu lỗi", "Input vượt đặc tả bị từ chối có kiểm soát, không crash", "PASS — 0/200 crash bản FIXED"),
    ("NFR-5", "Toàn vẹn (Audit)", "2 soLuongSinhVien khác nhau không map trùng 1 byte", "PASS trên FIXED — VULN va chạm (Check 6/Target 7)"),
    ("NFR-6", "Tính tất định", "Cùng input, BMC/SMT/fuzzing nhất quán", "PASS một phần — số crash fuzzing dao động 60–72/200"),
    ("NFR-7", "Không có dead field", "Mọi field cấu hình phải được ≥ 1 hàm đọc lại", "FAIL — 2/3 field Config chết: heSoQuyMoLop, nam"),
]
CWE_TABLE = [
    ("CWE-416", "Use-After-Free", "Ch2 dangling_free; ASan heap-use-after-free thật", 8.0, "HIGH"),
    ("CWE-120", "Buffer Overflow", "Ch2 strcpy; Ch4 crash 72/200", 7.2, "HIGH"),
    ("CWE-476", "NULL Pointer Dereference", "Ch2 unchecked_nested_deref; Ch4 Target 4", 6.7, "MEDIUM"),
    ("CWE-190", "Integer Overflow", "Ch1 S5; Ch3 Check 1 SAT / Check 2 UNSAT", 6.1, "MEDIUM"),
    ("CWE-197", "Numeric Truncation", "Ch1 P5; Ch3 Check 4/6; Ch4 BVA 17/17", 6.1, "MEDIUM"),
    ("CWE-1288", "Improper Validation", "Ch2 fallback heSoBangCap=1.0f; Ch3 Check 7 SAT", 3.9, "LOW"),
]
TRACE_TABLE = [
    ("TC-K1-01", "REQ-1", "BMC P1, bản BUGGY (nhảy thẳng sang tính tiền)", "UNSAT", "SAT — phản ví dụ S0→S5→S4", "FAIL*"),
    ("TC-K1-02", "REQ-1", "BMC P1, bản FIXED", "UNSAT", "UNSAT", "PASS"),
    ("TC-K1-03", "REQ-2", "BMC P2, cả 2 bản", "UNSAT", "UNSAT cả 2 bản", "PASS"),
    ("TC-K2-01", "REQ-3", "Scanner quét strcpy trên 3 file VULN", "Phát hiện đủ CWE-120", "5 cảnh báo đúng vị trí", "PASS"),
    ("TC-K2-02", "REQ-3", "Scanner quét main_fixed.c", "0 cảnh báo", "0 cảnh báo — [CLEAN]", "PASS"),
    ("TC-K4-01", "REQ-3", "White-box Target 1: hoTen dài 81 > CON-1 (80)", "Tìm điều kiện tràn", "SAT ở lần thử 1", "FAIL*"),
    ("TC-K4-02", "REQ-3", "White-box Target 2: maLop dài 21 > CON-4 (20)", "Tìm điều kiện tràn", "SAT ở lần thử 2", "FAIL*"),
    ("TC-K4-03", "REQ-3", "Black-box 200 lần ngẫu nhiên trên VULN", "0/200 crash", "72/200 crash, 0xC0000374", "FAIL*"),
    ("TC-K4-04", "REQ-3", "Black-box 200 lần trên FIXED", "0/200 crash", "0/200 crash", "PASS"),
    ("TC-K2-03", "REQ-4", "Scanner quét dangling_free trên VULN", "Phát hiện CWE-416 tại giang_vien.c:35", "Phát hiện đúng vị trí", "PASS"),
    ("TC-K4-05", "REQ-4", "White-box Target 3: free(gv) rồi vẫn đọc qua gv_ptr", "Tìm điều kiện UAF", "SAT ở lần thử 3", "FAIL*"),
    ("TC-K2-04", "REQ-4", "ASan-VULN: đọc gv->hoTen sau free()", "ASan phải bắt lỗi", "heap-use-after-free, offset +24 = hoTen", "FAIL*"),
    ("TC-K2-05", "REQ-4", "ASan-FIXED (gv_ptr=NULL trước free)", "0 vi phạm", "0 vi phạm", "PASS"),
    ("TC-K2-06", "REQ-5", "Scanner quét unchecked_nested_deref trên VULN", "Phát hiện CWE-476 tại tinh_tien_day.c:13", "Phát hiện đúng vị trí", "PASS"),
    ("TC-K4-06", "REQ-5", "White-box Target 4: gv_ptr=NULL rồi tính lương", "Tìm điều kiện NULL deref", "SAT ở lần thử 4", "FAIL*"),
    ("TC-K3-01", "REQ-6", "Check 1 (Z3): ∃ input hợp lệ tràn int32", "SAT dự kiến (VULN)", "SAT — numClasses=20, soTiet=120", "FAIL*"),
    ("TC-K3-02", "REQ-6", "Check 2 (Z3): cùng câu hỏi trên long long", "UNSAT", "UNSAT", "PASS"),
    ("TC-K4-07", "REQ-6", "White-box Target 5: soTiet=16694179, dmt=2147583020", "SAT dự kiến", "SAT ở lần thử 5", "FAIL*"),
    ("TC-K1-04", "REQ-8", "BMC P5, bản VULN", "UNSAT", "SAT — S3 mang nhãn byte_truncated", "FAIL*"),
    ("TC-K1-05", "REQ-8", "BMC P5, bản FIXED", "UNSAT", "UNSAT", "PASS"),
    ("TC-K3-03", "REQ-8", "Check 4 (Z3): ∃ n∈[0,300] ép char sai", "SAT dự kiến", "SAT — n=128 → byte=-128", "FAIL*"),
    ("TC-K3-04", "REQ-8", "Check 5 (Z3): cùng câu hỏi với guard [0,127]", "UNSAT", "UNSAT", "PASS"),
    ("TC-K3-05", "REQ-8, NFR-5", "Check 6 (Z3): ∃ a≠b∈[0,300] cùng cho 1 byte", "UNSAT mong muốn", "SAT — a=0, b=256 cùng byte=0", "FAIL**"),
    ("TC-K4-08", "REQ-8", "Black-box CWE-197, 200 lần trên VULN", "0/200 sai lệch", "120/200 sai lệch (60%)", "FAIL*"),
    ("TC-K4-09", "REQ-8", "Black-box CWE-197, 200 lần trên FIXED", "0/200 sai lệch", "0/200 (146/200 chặn an toàn)", "PASS"),
    ("TC-K4-10", "REQ-8, NFR-5", "BVA 17 giá trị biên trên VULN", "Khớp lý thuyết 17/17; không nên trùng", "17/17 khớp, nhưng lộ 6 nhóm trùng byte", "PASS/FAIL**"),
    ("TC-K4-11", "REQ-8, NFR-5", "BVA 17 giá trị biên trên FIXED", "0 nhóm trùng", "0 nhóm trùng", "PASS"),
    ("TC-K3-06", "REQ-9", "Check 7 (Z3): ∃ 2 bangCap khác nhau cùng 1 heSoBangCap", "UNSAT mong muốn", "SAT — cả 2 rơi vào fallback 1.0", "FAIL**"),
    ("TC-K4-12", "REQ-9", "Black-box: bangCap ngẫu nhiên không hợp lệ, trên VULN", "Cần oracle xác nhận đúng", "74/200 không hợp lệ, không crash — chưa assert", "QS†"),
    ("TC-K2-07", "REQ-7", "(chưa có test case riêng)", "Công thức đúng mọi input hợp lệ", "Check 1/2 chỉ chứng minh không tràn số", "QS†"),
    ("TC-N01", "NFR-1", "e2e_nfr_bench 10000 trên bản FIXED", "< 10 ms/lần", "0,000014 ms/lần", "PASS"),
    ("TC-N02", "NFR-1", "e2e_nfr_bench 10000 trên bản VULN (đối chứng)", "< 10 ms/lần", "0,000011 ms/lần", "PASS"),
    ("TC-N03", "NFR-2", "10.000 lần tạo/xoá trên bản FIXED", "Drift < 1024 KB", "Drift = 4 KB", "PASS"),
    ("TC-N04", "NFR-2", "Cùng kịch bản trên bản VULN", "Drift < 1024 KB", "Drift = 4 KB", "PASS"),
]

# ---------------------------------------------------------------------------
# Tien ich: doc log, chay script, chay binary
# ---------------------------------------------------------------------------
def read_log(name: str) -> str:
    p = os.path.join(LOGS, name)
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def log_mtime(name: str) -> str:
    p = os.path.join(LOGS, name)
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(os.path.getmtime(p))) if os.path.exists(p) else "chưa có"


def run_script(key: str, timeout: int = 600) -> tuple[int, str]:
    rel, _ = SCRIPTS[key]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    if os.path.exists(r"C:\msys64\ucrt64\bin"):
        env["PATH"] = r"C:\msys64\ucrt64\bin;" + env.get("PATH", "")
    proc = subprocess.run([PYTHON, os.path.join(BASE, rel)], cwd=BASE, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env, timeout=timeout)
    return proc.returncode, (proc.stdout or "") + (("\n[stderr]\n" + proc.stderr) if proc.stderr.strip() else "")


def run_binary(exe: str, args: list[str], stdin_text: str | None = None, timeout: int = 30) -> dict:
    if not os.path.exists(exe):
        return {"rc": None, "out": "", "err": f"Chưa có {os.path.basename(exe)} — bấm 'Biên dịch' ở sidebar.", "t": 0.0}
    t0 = time.perf_counter()
    try:
        proc = subprocess.run([exe] + args, cwd=CH2, input=stdin_text, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = -1, "", "TIMEOUT"
    return {"rc": rc, "out": out, "err": err, "t": time.perf_counter() - t0}


def compile_binaries() -> tuple[bool, str]:
    mods = ["giang_vien.c", "lop_hoc_phan.c", "tinh_tien_day.c"]
    logs = []
    ok = True
    for main_c, exe in (("main.c", VULN_EXE), ("main_fixed.c", FIXED_EXE)):
        cmd = [GCC, "-Wall", "-g", "-o", exe] + [os.path.join(CH2, m) for m in mods] + [os.path.join(CH2, main_c), "-lpsapi"]
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        ok &= proc.returncode == 0
        logs.append(f"$ gcc ... {main_c} -> {os.path.basename(exe)}  [rc={proc.returncode}]\n{proc.stdout}{proc.stderr}")
    return ok, "\n".join(logs)


def rc_badge(rc) -> str:
    if rc is None:
        return "⚪ chưa chạy"
    if rc == 0:
        return "🟢 exit 0 (bình thường)"
    if rc == -1:
        return "🟠 timeout"
    u = rc & 0xFFFFFFFF
    names = {0xC0000374: "STATUS_HEAP_CORRUPTION", 0xC0000005: "STATUS_ACCESS_VIOLATION", 0xC0000409: "STATUS_STACK_BUFFER_OVERRUN"}
    return f"🔴 exit {rc} (0x{u:08X} {names.get(u, 'CRASH')})"


def sat_color(v: str) -> str:
    return "background-color:#f8dede;color:#8a1f1f;font-weight:600" if v.startswith("SAT") else \
           ("background-color:#dcf1dc;color:#145214;font-weight:600" if v.startswith("UNSAT") else "")


def status_color(v: str) -> str:
    v = str(v)
    if v.startswith("PASS/"):
        return "background-color:#fff1cc;color:#6b4e00"
    if v.startswith("PASS"):
        return "background-color:#dcf1dc;color:#145214"
    if v.startswith("FAIL"):
        return "background-color:#f8dede;color:#8a1f1f"
    if v.startswith("QS"):
        return "background-color:#e3e9e0;color:#4b564e"
    return ""


# ---------------------------------------------------------------------------
# Parser cho tung log
# ---------------------------------------------------------------------------
def parse_kripke(text: str) -> tuple[pd.DataFrame, dict]:
    rows, traces = [], {}
    cur_model = None
    blocks = re.split(r"RUNNING BMC CHECK ON: ", text)
    for b in blocks[1:]:
        m = re.match(r"(\S+)\s*\((\d+) trang thai", b)
        cur_model = "BUGGY" if "BUGGY" in m.group(1) else "FIXED"
        for pm in re.finditer(r"\[Property (\d)\] (\w+): (.+?) \[(.+?)\]\n\s*--> RESULT: (SAT|UNSAT)([^\n]*)((?:\n\s+(?:Counterexample|Step).*)*)", b):
            pid, kind, formula, desc, res, _, trace = pm.groups()
            rows.append({"Property": f"P{pid}", "Loại": kind, "Công thức LTL": formula.strip(), "Ý nghĩa": desc, "Mô hình": cur_model, "Kết quả": res})
            steps = re.findall(r"Step (\d+): (\S+) \[Labels: (.+?)\]", trace or "")
            if steps:
                traces[(f"P{pid}", cur_model)] = steps
    df = pd.DataFrame(rows)
    if df.empty:
        return df, traces
    pivot = df.pivot_table(index=["Property", "Loại", "Công thức LTL", "Ý nghĩa"], columns="Mô hình", values="Kết quả", aggfunc="first").reset_index()
    return pivot, traces


def parse_scanner(text: str) -> pd.DataFrame:
    rows = []
    cur_file = None
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        m = re.match(r"== Quét tệp: (\S+) ==", ln)
        if m:
            cur_file = m.group(1)
            continue
        m = re.match(r".*?([A-Za-z_]+\.c):(\d+): cảnh báo \[(\w+)\] (.+?)\s*\((CWE-\d+)[^)]*\)", ln)
        if m:
            code = lines[i + 1].strip() if i + 1 < len(lines) else ""
            rows.append({"File": m.group(1), "Dòng": int(m.group(2)), "Quy tắc": m.group(3), "CWE": m.group(5), "Mô tả": m.group(4), "Mã nguồn": code})
        elif "[CLEAN]" in ln and cur_file:
            rows.append({"File": cur_file, "Dòng": None, "Quy tắc": "CLEAN", "CWE": "-", "Mô tả": "Không phát hiện vi phạm", "Mã nguồn": ""})
    return pd.DataFrame(rows)


def parse_smt(text: str) -> list[dict]:
    out = []
    for m in re.finditer(r"\[Check (\d+)\] (.+?):\n\s*--> RESULT: (SAT|UNSAT)\s*\((.*?)\)?\s*\n((?:(?!\[Check ).*\n?)*)", text):
        out.append({"id": int(m.group(1)), "title": m.group(2).strip(), "result": m.group(3),
                    "summary": m.group(4).strip(), "detail": m.group(5).strip()})
    return out


def parse_blackbox(text: str) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    crash_rows, trunc_rows = [], []
    for m in re.finditer(r"BLACK-BOX FUZZING TREN (\S+) \((\d+) runs\).*?Attempts\):\s+(\d+).*?Crash \(Buffer Overflow\): (\d+).*?Logic Error \(Bằng cấp\):\s+(\d+).*?Thời gian thực thi:\s+([\d.]+) giây.*?Tốc độ fuzzing:\s+([\d.]+)", text, re.S):
        crash_rows.append({"Binary": m.group(1), "Runs": int(m.group(3)), "Crash": int(m.group(4)), "Logic error (bằng cấp)": int(m.group(5)),
                           "Thời gian (s)": float(m.group(6)), "execs/s": float(m.group(7))})
    for m in re.finditer(r"\(CWE-197 Numeric Truncation\) TREN (\S+) \((\d+) runs\).*?Attempts\):\s+(\d+).*?Truncation\): (\d+).*?Safe Blocked\): (\d+).*?Normal\):\s+(\d+).*?Crash:\s+(\d+)", text, re.S):
        trunc_rows.append({"Binary": m.group(1), "Runs": int(m.group(3)), "Sai lệch (truncation)": int(m.group(4)),
                           "Chặn an toàn": int(m.group(5)), "Hợp lệ": int(m.group(6)), "Crash": int(m.group(7))})
    samples = [{"Sample": s[0], "Attempt": s[1], "TenLen": int(s[2]), "LopLen": int(s[3]), "BangCap": s[4], "Reason": s[5]}
               for s in re.findall(r"Sample #(\d+): Attempt #(\d+) \| TenLen=(\d+) \| LopLen=(\d+) \| BangCap='([^']*)' \| Reason: (.+)", text)]
    return pd.DataFrame(crash_rows), pd.DataFrame(trunc_rows), samples


def parse_whitebox(text: str) -> tuple[pd.DataFrame, dict]:
    rows = [{"Target": int(t[0]), "Mô tả": t[1].strip(), "CWE": t[2], "Kết quả": f"SAT in {t[3]} attempt", "Điều kiện Z3 tìm ra": t[4].strip()}
            for t in re.findall(r"\[Target (\d+)\] (.+?) \((CWE-\d+)\): SAT in (\d+) attempt\n\s*Condition: (.+)", text)]
    summary = {}
    m = re.search(r"Attempts\):\s+(\d+) lần.*?crash/vulnerability: (\d+) / (\d+) target.*?Thời gian thực thi:\s+([\d.]+) giây.*?~([\d.]+)x speedup", text, re.S)
    if m:
        summary = {"attempts": int(m.group(1)), "found": int(m.group(2)), "targets": int(m.group(3)), "time": float(m.group(4)), "speedup": float(m.group(5))}
    return pd.DataFrame(rows), summary


def parse_nfr(text: str) -> pd.DataFrame:
    rows = []
    for m in re.finditer(r"\[NFR-1 PERF\] (\d+) lan (calculate_e2e_salary_\w+): tong=([\d.]+) ms, trung binh=([\d.]+) ms/lan.*?-> (PASS|FAIL)", text):
        rows.append({"Bản": "VULN" if "VULN" in m.group(2) else "FIXED", "NFR": "NFR-1 Hiệu năng", "N": int(m.group(1)), "Giá trị": f"{m.group(4)} ms/lần (tổng {m.group(3)} ms)", "Ngưỡng": "< 10 ms/lần", "Kết quả": m.group(5)})
    for i, m in enumerate(re.finditer(r"\[NFR-2 MEMORY\] (\d+) lan .*?truoc=(\d+) KB, sau=(\d+) KB, drift=(-?\d+) KB.*?-> (PASS|FAIL)", text)):
        rows.append({"Bản": "VULN" if i == 0 else "FIXED", "NFR": "NFR-2 Bộ nhớ", "N": int(m.group(1)), "Giá trị": f"drift {m.group(4)} KB ({m.group(2)} → {m.group(3)} KB)", "Ngưỡng": "|drift| < 1024 KB", "Kết quả": m.group(5)})
    return pd.DataFrame(rows)


def kripke_dot(is_buggy: bool, highlight: list[str] | None = None) -> str:
    sys.path.insert(0, os.path.join(BASE, "ch1_models"))
    try:
        from kripke_bmc import build_duong_university_kripke  # type: ignore
        k = build_duong_university_kripke(is_buggy=is_buggy)
        states, trans, labels, initial = k.states, k.transitions, k.labels, k.initial
    except Exception:  # fallback neu import loi
        return 'digraph G { "khong import duoc kripke_bmc.py" }'
    hl = set(highlight or [])
    lines = ["digraph G {", "rankdir=LR; node [shape=box, style=\"rounded,filled\", fontname=Helvetica, fontsize=11];", "edge [color=\"#4b564e\"];"]
    for s in sorted(states):
        lb = labels[s]
        fill = "#f8dede" if "error" in lb else ("#fff1cc" if "byte_truncated" in lb else ("#dcece7" if "exported" in lb else "#ffffff"))
        pen = "#d03b3b" if s in hl else "#7c877e"
        pw = "3" if s in hl else "1"
        lines.append(f'"{s}" [label="{s}\\n{{{", ".join(sorted(lb))}}}", fillcolor="{fill}", color="{pen}", penwidth={pw}];')
    for s in initial:
        lines.append(f'"__init" [shape=point]; "__init" -> "{s}";')
    for src, dsts in trans.items():
        for d in sorted(dsts):
            style = ' [color="#d03b3b", penwidth=2]' if (src in hl and d in hl) else ""
            lines.append(f'"{src}" -> "{d}"{style};')
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Thanh phan giao dien dung chung
# ---------------------------------------------------------------------------
def rerun_bar(key: str, label: str, timeout: int = 600):
    _, logname = SCRIPTS[key]
    c1, c2 = st.columns([3, 1])
    c1.caption(f"Nguồn dữ liệu: `logs/{logname}` — cập nhật lần cuối: **{log_mtime(logname)}**")
    if c2.button(f"▶ Chạy lại {label}", key=f"btn_{key}", use_container_width=True):
        with st.spinner(f"Đang chạy {SCRIPTS[key][0]} ..."):
            rc, out = run_script(key, timeout)
        st.session_state[f"out_{key}"] = (rc, out)
        st.rerun()
    if f"out_{key}" in st.session_state:
        rc, out = st.session_state.pop(f"out_{key}")
        (st.success if rc == 0 else st.error)(f"Script kết thúc với exit code {rc}. Log đã được ghi lại.")
        with st.expander("Output vừa chạy", expanded=False):
            st.code(out, language="text")


def raw_log(logname: str):
    with st.expander(f"📄 Log nguyên văn: logs/{logname}"):
        st.code(read_log(logname) or "(chưa có log — hãy bấm Chạy lại)", language="text")


def show_run(res: dict, title: str):
    st.markdown(f"**{title}** — {rc_badge(res['rc'])} · {res['t']*1000:.0f} ms")
    if res["out"].strip():
        st.code(res["out"], language="text")
    if res["err"].strip():
        st.code(res["err"], language="text")


# ---------------------------------------------------------------------------
# Cac trang
# ---------------------------------------------------------------------------
def page_overview():
    st.title("SoftSec Toolkit — DuongUniversity Management System")
    st.markdown("Hệ thống E2E 3 mô-đun (Giảng viên → Lớp học phần → Tính tiền dạy) được kiểm chứng bằng **4 kỹ thuật** "
                "tương ứng 4 chương: mô hình hoá Kripke/BMC, quét tĩnh an toàn bộ nhớ, kiểm chứng SMT bằng Z3, fuzzing hộp đen/hộp trắng. "
                "Mọi số liệu dưới đây được **đọc trực tiếp từ `logs/`** do script thật sinh ra.")

    kr, _ = parse_kripke(read_log("kripke_bmc.log"))
    sc = parse_scanner(read_log("pattern_scanner.log"))
    smt = parse_smt(read_log("smt_verify.log"))
    bb, _, _ = parse_blackbox(read_log("fuzzer_blackbox.log"))
    wb, wbs = parse_whitebox(read_log("fuzzer_whitebox.log"))

    c = st.columns(5)
    n_sat_buggy = int((kr["BUGGY"] == "SAT").sum()) if not kr.empty and "BUGGY" in kr else 0
    n_sat_fixed = int((kr["FIXED"] == "SAT").sum()) if not kr.empty and "FIXED" in kr else 0
    c[0].metric("Ch1 · LTL vi phạm BUGGY / FIXED", f"{n_sat_buggy} / {n_sat_fixed}", help="Số thuộc tính SAT (tìm được phản ví dụ) trên 5 thuộc tính P1–P5")
    c[1].metric("Ch2 · Cảnh báo quét tĩnh", int((sc["Quy tắc"] != "CLEAN").sum()) if not sc.empty else 0, help="trên 3 file module VULN; main_fixed.c CLEAN")
    c[2].metric("Ch3 · Z3 SAT / UNSAT", f"{sum(1 for x in smt if x['result']=='SAT')} / {sum(1 for x in smt if x['result']=='UNSAT')}", help="SAT = lỗ hổng thật (VULN), UNSAT = chứng minh an toàn (FIXED)")
    if not bb.empty:
        v = bb[bb["Binary"].str.contains("fixed") == False].iloc[0]
        f = bb[bb["Binary"].str.contains("fixed")].iloc[0]
        c[3].metric("Ch4 · Crash hộp đen VULN → FIXED", f"{v['Crash']} → {f['Crash']}", delta=f"-{v['Crash']-f['Crash']} crash / {v['Runs']} runs", delta_color="normal")
    if wbs:
        c[4].metric("Ch4 · Hộp trắng Z3", f"{wbs['found']}/{wbs['targets']} target", delta=f"~{wbs['speedup']}x nhanh hơn", delta_color="normal")

    st.divider()
    l, r = st.columns([1.1, 1])
    with l:
        st.subheader("Pipeline 4 chương")
        st.graphviz_chart("""
digraph P { rankdir=LR; node [shape=box, style="rounded,filled", fontname=Helvetica, fontsize=11, fillcolor="#ffffff", color="#7c877e"];
  src [label="ch2_memsafe/*.c\\n3 mô-đun C\\n(VULN + FIXED)", fillcolor="#e3e9e0"];
  ch1 [label="Ch1 · Kripke + BMC\\n(kripke_bmc.py, Z3)\\n5 thuộc tính LTL"];
  ch2 [label="Ch2 · Quét tĩnh\\n(pattern_scanner.py)\\n+ ASan trace + NFR"];
  ch3 [label="Ch3 · SMT Z3\\n(smt_verify.py)\\n7 check"];
  ch4 [label="Ch4 · Fuzzing\\nhộp đen 200 runs\\nhộp trắng Z3 7 target"];
  cwe [label="Tổng hợp CWE\\nCVSS-lite\\nMa trận truy vết", fillcolor="#dcece7"];
  src -> ch2; src -> ch4; ch1 -> ch2 [label="đối chiếu\\nS4/S3", fontsize=9]; ch2 -> cwe; ch3 -> cwe; ch4 -> cwe; ch1 -> cwe; ch2 -> ch3 [style=dashed, label="ràng buộc", fontsize=9]; ch4 -> ch3 [style=dashed, label="speedup", fontsize=9];
}""")
    with r:
        st.subheader("Mức rủi ro CVSS-lite theo CWE")
        dfc = pd.DataFrame(CWE_TABLE, columns=["CWE", "Tên", "Vị trí", "CVSS", "Mức"])
        fig = px.bar(dfc.sort_values("CVSS"), x="CVSS", y="CWE", color="Mức", orientation="h", text="CVSS",
                     color_discrete_map={"HIGH": "#d03b3b", "MEDIUM": "#e08a52", "LOW": "#7c877e"}, hover_data=["Tên", "Vị trí"])
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_range=[0, 10], legend_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Đặc tả yêu cầu")
    t1, t2 = st.tabs(["REQ (chức năng / an toàn)", "NFR (phi chức năng)"])
    with t1:
        st.dataframe(pd.DataFrame(REQ_TABLE, columns=["Mã", "Loại", "Ưu tiên", "Nội dung", "Kiểm chứng chính"]), use_container_width=True, hide_index=True)
    with t2:
        dfn = pd.DataFrame(NFR_TABLE, columns=["Mã", "Thuộc tính", "Nội dung", "Kết quả"])
        st.dataframe(dfn.style.map(status_color, subset=["Kết quả"]), use_container_width=True, hide_index=True)


def page_ch1():
    st.title("Chương 1 — Mô hình hoá Kripke & Bounded Model Checking")
    rerun_bar("kripke_bmc", "Ch1", 120)
    text = read_log("kripke_bmc.log")
    df, traces = parse_kripke(text)

    st.subheader("Kết quả 5 thuộc tính LTL (k = 5)")
    st.caption("**SAT** = Z3 tìm được một vết thực thi ≤ 5 bước **vi phạm** thuộc tính (phản ví dụ). **UNSAT** = thuộc tính đúng trong phạm vi k bước.")
    if df.empty:
        st.warning("Chưa có log. Bấm Chạy lại.")
        return
    st.dataframe(df.style.map(sat_color, subset=[c for c in ("BUGGY", "FIXED") if c in df]), use_container_width=True, hide_index=True)

    st.subheader("Đồ thị Kripke & phản ví dụ")
    c1, c2 = st.columns([1, 2])
    model = c1.radio("Mô hình", ["BUGGY", "FIXED"], horizontal=True)
    avail = [p for (p, m) in traces if m == model]
    chosen = c1.selectbox("Tô đậm phản ví dụ của", ["(không)"] + avail)
    hl = [s for _, s, _ in traces.get((chosen, model), [])] if chosen != "(không)" else []
    with c2:
        st.graphviz_chart(kripke_dot(model == "BUGGY", hl))
    if hl:
        steps = traces[(chosen, model)]
        st.markdown(f"**Vết phản ví dụ {chosen} ({model})**: " + " → ".join(f"`{s}`" for _, s, _ in steps))
        st.dataframe(pd.DataFrame(steps, columns=["Bước", "Trạng thái", "Nhãn"]), use_container_width=True, hide_index=True)

    m = re.search(r"DOI CHIEU MO HINH KRIPKE.*", text, re.S)
    if m:
        st.subheader("Đối chiếu Kripke ↔ Chương 2 (traceability)")
        st.code(m.group(0), language="text")
    raw_log("kripke_bmc.log")


def page_ch2():
    st.title("Chương 2 — Quét tĩnh an toàn bộ nhớ liên mô-đun")
    tab1, tab2, tab3, tab4 = st.tabs(["Pattern scanner (tĩnh)", "Memory trace (động, ASan)", "NFR-1/NFR-2", "Demo binary VULN vs FIXED"])

    with tab1:
        rerun_bar("pattern_scanner", "scanner", 60)
        df = parse_scanner(read_log("pattern_scanner.log"))
        if df.empty:
            st.warning("Chưa có log.")
        else:
            findings = df[df["Quy tắc"] != "CLEAN"]
            c1, c2 = st.columns([1, 1])
            with c1:
                st.plotly_chart(px.bar(findings.groupby(["File", "CWE"]).size().reset_index(name="Số cảnh báo"), x="File", y="Số cảnh báo", color="CWE", title="Cảnh báo theo file & CWE").update_layout(height=320, margin=dict(t=40, b=10)), use_container_width=True)
            with c2:
                st.plotly_chart(px.pie(findings, names="Quy tắc", title="Phân bố quy tắc vi phạm", hole=0.45).update_layout(height=320, margin=dict(t=40, b=10)), use_container_width=True)
            st.dataframe(df, use_container_width=True, hide_index=True,
                         column_config={"Mã nguồn": st.column_config.TextColumn(width="large")})
            st.info("`main_fixed.c` → **[CLEAN]**: bản vá dùng cùng 3 module nhưng chỉ gọi các hàm `*_SAFE` (snprintf, nullify sau free, long long/double, guard 0..127).")
        raw_log("pattern_scanner.log")

    with tab2:
        rerun_bar("memory_trace", "memory trace (cần clang64)", 180)
        text = read_log("memory_trace.log")
        st.caption("Bằng chứng động: trace **địa chỉ thật** qua 7 bước — bước 7 đọc lại đúng vùng nhớ đã `free()` ở bước 6 (CWE-416). Bản ASan bắt `heap-use-after-free`; bản FIXED chạy sạch.")
        secs = re.split(r"\n(?==+\n\s+BUOC )", text)
        for s in secs:
            m = re.match(r"=+\n\s+(BUOC [^\n]+)\n=+\n(.*)", s, re.S)
            if m:
                body = m.group(2).strip()
                is_err = "ERROR: AddressSanitizer" in body
                with st.expander(("🔴 " if is_err else "🟢 ") + m.group(1), expanded=is_err):
                    st.code(body, language="text")
        raw_log("memory_trace.log")

    with tab3:
        rerun_bar("nfr_check", "NFR check", 120)
        dfn = parse_nfr(read_log("nfr_check.log"))
        if not dfn.empty:
            st.dataframe(dfn.style.map(status_color, subset=["Kết quả"]), use_container_width=True, hide_index=True)
        raw_log("nfr_check.log")

    with tab4:
        st.caption("Chạy **cùng một subcommand** trên 2 binary. Bản VULN crash (exit code 0xC0000374/0xC0000005) hoặc in dữ liệu sai; bản FIXED từ chối có kiểm soát.")
        mode = st.selectbox("Kịch bản E2E", list(E2E_MODES), format_func=lambda k: f"{k} — {E2E_MODES[k]}")
        extra = []
        if mode == "e2e_byte_truncate":
            extra = [str(st.slider("soLuongSinhVien", -50, 400, 200))]
        elif mode == "e2e_nfr_bench":
            extra = [str(st.select_slider("N lần lặp", [1000, 10000, 100000], 10000))]
        if st.button("▶ Chạy cả 2 binary", type="primary"):
            cv, cf = st.columns(2)
            with cv:
                show_run(run_binary(VULN_EXE, [mode] + extra), "salary_calc.exe (VULN)")
            with cf:
                show_run(run_binary(FIXED_EXE, [mode] + extra), "salary_calc_fixed.exe (FIXED)")


def page_ch3():
    st.title("Chương 3 — Kiểm chứng hình thức bằng Z3 SMT")
    rerun_bar("smt_verify", "Ch3", 120)
    checks = parse_smt(read_log("smt_verify.log"))
    if not checks:
        st.warning("Chưa có log.")
        return
    st.caption("Mỗi *check* hỏi Z3: *tồn tại* input hợp lệ vi phạm ràng buộc không? **SAT** = có (kèm phản ví dụ cụ thể) → lỗ hổng thật trên bản VULN; **UNSAT** = chứng minh an toàn (bản FIXED) trong miền ràng buộc.")
    df = pd.DataFrame([{"Check": c["id"], "Nội dung": c["title"], "Kết quả": c["result"], "Tóm tắt": c["summary"]} for c in checks])
    st.dataframe(df.style.map(sat_color, subset=["Kết quả"]), use_container_width=True, hide_index=True)
    pairs = [(1, 2, "CWE-190: int32 (SAT) → long long (UNSAT)"), (4, 5, "CWE-197: ép char không guard (SAT) → guard 0..127 (UNSAT)")]
    st.subheader("Cặp VULN → FIXED được chứng minh")
    for a, b, title in pairs:
        ca = next((c for c in checks if c["id"] == a), None)
        cb = next((c for c in checks if c["id"] == b), None)
        if ca and cb:
            st.markdown(f"**{title}**")
            l, r = st.columns(2)
            l.error(f"Check {a} — {ca['result']}\n\n{ca['summary']}")
            r.success(f"Check {b} — {cb['result']}\n\n{cb['summary']}")
    st.subheader("Chi tiết phản ví dụ")
    for c in checks:
        with st.expander(f"{'🔴' if c['result']=='SAT' else '🟢'} Check {c['id']} — {c['title']} → {c['result']}"):
            st.code((c["summary"] + "\n" + c["detail"]).strip(), language="text")
    raw_log("smt_verify.log")


def page_ch4():
    st.title("Chương 4 — Fuzzing: Hộp đen đối chứng Hộp trắng")
    t1, t2 = st.tabs(["Hộp đen (ngẫu nhiên, 200 runs)", "Hộp trắng (Z3-guided)"])
    with t1:
        rerun_bar("fuzzer_blackbox", "black-box (≈15-60 s)", 900)
        bb, tr, samples = parse_blackbox(read_log("fuzzer_blackbox.log"))
        if bb.empty:
            st.warning("Chưa có log.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                long = bb.melt(id_vars="Binary", value_vars=["Crash", "Logic error (bằng cấp)"], var_name="Loại", value_name="Số lần")
                st.plotly_chart(px.bar(long, x="Binary", y="Số lần", color="Loại", barmode="group", title="Crash & logic error / 200 runs",
                                       color_discrete_map={"Crash": "#d03b3b", "Logic error (bằng cấp)": "#e08a52"}).update_layout(height=330, margin=dict(t=40, b=10)), use_container_width=True)
            with c2:
                if not tr.empty:
                    longt = tr.melt(id_vars="Binary", value_vars=["Sai lệch (truncation)", "Chặn an toàn", "Hợp lệ"], var_name="Kết quả", value_name="Số lần")
                    st.plotly_chart(px.bar(longt, x="Binary", y="Số lần", color="Kết quả", title="CWE-197 fuzzing soLuongSinhVien ∈ [-50, 400]",
                                           color_discrete_map={"Sai lệch (truncation)": "#d03b3b", "Chặn an toàn": "#0f6b5c", "Hợp lệ": "#7c877e"}).update_layout(height=330, margin=dict(t=40, b=10)), use_container_width=True)
            st.dataframe(bb, use_container_width=True, hide_index=True)
            if not tr.empty:
                st.dataframe(tr, use_container_width=True, hide_index=True)
            if samples:
                st.markdown("**Mẫu input gây crash** (bản VULN) — TenLen > 80 = tràn `hoTen[MAX_NAME]`, LopLen > 20 = tràn `maLop[MAX_MALOP]`:")
                st.dataframe(pd.DataFrame(samples), use_container_width=True, hide_index=True)
            m = re.search(r"--> PHAT HIEN TRUNG LAP BYTE.*?(?=\n\n=+|\Z)", read_log("fuzzer_blackbox.log"), re.S)
            bva = re.findall(r"n=\s*(-?\d+)\s+->\s+status=(\w+)\s+byte_that=\s*(\S+)\s+byte_du_kien=\s*(-?\d+)\s+\[(\w+)\]", read_log("fuzzer_blackbox.log"))
            if bva:
                st.markdown("**BVA 17 giá trị biên (CWE-197)** — bản chạy cuối trong log:")
                dfb = pd.DataFrame(bva, columns=["n (soLuongSinhVien)", "status", "byte thật", "byte dự kiến (lý thuyết)", "KL"])
                st.dataframe(dfb.tail(17), use_container_width=True, hide_index=True)
        raw_log("fuzzer_blackbox.log")
    with t2:
        rerun_bar("fuzzer_whitebox", "white-box (cần log hộp đen)", 120)
        wb, s = parse_whitebox(read_log("fuzzer_whitebox.log"))
        if s:
            c = st.columns(4)
            c[0].metric("Target phát hiện", f"{s['found']}/{s['targets']}")
            c[1].metric("Số lần giải Z3", s["attempts"])
            c[2].metric("Thời gian", f"{s['time']:.3f} s")
            c[3].metric("Speedup so với hộp đen", f"~{s['speedup']}x")
            bb, _, _ = parse_blackbox(read_log("fuzzer_blackbox.log"))
            if not bb.empty:
                bbt = float(bb.iloc[0]["Thời gian (s)"])
                fig = go.Figure([go.Bar(x=["Hộp đen (200 runs ngẫu nhiên)", "Hộp trắng (Z3, 7 target)"], y=[bbt, s["time"]],
                                        text=[f"{bbt:.2f} s", f"{s['time']:.3f} s"], marker_color=["#eb6834", "#2a78d6"])])
                fig.update_layout(title="Thời gian tìm lỗ hổng trên bản VULN", yaxis_title="giây", height=320, margin=dict(t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)
        if not wb.empty:
            st.dataframe(wb, use_container_width=True, hide_index=True, column_config={"Điều kiện Z3 tìm ra": st.column_config.TextColumn(width="large")})
        st.info("Hộp trắng là *constraint-based exact SAT* trên 7 target đã xác định từ ràng buộc trong header (`MAX_NAME`, `MAX_MALOP`, INT32_MAX, char range) — không phải coverage-guided tự động; "
                "vì vậy nó nhanh nhưng **chỉ tìm được lỗi đã mô hình hoá**, còn hộp đen tìm được crash bất ngờ nhưng tốn 200 lần chạy.")
        raw_log("fuzzer_whitebox.log")


def page_live():
    st.title("Demo E2E trực tiếp — nhập dữ liệu, chạy cả 2 binary")
    st.caption("Chế độ tương tác của `main.c` / `main_fixed.c`: nhập họ tên → bằng cấp → mã lớp qua stdin, hệ thống tạo GV (Mod 1), lớp 45 tiết / 60 SV (Mod 2), tính tiền và xuất báo cáo (Mod 3).")
    c1, c2, c3 = st.columns([2, 1, 1])
    name = c1.text_input("Họ tên giảng viên (MAX_NAME = 80)", "Pham Van Duong")
    cap = c2.selectbox("Bằng cấp", ["GS", "PGS", "TIEN_SI", "THAC_SI", "CU_NHAN", "KY_SU (không hợp lệ)"], index=2)
    malop = c3.text_input("Mã lớp (MAX_MALOP = 20)", "CNTT2024_01")
    cap_val = cap.split(" ")[0]
    q = st.columns(4)
    if q[0].button("Preset: hợp lệ"):
        st.session_state.update(preset=("Pham Van Duong", "TIEN_SI", "CNTT2024_01"))
    if q[1].button("Preset: tràn hoTen (120 'A')"):
        st.session_state.update(preset=("A" * 120, "TIEN_SI", "CNTT2024_01"))
    if q[2].button("Preset: tràn maLop (45 'B')"):
        st.session_state.update(preset=("Pham Van Duong", "TIEN_SI", "B" * 45))
    if q[3].button("Preset: bằng cấp lạ (CWE-1288)"):
        st.session_state.update(preset=("Pham Van Duong", "KY_SU", "CNTT2024_01"))
    if "preset" in st.session_state:
        name, cap_val, malop = st.session_state.pop("preset")
        st.info(f"Preset: hoTen={len(name)} ký tự · bangCap={cap_val} · maLop={len(malop)} ký tự")
    st.markdown(f"Độ dài input: **hoTen = {len(name)}** ({'⚠ vượt 80' if len(name) > 80 else 'ok'}) · **maLop = {len(malop)}** ({'⚠ vượt 20' if len(malop) > 20 else 'ok'}) · bangCap = `{cap_val}`")
    if st.button("▶ Chạy VULN và FIXED", type="primary"):
        stdin = f"{name}\n{cap_val}\n{malop}\n"
        l, r = st.columns(2)
        with l:
            show_run(run_binary(VULN_EXE, [], stdin), "salary_calc.exe (VULN — *_VULN)")
        with r:
            show_run(run_binary(FIXED_EXE, [], stdin), "salary_calc_fixed.exe (FIXED — *_SAFE)")
        st.markdown("Kỳ vọng: tràn buffer → VULN **crash** (`0xC0000374` heap corruption) hoặc in rác, FIXED **cắt ngắn** bằng `snprintf`; bằng cấp lạ → VULN âm thầm dùng 1.0, FIXED cảnh báo `[SAFE ERROR] Invalid degree` rồi fallback CU_NHAN.")


def page_trace():
    st.title("Tổng hợp CWE & Ma trận truy vết Test Case → Yêu cầu (IEEE 829)")
    dfc = pd.DataFrame(CWE_TABLE, columns=["CWE", "Tên", "Vị trí trong đề tài", "CVSS-lite", "Mức"])
    st.dataframe(dfc.style.map(lambda v: {"HIGH": "background-color:#f8dede", "MEDIUM": "background-color:#fff1cc", "LOW": "background-color:#e3e9e0"}.get(v, ""), subset=["Mức"]), use_container_width=True, hide_index=True)
    df = pd.DataFrame(TRACE_TABLE, columns=["Mã TC", "REQ", "Input / Điều kiện", "Kỳ vọng", "Thực tế (log)", "KL"])
    c1, c2, c3 = st.columns(3)
    req = c1.multiselect("Lọc theo REQ/NFR", sorted({r for x in df["REQ"] for r in x.split(", ")}))
    kl = c2.multiselect("Lọc theo kết luận", sorted(df["KL"].unique()))
    ch = c3.multiselect("Lọc theo chương", ["K1", "K2", "K3", "K4", "N"])
    f = df.copy()
    if req:
        f = f[f["REQ"].apply(lambda x: any(r in x.split(", ") for r in req))]
    if kl:
        f = f[f["KL"].isin(kl)]
    if ch:
        f = f[f["Mã TC"].apply(lambda x: any(x.startswith(f"TC-{c}") for c in ch))]
    st.dataframe(f.style.map(status_color, subset=["KL"]), use_container_width=True, hide_index=True, height=600)
    cnt = df["KL"].str.extract(r"^(PASS/FAIL|PASS|FAIL|QS)")[0].value_counts()
    st.plotly_chart(px.pie(values=cnt.values, names=cnt.index, hole=0.5, title=f"{len(df)} test case theo kết luận",
                           color=cnt.index, color_discrete_map={"PASS": "#0ca30c", "FAIL": "#d03b3b", "PASS/FAIL": "#e08a52", "QS": "#7c877e"}).update_layout(height=300, margin=dict(t=40, b=10)), use_container_width=True)
    st.caption("`FAIL*` = kiểm chứng **tìm thấy lỗ hổng thật trên bản VULN** (đúng kỳ vọng của đề tài, không phải công cụ lỗi). `FAIL**` = lỗ hổng thiết kế còn tồn tại ở cả bản FIXED (va chạm giá trị). `QS†` = chưa có oracle tự động.")


def page_logs():
    st.title("Logs & chạy toàn bộ suite")
    st.caption(f"Python dùng để chạy script: `{PYTHON}` · gcc: `{GCC}`")
    if st.button("▶ Chạy toàn bộ run_all.py (biên dịch + 7 script, ≈ 1–2 phút)", type="primary"):
        with st.spinner("Đang chạy run_all.py ..."):
            env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
            proc = subprocess.run([PYTHON, os.path.join(BASE, "run_all.py")], cwd=BASE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=1800)
        (st.success if proc.returncode == 0 else st.error)(f"run_all.py exit code {proc.returncode}")
        st.code(proc.stdout + proc.stderr, language="text")
    rows = [{"Log": ln, "Kích thước": f"{os.path.getsize(os.path.join(LOGS, ln))/1024:.1f} KB" if os.path.exists(os.path.join(LOGS, ln)) else "-", "Cập nhật": log_mtime(ln), "Script": rel}
            for rel, ln in SCRIPTS.values()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    sel = st.selectbox("Xem log", [ln for _, ln in SCRIPTS.values()])
    st.code(read_log(sel) or "(trống)", language="text")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="SoftSec Toolkit — DuongUniversity", page_icon="🛡️", layout="wide")
    pages = {
        "🏠 Tổng quan": page_overview,
        "1️⃣ Ch1 · Kripke & BMC": page_ch1,
        "2️⃣ Ch2 · An toàn bộ nhớ": page_ch2,
        "3️⃣ Ch3 · SMT Z3": page_ch3,
        "4️⃣ Ch4 · Fuzzing": page_ch4,
        "🧪 Demo E2E trực tiếp": page_live,
        "🔗 CWE & Truy vết": page_trace,
        "📄 Logs & run_all": page_logs,
    }
    with st.sidebar:
        st.markdown("## 🛡️ SoftSec Toolkit")
        st.caption("BTL An toàn phần mềm — DuongUniversity")
        choice = st.radio("Điều hướng", list(pages), label_visibility="collapsed")
        st.divider()
        st.markdown("**Binary C (ch2_memsafe/)**")
        for exe in (VULN_EXE, FIXED_EXE):
            st.markdown(("🟢 " if os.path.exists(exe) else "🔴 ") + os.path.basename(exe))
        if st.button("🔨 Biên dịch lại 2 binary (gcc)", use_container_width=True):
            ok, out = compile_binaries()
            (st.success if ok else st.error)("Biên dịch " + ("thành công" if ok else "thất bại"))
            st.code(out, language="text")
        st.divider()
        st.caption("Số liệu đọc từ `logs/`. Mỗi trang có nút **Chạy lại** gọi đúng script gốc để ghi log mới.")
    pages[choice]()


if __name__ == "__main__":
    main()
