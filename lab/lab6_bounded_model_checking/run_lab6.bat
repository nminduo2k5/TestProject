@echo off
setlocal
cd /d "%~dp0"
echo =================================================================
echo   LAB 6 - BOUNDED MODEL CHECKING (DuongUniversity - danhSachLop[MAX_LOP])
echo   (chay truc tiep, khong can make.exe)
echo =================================================================

set CLANG=C:\msys64\clang64\bin\clang.exe
set PY=python
if exist "%USERPROFILE%\anaconda3\python.exe" set PY=%USERPROFILE%\anaconda3\python.exe

echo.
echo [1/5] Bien dich lop_hoc_phan_access.c voi AddressSanitizer (Clang clang64)...
if not exist "%CLANG%" (
    echo [LOI] Khong tim thay %CLANG%. Cai: pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt
    exit /b 1
)
"%CLANG%" -g -Wall -Wextra -fsanitize=address -o c\lop_hoc_phan_access.exe c\lop_hoc_phan_access.c
if errorlevel 1 ( echo [LOI] Bien dich that bai. & exit /b 1 )
copy /y C:\msys64\clang64\bin\libclang_rt.asan_dynamic-x86_64.dll c\ >nul
copy /y C:\msys64\clang64\bin\libc++.dll c\ >nul

echo.
echo [2/5] Chay dong co BMC (Z3) tren 6 chuong trinh...
"%PY%" python\bmc_engine.py

echo.
echo [3/5] Thi nghiem gioi han BMC (giam unwind_bound - Buoc 4)...
"%PY%" python\bmc_engine.py --bound-experiment

echo.
echo [4/5] Doi chieu runtime (C + ASan) - 7 kich ban...
for %%M in ("safe_full_scan" "offbyone" "symbolic_unsafe 9" "symbolic_safe 9" "symbolic_safe 3" "symbolic_reverse" "symbolic_reverse_fixed") do (
    echo --- %%~M ---
    c\lop_hoc_phan_access.exe %%~M
)

echo.
echo [5/5] Chay bo test tu dong (7 test)...
"%PY%" tests\test_bmc.py

echo.
echo =================================================================
echo   HOAN THANH! Xem REPORT.md de biet ket qua chi tiet.
echo =================================================================
endlocal
