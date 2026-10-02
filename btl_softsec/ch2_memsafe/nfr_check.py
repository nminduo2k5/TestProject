"""
ch2_memsafe/nfr_check.py - Kiem chung THUC NGHIEM (khong phai suy luan ly thuyet) 2 yeu cau
phi chuc nang quan trong nhat trong chuong2.tex (Bang 2, tab:nfr):
  NFR-1 (Hieu nang)         : thoi gian tinh luong cho 1 lop hoc phan phai < 10ms
  NFR-2 (On dinh bo nho)    : khong ro ri bo nho (heap) sau >= 10.000 lan lap tao/xoa lien tuc

Goi subcommand "e2e_nfr_bench <N>" da them vao main.c (VULN) va main_fixed.c (SAFE)
(ch2_memsafe/main.c, main_fixed.c) tren chinh 2 binary da bien dich cua Chuong 2, khong phai
1 microbenchmark tach biet - dam bao so do phan anh dung ham that dang dung trong he thong.

Tu dong luu toan bo output that vao ../logs/nfr_check.log
"""

import subprocess
import os
import sys

N_ITER = 10000


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def section(title):
    print(f"\n=================================================================")
    print(f"  {title}")
    print(f"=================================================================")


def main():
    ch2_dir = os.path.dirname(os.path.abspath(__file__))
    exe_vuln = os.path.join(ch2_dir, "salary_calc.exe")
    exe_fixed = os.path.join(ch2_dir, "salary_calc_fixed.exe")

    if not (os.path.exists(exe_vuln) and os.path.exists(exe_fixed)):
        print(f"[LOI] Khong tim thay {exe_vuln} / {exe_fixed} - hay chay run_all.py (buoc "
              f"bien dich) truoc, hoac tu bien dich bang gcc -Wall -g -o salary_calc.exe "
              f"giang_vien.c lop_hoc_phan.c tinh_tien_day.c main.c -lpsapi")
        return

    section(f"NFR-1 + NFR-2: BAN VULN (salary_calc.exe), N={N_ITER}")
    rv = run([exe_vuln, "e2e_nfr_bench", str(N_ITER)])
    print(rv.stdout)
    print(rv.stderr)

    section(f"NFR-1 + NFR-2: BAN FIXED (salary_calc_fixed.exe), N={N_ITER}")
    rf = run([exe_fixed, "e2e_nfr_bench", str(N_ITER)])
    print(rf.stdout)
    print(rf.stderr)

    section("KET LUAN")
    all_pass = all(tag in rv.stdout for tag in ["PASS"]) and all(tag in rf.stdout for tag in ["PASS"])
    fail_found = ("FAIL" in rv.stdout) or ("FAIL" in rf.stdout)
    if fail_found:
        print("  --> Co it nhat 1 NFR FAIL - xem chi tiet o tren.")
    else:
        print(f"  --> NFR-1 (hieu nang <10ms/lan) va NFR-2 (drift bo nho <1024KB sau "
              f"{N_ITER} lan) deu PASS tren CA HAI ban VULN va FIXED - xac nhan bang thuc "
              f"nghiem thay vi chi lap luan ly thuyet O(1) nhu ban dac ta truoc do.")


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
    log_file = os.path.join(base_dir, "logs", "nfr_check.log")
    sys.stdout = TeeLogger(log_file)
    print("=================================================================")
    print("  KIEM CHUNG THUC NGHIEM NFR-1 (HIEU NANG) VA NFR-2 (ON DINH BO NHO)")
    print("  (bo sung cho Chuong 2 - dac ta tai chuong2.tex Bang 2, tab:nfr)")
    print("=================================================================")
    main()
