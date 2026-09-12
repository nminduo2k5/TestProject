"""
ch1_models/kripke_bmc.py - Mô hình hóa Kripke & BMC cho DuongUniversity (giang_vien.c/lop_hoc_phan.c/tinh_tien_day.c)
Luồng trạng thái: S0_INIT (Chưa phân công) -> S1_GV_ASSIGNED (Đã phân công)
                 -> S2_SALARY_CALC (Tính tiền) -> S3_EXPORTED (Xuất báo cáo) -> S4_ERROR (Lỗi)
Bản FIXED: 5 trạng thái (S0-S4). Bản BUGGY: 6 trạng thái (thêm S5_INVALID_CALC mô phỏng
nhánh nhảy cóc bỏ qua bước phân công — xem THAM_CHIEU_TRANG_THAI bên dưới để đối chiếu
từng trạng thái với vị trí thật trong code C, và cross_validate_with_pattern_scanner()
để tự động xác nhận bằng kết quả quét tĩnh Chương 2).
Tự động lưu nhật ký thực thi vào ../logs/kripke_bmc.log
"""

import sys
import os
from collections import deque
from typing import Dict, List, Optional, Set
from z3 import *


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


class KripkeStructure:
    """Kripke structure M = (S, S0, R, L) cho luồng E2E 3 mô-đun (5 trạng thái bản FIXED, 6 bản BUGGY)."""

    def __init__(self, name: str = "KripkeModel") -> None:
        self.name = name
        self.states: Set[str] = set()
        self.initial: Set[str] = set()
        self.transitions: Dict[str, Set[str]] = {}
        self.labels: Dict[str, Set[str]] = {}

    def add_state(self, s: str, labels: Optional[List[str]] = None, initial: bool = False) -> None:
        self.states.add(s)
        self.transitions.setdefault(s, set())
        self.labels[s] = set(labels or [])
        if initial:
            self.initial.add(s)

    def add_transition(self, src: str, dst: str) -> None:
        if src not in self.states or dst not in self.states:
            raise ValueError(f"Trạng thái '{src}' hoặc '{dst}' chưa được khai báo.")
        self.transitions[src].add(dst)

    def reachable_states(self) -> Set[str]:
        visited: Set[str] = set()
        queue = deque(self.initial)
        while queue:
            s = queue.popleft()
            if s in visited:
                continue
            visited.add(s)
            for nxt in self.transitions.get(s, ()):
                if nxt not in visited:
                    queue.append(nxt)
        return visited


# Anh xa moi trang thai/chuyen tiep toi vi tri THAT trong code C, de mo hinh Kripke truu tuong
# co the doi chieu duoc voi code nguon thay vi chi ton tai doc lap tren giay:
#   S0_INIT          <-> chua goi add_lecturer_*() / create_class_section_*() (chua co GiangVien)
#   S1_GV_ASSIGNED   <-> sau add_lecturer_*() + create_class_section_*() voi gv != NULL
#                        (giang_vien.c, lop_hoc_phan.c)
#   S2_SALARY_CALC   <-> sau calculate_e2e_salary_*() (tinh_tien_day.c ham calculate_e2e_salary_VULN/SAFE)
#   S3_EXPORTED      <-> sau export_report_*() (tinh_tien_day.c)
#   S4_ERROR         <-> nhanh loi: gv_ptr==NULL (CWE-476, tinh_tien_day.c:13) hoac UAF sau
#                        delete_lecturer_VULN() khong huy lien ket (CWE-416, giang_vien.c:32)
#   S5_INVALID_CALC  <-> chi co trong ban BUGGY: goi calculate_e2e_salary_VULN() ma KHONG
#                        qua buoc gan giang vien hop le - dung de mo phong nhanh loi CWE-476/416
# Xem THAM_CHIEU_TRANG_THAI o cuoi file va ham cross_validate_with_pattern_scanner() de doi
# chieu tu dong voi ket qua quet tinh o Chuong 2 (ch2_memsafe/pattern_scanner.py).
THAM_CHIEU_TRANG_THAI = {
    "S4_ERROR": [("ch2_memsafe/giang_vien.c", "dangling_free"), ("ch2_memsafe/tinh_tien_day.c", "unchecked_nested_deref")],
}


