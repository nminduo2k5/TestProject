# Lab 7 - Code Coverage (DuongUniversity - Module 3 calculate_salary())
# Moi truong: gcc + gcov cua MSYS2 UCRT64 (co san tren PATH). Khong can z3/clang.
# Dung: mingw32-make test   (hoac run_lab7.bat neu khong muon dung make)

CC      = gcc
CFLAGS  = -Wall -Wextra -std=c11 --coverage -DSALARY_CLI_MAIN
PYTHON ?= python

.PHONY: all clean test coverage-report generate-combinatorial generate-extended

all:
	$(CC) $(CFLAGS) -c c/tinh_tien_day_coverage.c -o c/tinh_tien_day_coverage.o
	$(CC) --coverage -o c/tinh_tien_day_cli.exe c/tinh_tien_day_coverage.o

generate-combinatorial:
	$(PYTHON) python/test_case_generator.py --quiet

generate-extended:
	$(PYTHON) python/test_case_generator.py --extended --quiet

coverage-report: generate-combinatorial generate-extended
	$(PYTHON) python/coverage_runner.py

test:
	$(PYTHON) tests/test_coverage.py

clean:
	rm -f c/tinh_tien_day_cli.exe c/*.o c/*.gcda c/*.gcno c/*.gcov
