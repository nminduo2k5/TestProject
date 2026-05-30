@echo off
echo.
echo ===== RUNNING ALL API TESTS =====
echo.

echo [1/12] bangCapTest.js
k6 run bangCapTest.js
echo.

echo [2/12] khoaTest.js
k6 run khoaTest.js
echo.

echo [3/12] hocPhanTest.js
k6 run hocPhanTest.js
echo.

echo [4/12] lopHocPhanTest.js
k6 run lopHocPhanTest.js
echo.

echo [5/12] lopHocPhanThongKeTest.js
k6 run lopHocPhanThongKeTest.js
echo.

echo [6/12] thietLapDinhMucTest.js
k6 run thietLapDinhMucTest.js
echo.

echo [7/12] thietLapHeSoBCTest.js
k6 run thietLapHeSoBCTest.js
echo.

echo [8/12] thietLapHeSoLopTest.js
k6 run thietLapHeSoLopTest.js
echo.

echo [9/12] hocKiTest.js
k6 run hocKiTest.js
echo.

echo [10/12] giaoVienTest.js
k6 run giaoVienTest.js
echo.

echo [11/12] thongKeGVTest.js
k6 run thongKeGVTest.js
echo.

echo [12/12] tinhTienDayTest.js
k6 run tinhTienDayTest.js
echo.

echo ===== ALL TESTS COMPLETED =====
pause