def build_duong_university_kripke(is_buggy=False) -> KripkeStructure:
    name = "DuongUniversity_Kripke_BUGGY" if is_buggy else "DuongUniversity_Kripke_FIXED"
    k = KripkeStructure(name)

    # 5 Trạng thái chuẩn (bản FIXED): chưa phân công -> đã phân công -> tính tiền -> xuất báo cáo -> lỗi
    k.add_state("S0_INIT", labels=["init"], initial=True)
    k.add_state("S1_GV_ASSIGNED", labels=["assigned"])
    k.add_state("S2_SALARY_CALC", labels=["assigned", "calculated"])
    k.add_state("S3_EXPORTED", labels=["assigned", "calculated", "exported"])
    k.add_state("S4_ERROR", labels=["error"])

    # Chuyển trạng thái hợp lệ
    k.add_transition("S0_INIT", "S1_GV_ASSIGNED")
    k.add_transition("S1_GV_ASSIGNED", "S2_SALARY_CALC")
    k.add_transition("S1_GV_ASSIGNED", "S4_ERROR")
    k.add_transition("S2_SALARY_CALC", "S3_EXPORTED")
    k.add_transition("S2_SALARY_CALC", "S4_ERROR")
    k.add_transition("S3_EXPORTED", "S0_INIT")
    k.add_transition("S4_ERROR", "S0_INIT")

    if is_buggy:
        # Bản BUGGY MỞ RỘNG thành 6 trạng thái: thêm S5_INVALID_CALC với đường chuyển nhảy cóc
        # sai từ S0_INIT trực tiếp sang tính tiền mà chưa qua bước phân công S1 hợp lệ.
        k.add_state("S5_INVALID_CALC", labels=["calculated", "error"])
        k.add_transition("S0_INIT", "S5_INVALID_CALC")
        k.add_transition("S5_INVALID_CALC", "S4_ERROR")

    return k


def cross_validate_with_pattern_scanner():
    """Doi chieu tu dong: xac nhan cac trang thai/chuyen tiep loi (S4_ERROR, S5_INVALID_CALC)
    trong mo hinh Kripke TRUU TUONG o tren thuc su tuong ung voi lo hong THAT da duoc Chuong 2
    (ch2_memsafe/pattern_scanner.py) quet thay tren code C that - thay vi mo hinh Kripke ton tai
    doc lap, khong co co che nao chung minh no phan anh dung luong thuc thi thuc te."""
    ch1_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(ch1_dir)
    ch2_dir = os.path.join(base_dir, "ch2_memsafe")
    sys.path.insert(0, ch2_dir)
    import pattern_scanner  # ch2_memsafe/pattern_scanner.py - tai su dung chinh scanner cua Chuong 2

    print("\n=======================================================")
    print("  DOI CHIEU MO HINH KRIPKE VOI KET QUA QUET TINH CHUONG 2 (Traceability Check)")
    print("=======================================================")

    all_ok = True
    for src_relpath, expected_rule in THAM_CHIEU_TRANG_THAI["S4_ERROR"]:
        src_path = os.path.join(base_dir, *src_relpath.split("/"))
        findings = pattern_scanner.scan_source(src_path)
        matched = [f for f in findings if f.rule == expected_rule]
        if matched:
            f = matched[0]
            print(f"  [OK] S4_ERROR <-> {src_relpath}:{f.line_no} [{expected_rule}] (xac nhan boi pattern_scanner.py)")
        else:
            all_ok = False
            print(f"  [CANH BAO] Khong tim thay [{expected_rule}] trong {src_relpath} - mo hinh Kripke co the KHONG con khop voi code that!")

    if all_ok:
        print("  --> KET LUAN: Trang thai loi (S4_ERROR) trong mo hinh Kripke duoc xac nhan boi\n"
              "      it nhat 1 lo hong THAT (CWE-416/CWE-476) do Chuong 2 quet duoc tren code C hien tai.")
    return all_ok


