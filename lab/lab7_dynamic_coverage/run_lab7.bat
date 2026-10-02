@echo off
setlocal
cd /d "%~dp0"
echo =================================================================
echo   LAB 7 - CODE COVERAGE (DuongUniversity - Module 3 calculate_salary)
echo   (chay truc tiep, khong can make.exe)
echo =================================================================

set PY=python
if exist "%USERPROFILE%\anaconda3\python.exe" set PY=%USERPROFILE%\anaconda3\python.exe

echo.
echo [1/4] Sinh bo test to hop (goc + mo rong lop bien sv=50/51)...
"%PY%" python\test_case_generator.py --quiet
"%PY%" python\test_case_generator.py --extended --quiet

echo.
echo [2/4] Bien dich voi --coverage, chay 4 bo test, do gcov (line + branch)...
"%PY%" python\coverage_runner.py

echo.
echo [3/4] Xem bao cao gcov chi tiet dong theo dong (cac dong ##### la chua phu):
findstr /C:"#####" c\tinh_tien_day_coverage.c.gcov

echo.
echo [4/4] Chay bo test tu dong (5 test)...
"%PY%" tests\test_coverage.py

echo.
echo =================================================================
echo   HOAN THANH! Xem REPORT.md de biet ket qua chi tiet.
echo =================================================================
endlocal
