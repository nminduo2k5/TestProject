@echo off
setlocal
cd /d "%~dp0"
echo =================================================================
echo   LAB 8 - FUZZING HOP DEN vs HOP TRANG (DuongUniversity - Module 3)
echo   (chay truc tiep, khong can make.exe)
echo =================================================================

set CLANG=C:\msys64\clang64\bin\clang.exe
set PATH=C:\msys64\clang64\bin;%PATH%
set PYTHONIOENCODING=utf-8
set PY=python
if exist "%USERPROFILE%\anaconda3\python.exe" set PY=%USERPROFILE%\anaconda3\python.exe

if not exist "%CLANG%" (
    echo [LOI] Khong tim thay %CLANG%. Cai: pacman -S mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-compiler-rt
    exit /b 1
)

echo.
echo [1/4] Bien dich + xac nhan loi thu cong (Buoc 1)...
pushd c
"%CLANG%" -g -Wall -Wextra -fsanitize=address --coverage -o tinh_tien_day_fuzz.exe tinh_tien_day_fuzz.c
if errorlevel 1 ( echo [LOI] Bien dich that bai. & popd & exit /b 1 )
copy /y C:\msys64\clang64\bin\libclang_rt.asan_dynamic-x86_64.dll . >nul
copy /y C:\msys64\clang64\bin\libc++.dll . >nul
echo --- GV:NguyenVanA (hop le) ---
tinh_tien_day_fuzz.exe "GV:NguyenVanA"
echo --- GVADM:!AAAA... (kenh debug + payload dai) ---
tinh_tien_day_fuzz.exe "GVADM:!AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" 2>&1 | findstr /C:"ERROR: AddressSanitizer" /C:"SUMMARY"
popd

echo.
echo [2/4] Fuzzing HOP DEN (1000 / 3000 / 5000 lan thu, seed 42)...
"%PY%" -u python\blackbox_fuzzer.py

echo.
echo [3/4] Fuzzing HOP TRANG coverage-guided (500 lan thu, seed 7)...
"%PY%" -u python\whitebox_fuzzer.py

echo.
echo [4/4] Chay bo test tu dong (5 test)...
"%PY%" -u tests\test_fuzzing.py

echo.
echo =================================================================
echo   HOAN THANH! Crash luu trong crashes\ - xem REPORT.md.
echo =================================================================
endlocal
