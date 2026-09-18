CC     = C:/msys64/ucrt64/bin/gcc.exe
PYTHON = C:/Users/Admin/miniconda3/envs/duong/python.exe
CFLAGS = -Wall -Wextra -std=c11 -O2

.PHONY: all clean test smt-report

all: c/brute_force_checker.exe

c/brute_force_checker.exe: c/brute_force_checker.c
	$(CC) $(CFLAGS) -o c/brute_force_checker.exe c/brute_force_checker.c

smt-report:
	$(PYTHON) python/smt_equivalence_checker.py

test: all
	$(PYTHON) tests/test_smt_verification.py

clean:
	del /f c\brute_force_checker.exe 2>nul || true
