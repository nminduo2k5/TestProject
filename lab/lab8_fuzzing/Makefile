# Lab 8 - Fuzzing hop den vs hop trang (DuongUniversity - Module 3 Tinh tien day)
#
# CHU Y (giong Lab 3/6): can ASan THAT + coverage. GCC MSYS2 UCRT64 KHONG co libasan tren
# Windows -> dung Clang MSYS2 clang64 (ASan + --coverage), doc coverage bang llvm-cov gcov.
# Cai dat (mot lan, trong "MSYS2 CLANG64" shell):
#   pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld
# Dung: mingw32-make test   (hoac run_lab8.bat)

CC         = C:/msys64/clang64/bin/clang.exe
CFLAGS     = -g -Wall -Wextra -fsanitize=address --coverage
ASAN_DLL   = C:/msys64/clang64/bin/libclang_rt.asan_dynamic-x86_64.dll
LIBCXX_DLL = C:/msys64/clang64/bin/libc++.dll
PYTHON    ?= python

.PHONY: all clean test fuzz-blackbox fuzz-whitebox demo

all: c/tinh_tien_day_fuzz.exe

c/tinh_tien_day_fuzz.exe: c/tinh_tien_day_fuzz.c
	cd c && $(CC) $(CFLAGS) -o tinh_tien_day_fuzz.exe tinh_tien_day_fuzz.c
	cp -f "$(ASAN_DLL)" "$(LIBCXX_DLL)" c/

demo: all
	-./c/tinh_tien_day_fuzz.exe "GV:NguyenVanA"
	-./c/tinh_tien_day_fuzz.exe "GVADM:xinchao"
	-./c/tinh_tien_day_fuzz.exe "GVADM:!AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

fuzz-blackbox: all
	$(PYTHON) python/blackbox_fuzzer.py

fuzz-whitebox: all
	$(PYTHON) python/whitebox_fuzzer.py

test: all
	$(PYTHON) tests/test_fuzzing.py

clean:
	rm -f c/tinh_tien_day_fuzz.exe c/*.gcda c/*.gcno c/*.gcov c/*.dll crashes/*.txt
