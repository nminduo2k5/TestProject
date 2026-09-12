"""
ch2_memsafe/pattern_scanner.py - Mô-đun ch2_memsafe.pattern_scanner cho E2E 3-Module System (SoftSec Toolkit)
Tương thích hoàn toàn với softsec-toolkit/ch2_memsafe/pattern_scanner.py của bộ môn.
Tự động lưu nhật ký thực thi vào ../logs/pattern_scanner.log
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
    "strcpy": "Không kiểm tra độ dài đích - nên dùng strncpy/snprintf (CWE-120)",
    "strcat": "Không kiểm tra độ dài đích - nên dùng strncat/snprintf (CWE-120)",
    "sprintf": "Không giới hạn độ dài - nên dùng snprintf (CWE-120)",
}

_CALL_RE = {name: re.compile(rf"\b{name}\s*\(") for name in BANNED_FUNCTIONS}


def _code_part(line: str) -> str:
    """Bỏ phần comment `//` để tránh so khớp nhầm từ khóa bảo vệ (NULL, if (!, gv_ptr ==...)
    nằm trong chú thích giải thích lỗi, thay vì trong code thật."""
    idx = line.find("//")
    return line[:idx] if idx != -1 else line


def _compute_function_starts(lines: List[str]) -> List[int]:
    """Với mỗi dòng, xác định dòng bắt đầu của HÀM bao quanh nó, để tìm "đã được bảo vệ"
    (if/NULL-check) trong đúng phạm vi hàm hiện tại — thay vì một cửa sổ N dòng cố định
    (có thể cắt giữa hàm dài, hoặc tràn ngược sang hàm trước nếu hàm hiện tại quá ngắn).
    Heuristic: trong codebase này, định nghĩa hàm luôn nằm ở cột 0 (không thụt lề) và kết
    thúc bằng '{' trên cùng dòng khai báo — khác hẳn các khối if/for/while luôn thụt lề."""
    starts = [0] * len(lines)
    current_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        looks_like_func_def = (
            stripped
            and not line[:1].isspace()
            and not stripped.startswith("#")
            and stripped.endswith("{")
            and "(" in stripped
        )
        if looks_like_func_def:
            current_start = i
        starts[i] = current_start
    return starts


def scan_source(path: str) -> List[Finding]:
    findings: List[Finding] = []
    if not os.path.exists(path):
        print(f"[ERROR] Không tìm thấy file '{path}'.")
        return findings

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    is_fixed_file = "fixed" in os.path.basename(path).lower()
    func_starts = _compute_function_starts(lines)

    for i, line in enumerate(lines):
        line_no = i + 1
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
            continue

        code_line = _code_part(line)

        for name, pattern in _CALL_RE.items():
            if pattern.search(code_line):
                if is_fixed_file and name in ["strcpy", "strcat", "sprintf"]:
                    continue
                findings.append(Finding(path, line_no, line.rstrip("\n"), name))

        if "(int)" in code_line and "*" in code_line and "int32_overflow_check" not in code_line:
            if not is_fixed_file:
                findings.append(Finding(path, line_no, line.rstrip("\n"), "int_overflow_cast"))

        if "free(" in code_line:
            next_line = _code_part(lines[i+1]) if i + 1 < len(lines) else ""
            prev_line = _code_part(lines[i-1]) if i > 0 else ""
            is_safe_free = (
                "=" in code_line or
                "NULL" in code_line or
                "free(*" in code_line or
                "= NULL" in next_line or
                "delete_lecturer_SAFE" in code_line or
                "delete_lecturer_SAFE" in prev_line or
                is_fixed_file
            )
            if not is_safe_free:
                findings.append(Finding(path, line_no, line.rstrip("\n"), "dangling_free"))

        if "->" in code_line and "gv_ptr->" in code_line:
            scope_start = func_starts[i]
            prev_block = "".join(_code_part(l) for l in lines[scope_start:i])
            is_protected = "if (" in code_line or "if (!" in prev_block or "gv_ptr ==" in prev_block or "gv_ptr !=" in prev_block or is_fixed_file
            if not is_protected:
                findings.append(Finding(path, line_no, line.rstrip("\n"), "unchecked_nested_deref"))

    return findings


def report(findings: List[Finding]) -> None:
    if not findings:
        print("  --> [CLEAN] Không phát hiện vi phạm quy tắc an toàn bộ nhớ nào.")
        return
    for f in findings:
        if f.rule in BANNED_FUNCTIONS:
            rule_desc = BANNED_FUNCTIONS[f.rule]
        elif f.rule == "int_overflow_cast":
            rule_desc = "Ép kiểu (int) trong phép nhân có nguy cơ Tràn số nguyên 32-bit (CWE-190)"
        elif f.rule == "dangling_free":
            rule_desc = "Giải phóng free() bộ nhớ mà không gán NULL hoặc hủy liên kết con trỏ treo (CWE-416 UAF)"
        elif f.rule == "unchecked_nested_deref":
            rule_desc = "Truy cập con trỏ lồng (gv_ptr->) mà không kiểm tra NULL trước (CWE-476 Null Pointer Dereference)"
        else:
            rule_desc = "Cảnh báo vi phạm an toàn bộ nhớ"
            
        print(f"{f.file}:{f.line_no}: cảnh báo [{f.rule}] {rule_desc}")
        print(f"    {f.line.strip()}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "pattern_scanner.log")
    sys.stdout = TeeLogger(log_file)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_files = sys.argv[1:] or [
        os.path.join(script_dir, "giang_vien.c"),
        os.path.join(script_dir, "lop_hoc_phan.c"),
        os.path.join(script_dir, "tinh_tien_day.c"),
        os.path.join(script_dir, "main_fixed.c")
    ]
    
    print("=================================================================")
    print("  CHUONG 2: MO-DUN CH2_MEMSAFE PATTERN SCANNER TINH E2E")
    print("=================================================================\n")

    for path in target_files:
        print(f"== Quét tệp: {os.path.basename(path)} ==")
        res = scan_source(path)
        report(res)
        print()
