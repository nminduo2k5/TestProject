# CHU Y: -fsanitize=address can mot compiler-rt/ASan runtime THAT SU.
# GCC cua MSYS2 UCRT64 (mac dinh tren PATH) KHONG kem libasan tren Windows -
# se loi link "ld returned 1/5 exit status". Dung Clang cua moi truong MSYS2
# clang64 (co compiler-rt day du) de -fsanitize=address hoat dong that.
# Cai dat (mot lan): mo "MSYS2 CLANG64" shell roi chay:
#   pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt mingw-w64-clang-x86_64-lld
CC = C:/msys64/clang64/bin/clang.exe
CFLAGS = -g -Wall -Wextra -fsanitize=address
ASAN_DLL = C:/msys64/clang64/bin/libclang_rt.asan_dynamic-x86_64.dll
LIBCXX_DLL = C:/msys64/clang64/bin/libc++.dll

.PHONY: all clean test risk-report

all: c/vulnerable_inventory.exe c/secure_inventory.exe

# Sao chep runtime DLL cua ASan vao cung thu muc voi file .exe, de binary
# chay duoc ngay ma KHONG can them C:\msys64\clang64\bin vao PATH he thong.
c/vulnerable_inventory.exe: c/vulnerable_inventory.c
	$(CC) $(CFLAGS) -o c/vulnerable_inventory.exe c/vulnerable_inventory.c
	cp -f "$(ASAN_DLL)" "$(LIBCXX_DLL)" c/

c/secure_inventory.exe: c/secure_inventory.c
	$(CC) $(CFLAGS) -o c/secure_inventory.exe c/secure_inventory.c
	cp -f "$(ASAN_DLL)" "$(LIBCXX_DLL)" c/

risk-report:
	python python/risk_assessor.py

test: all
	python tests/test_memory_safety.py

clean:
	rm -f c/vulnerable_inventory.exe c/secure_inventory.exe c/libclang_rt.asan_dynamic-x86_64.dll c/libc++.dll
