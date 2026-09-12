@echo off
echo =================================================================
echo   LAB 4 - DANH SACH LIEN KET GIANG VIEN (DuongUniversity) - CHAY TRUC TIEP
echo   (khong dung make.exe - tranh loi make C:\make\make.exe khong tuong thich)
echo =================================================================

echo.
echo [1/4] Don dep file cu...
if exist c\booklist_v1.exe del /q c\booklist_v1.exe
if exist c\booklist_v2.exe del /q c\booklist_v2.exe
if exist c\*.xml del /q c\*.xml

echo.
echo [2/4] Bien dich ban buggy va ban fixed...
gcc -Wall -Wextra -std=c11 -O2 -o c\booklist_v1.exe c\booklist_v1_buggy.c
if errorlevel 1 (
    echo [LOI] Bien dich booklist_v1_buggy.c that bai.
    exit /b 1
)
gcc -Wall -Wextra -std=c11 -O2 -o c\booklist_v2.exe c\booklist_v2_fixed.c
if errorlevel 1 (
    echo [LOI] Bien dich booklist_v2_fixed.c that bai.
    exit /b 1
)

echo.
echo [3/4] Chay thu 2 ban...
echo --- booklist_v1 (buggy) ---
c\booklist_v1.exe
echo --- booklist_v2 (fixed) ---
c\booklist_v2.exe

echo.
echo [4/4] Chay bao cao cppcheck + bo test tu dong...
python python\static_analysis_runner.py
python tests\test_static_analysis.py

echo.
echo =================================================================
echo   HOAN THANH! Xem REPORT.md de biet ket qua chi tiet.
echo =================================================================