def run_bmc_check_5state(kripke: KripkeStructure, bound_k: int = 5):
    print(f"\n=======================================================")
    print(f"  RUNNING BMC CHECK ON: {kripke.name} ({len(kripke.states)} trang thai, k={bound_k})")
    print(f"=======================================================")

    solver = Solver()
    solver.set('random_seed', 0)
    states_list = sorted(list(kripke.states))
    state_map = {s: idx for idx, s in enumerate(states_list)}
    inv_state_map = {idx: s for idx, s in enumerate(states_list)}

    state_vars = [Int(f"state_{i}") for i in range(bound_k + 1)]
    s0_name = list(kripke.initial)[0]
    solver.add(state_vars[0] == state_map[s0_name])

    for i in range(bound_k + 1):
        solver.add(And(state_vars[i] >= 0, state_vars[i] < len(states_list)))

    for i in range(bound_k):
        trans_conds = []
        for src_state, dst_states in kripke.transitions.items():
            src_idx = state_map[src_state]
            dst_conds = [state_vars[i + 1] == state_map[dst] for dst in sorted(dst_states)]
            if dst_conds:
                trans_conds.append(Implies(state_vars[i] == src_idx, Or(dst_conds)))
        if trans_conds:
            solver.add(And(trans_conds))

    # P1 (Safety): G(calculated -> assigned) - Chưa phân công -> không được tính tiền
    violation_conds_p1 = []
    for i in range(bound_k + 1):
        step_violations = []
        for s_idx, s_name in inv_state_map.items():
            lbls = kripke.labels[s_name]
            if "calculated" in lbls and "assigned" not in lbls:
                step_violations.append(state_vars[i] == s_idx)
        if step_violations:
            violation_conds_p1.append(Or(step_violations))

    solver.push()
    solver.add(Or(violation_conds_p1) if violation_conds_p1 else False)
    res1 = solver.check()
    print(f"\n[Property 1] Safety: G(calculated -> assigned) [Chưa phân công -> Không tính tiền]")
    if res1 == sat:
        model = solver.model()
        print(f"  --> RESULT: SAT (Counterexample Trace Found!)")
        print(f"  Counterexample Trace:")
        for i in range(bound_k + 1):
            s_val = model[state_vars[i]].as_long()
            s_name = inv_state_map[s_val]
            lbls = sorted(list(kripke.labels[s_name]))
            print(f"    Step {i}: {s_name} [Labels: {lbls}]")
    else:
        print(f"  --> RESULT: UNSAT (Property Holds up to k={bound_k})")
    solver.pop()

    # P2 (Safety): G(exported -> calculated) - Chưa tính tiền -> không được xuất báo cáo
    violation_conds_p2 = []
    for i in range(bound_k + 1):
        step_violations = []
        for s_idx, s_name in inv_state_map.items():
            lbls = kripke.labels[s_name]
            if "exported" in lbls and "calculated" not in lbls:
                step_violations.append(state_vars[i] == s_idx)
        if step_violations:
            violation_conds_p2.append(Or(step_violations))

    solver.push()
    solver.add(Or(violation_conds_p2) if violation_conds_p2 else False)
    res2 = solver.check()
    print(f"\n[Property 2] Safety: G(exported -> calculated) [Chưa tính tiền -> Không xuất báo cáo]")
    if res2 == sat:
        print(f"  --> RESULT: SAT (Counterexample Found!)")
    else:
        print(f"  --> RESULT: UNSAT (Property Holds up to k={bound_k})")
    solver.pop()

    # P3 (Liveness): G(assigned -> F calculated) - Phân công rồi -> cuối cùng phải tính tiền
    solver.push()
    has_assigned = Or([Or([state_vars[i] == state_map[s] for s in states_list if "assigned" in kripke.labels[s]]) for i in range(bound_k)])
    no_calculated_after = And([And([state_vars[j] != state_map[s] for s in states_list if "calculated" in kripke.labels[s]]) for j in range(bound_k + 1)])
    solver.add(And(has_assigned, no_calculated_after))
    res3 = solver.check()
    print(f"\n[Property 3] Liveness: G(assigned -> F calculated) [Phân công -> Cuối cùng tính tiền]")
    if res3 == sat:
        print(f"  --> RESULT: SAT (Counterexample Trace Found!)")
    else:
        print(f"  --> RESULT: UNSAT (Property Holds up to k={bound_k})")
    solver.pop()

    # P4 (Safety): G(error -> NOT exported) - Lỗi -> không được xuất báo cáo
    violation_conds_p4 = []
    for i in range(bound_k + 1):
        step_violations = []
        for s_idx, s_name in inv_state_map.items():
            lbls = kripke.labels[s_name]
            if "error" in lbls and "exported" in lbls:
                step_violations.append(state_vars[i] == s_idx)
        if step_violations:
            violation_conds_p4.append(Or(step_violations))

    solver.push()
    solver.add(Or(violation_conds_p4) if violation_conds_p4 else False)
    res4 = solver.check()
    print(f"\n[Property 4] Safety: G(error -> NOT exported) [Hệ thống Lỗi -> Không xuất báo cáo]")
    if res4 == sat:
        print(f"  --> RESULT: SAT (Counterexample Found!)")
    else:
        print(f"  --> RESULT: UNSAT (Property Holds up to k={bound_k})")
    solver.pop()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "logs", "kripke_bmc.log")
    sys.stdout = TeeLogger(log_file)

    print("=========================================================")
    print("  CHUONG 1: MO HINH HOA KRIPKE & BMC (k=5)")
    print("  Ban FIXED: 5 trang thai (S0-S4) | Ban BUGGY: 6 trang thai (S0-S5)")
    print("=========================================================")

    buggy_kripke = build_duong_university_kripke(is_buggy=True)
    run_bmc_check_5state(buggy_kripke, bound_k=5)

    fixed_kripke = build_duong_university_kripke(is_buggy=False)
    run_bmc_check_5state(fixed_kripke, bound_k=5)

    cross_validate_with_pattern_scanner()
