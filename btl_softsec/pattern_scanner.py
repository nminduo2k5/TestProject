"""
pattern_scanner.py - Mô-đun ch2_memsafe.pattern_scanner (SoftSec Toolkit)
Tương thích hoàn toàn với softsec-toolkit/ch2_memsafe/pattern_scanner.py của bộ môn.
Tự động lưu nhật ký thực thi vào logs/pattern_scanner.log
"""

import sys
import re
import os
from dataclasses import dataclass
from typing import List


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


@dataclass
class Finding:
    file: str
    line_no: int
    line: str
    rule: str


BANNED_FUNCTIONS = {
    "system": "Nguy cơ Command Injection (CWE-78) - cấm dùng theo chính sách tổ chức",
    "gets": "Không giới hạn độ dài input - buffer overflow chắc chắn (CWE-242)",
    "strcpy": "Không kiểm tra độ dài đích - nên dùng strncpy/snprintf",
    "strcat": "Không kiểm tra độ dài đích - nên dùng strncat/snprintf",
    "sprintf": "Không giới hạn độ dài - nên dùng snprintf",
}

_CALL_RE = {name: re.compile(rf"\b{name}\s*\(") for name in BANNED_FUNCTIONS}


def scan_source(path: str) -> List[Finding]:
    findings: List[Finding] = []
    if not os.path.exists(path):
        print(f"[ERROR] Không tìm thấy file '{path}'.")
        return findings

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue

            for name, pattern in _CALL_RE.items():
                if pattern.search(line):
                    findings.append(Finding(path, line_no, line.rstrip("\n"), name))

            if "(int)" in line and "*" in line and "int32_overflow_check" not in line:
                findings.append(Finding(path, line_no, line.rstrip("\n"), "int_overflow_cast"))

    return findings


def report(findings: List[Finding]) -> None:
    if not findings:
        print("Không phát hiện vi phạm nào.")
        return
    for f in findings:
        rule_desc = BANNED_FUNCTIONS.get(f.rule, "Ép kiểu (int) trong phép nhân có nguy cơ Tràn số nguyên (Integer Overflow)")
        print(f"{f.file}:{f.line_no}: cảnh báo [{f.rule}] {rule_desc}")
        print(f"    {f.line.strip()}")


if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(__file__), "logs", "pattern_scanner.log")
    sys.stdout = TeeLogger(log_file)

    target_files = sys.argv[1:] or ["salary_calc.c"]
    print("=================================================================")
    print(f"  MO-DUN CH2_MEMSAFE: PATTERN SCANNER TINH (SoftSec Toolkit)")
    print("=================================================================\n")

    for path in target_files:
        print(f"== Quet tep: {path} ==")
        res = scan_source(path)
        report(res)
        print()
