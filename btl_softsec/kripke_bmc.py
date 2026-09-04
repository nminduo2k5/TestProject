"""
kripke_bmc.py - Kripke Structure & Bounded Model Checking (BMC) cho DuongUniversity
Tương thích hoàn toàn với softsec-toolkit (Chương 1: ch1_models + Chương 3: ch3_verify)
Tự động lưu nhật ký thực thi vào logs/kripke_bmc.log
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
    """Kripke structure M = (S, S0, R, L) theo chuẩn softsec-toolkit."""

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

    def find_path(self, target: str) -> Optional[List[str]]:
        for s0 in self.initial:
            path = self._bfs_path(s0, target)
            if path is not None:
                return path
        return None

    def _bfs_path(self, start: str, target: str) -> Optional[List[str]]:
        if start == target:
            return [start]
        visited = {start}
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            last = path[-1]
            for nxt in self.transitions.get(last, ()):
                if nxt == target:
                    return path + [nxt]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(path + [nxt])
        return None


def build_duong_university_kripke(is_buggy=False) -> KripkeStructure:
    name = "DuongUniversity_Kripke_BUGGY" if is_buggy else "DuongUniversity_Kripke_FIXED"
    k = KripkeStructure(name)

    k.add_state("S0_INIT", labels=["init"], initial=True)
    k.add_state("S1_GV_ASSIGNED", labels=["assigned"])
    k.add_state("S2_SALARY_CALC", labels=["assigned", "calculated"])
    k.add_state("S3_EXPORTED", labels=["assigned", "calculated", "exported"])
    k.add_state("S4_ERROR", labels=["error"])

    k.add_transition("S0_INIT", "S1_GV_ASSIGNED")
    k.add_transition("S1_GV_ASSIGNED", "S2_SALARY_CALC")
    k.add_transition("S1_GV_ASSIGNED", "S4_ERROR")
    k.add_transition("S2_SALARY_CALC", "S3_EXPORTED")
    k.add_transition("S2_SALARY_CALC", "S4_ERROR")
    k.add_transition("S3_EXPORTED", "S0_INIT")
    k.add_transition("S4_ERROR", "S0_INIT")

    if is_buggy:
        k.add_state("S5_INVALID_CALC", labels=["calculated", "error"])
        k.add_transition("S0_INIT", "S5_INVALID_CALC")
        k.add_transition("S5_INVALID_CALC", "S4_ERROR")

    return k


def run_bmc_check(kripke: KripkeStructure, bound_k: int = 5):
    print(f"\n=======================================================")
    print(f"  RUNNING BMC CHECK ON: {kripke.name} (k={bound_k})")
    print(f"=======================================================")

    solver = Solver()

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
            dst_conds = [state_vars[i + 1] == state_map[dst] for dst in dst_states]
            if dst_conds:
                trans_conds.append(Implies(state_vars[i] == src_idx, Or(dst_conds)))
        if trans_conds:
            solver.add(And(trans_conds))

    violation_conds_p1 = []
    for i in range(bound_k + 1):
        step_violations = []
        for s_idx, s_name in inv_state_map.items():
            lbls = kripke.labels[s_name]
            if "calculated" in lbls and "assigned" not in lbls:
                step_violations.append(state_vars[i] == s_idx)
        if step_violations:
            violation_conds_p1.append(Or(step_violations))

    p1_violated = Or(violation_conds_p1) if violation_conds_p1 else False

    solver.push()
    solver.add(p1_violated)
    res = solver.check()

    print(f"\n[Property 1] Safety: G(calculated -> assigned)")
    if res == sat:
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

    violation_conds_p2 = []
    for i in range(bound_k + 1):
        step_violations = []
        for s_idx, s_name in inv_state_map.items():
            lbls = kripke.labels[s_name]
            if "exported" in lbls and "calculated" not in lbls:
                step_violations.append(state_vars[i] == s_idx)
        if step_violations:
            violation_conds_p2.append(Or(step_violations))

    p2_violated = Or(violation_conds_p2) if violation_conds_p2 else False
    solver.push()
    solver.add(p2_violated)
    res2 = solver.check()
    print(f"\n[Property 2] Safety: G(exported -> calculated)")
    if res2 == sat:
        print(f"  --> RESULT: SAT (Counterexample Found!)")
    else:
        print(f"  --> RESULT: UNSAT (Property Holds up to k={bound_k})")
    solver.pop()


if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(__file__), "logs", "kripke_bmc.log")
    sys.stdout = TeeLogger(log_file)

    buggy_kripke = build_duong_university_kripke(is_buggy=True)
    run_bmc_check(buggy_kripke, bound_k=5)

    fixed_kripke = build_duong_university_kripke(is_buggy=False)
    run_bmc_check(fixed_kripke, bound_k=5)
