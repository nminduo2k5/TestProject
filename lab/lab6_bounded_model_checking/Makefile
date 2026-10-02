# Lab 6 - Bounded Model Checking (DuongUniversity - Module 2 danhSachLop[MAX_LOP])
#
# CHU Y (giong Lab 3): -fsanitize=address can runtime ASan THAT. GCC cua MSYS2
# UCRT64 (mac dinh tren PATH) KHONG kem libasan tren Windows -> dung Clang cua
# moi truong MSYS2 clang64. Cai dat (mot lan, trong "MSYS2 CLANG64" shell):
#   pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld
# Python can co z3-solver (pip install z3-solver) - tren may nay la Anaconda.
# Dung: mingw32-make test   (hoac run_lab6.bat neu khong muon dung make)

CC         = C:/msys64/clang64/bin/clang.exe
CFLAGS     = -g -Wall -Wextra -fsanitize=address
ASAN_DLL   = C:/msys64/clang64/bin/libclang_rt.asan_dynamic-x86_64.dll
LIBCXX_DLL = C:/msys64/clang64/bin/libc++.dll
PYTHON    ?= C:/Users/HP/anaconda3/python.exe

.PHONY: all clean test bmc-report bound-experiment demo

all: c/lop_hoc_phan_access.exe

c/lop_hoc_phan_access.exe: c/lop_hoc_phan_access.c
	$(CC) $(CFLAGS) -o c/lop_hoc_phan_access.exe c/lop_hoc_phan_access.c
	cp -f "$(ASAN_DLL)" "$(LIBCXX_DLL)" c/

bmc-report:
	$(PYTHON) python/bmc_engine.py

bound-experiment:
	$(PYTHON) python/bmc_engine.py --bound-experiment

demo: all
	-./c/lop_hoc_phan_access.exe safe_full_scan
	-./c/lop_hoc_phan_access.exe offbyone
	-./c/lop_hoc_phan_access.exe symbolic_unsafe 9
	-./c/lop_hoc_phan_access.exe symbolic_safe 9
	-./c/lop_hoc_phan_access.exe symbolic_safe 3
	-./c/lop_hoc_phan_access.exe symbolic_reverse
	-./c/lop_hoc_phan_access.exe symbolic_reverse_fixed

test: all
	$(PYTHON) tests/test_bmc.py

clean:
	rm -f c/lop_hoc_phan_access.exe c/libclang_rt.asan_dynamic-x86_64.dll c/libc++.dll c/*.pdb c/*.ilk
