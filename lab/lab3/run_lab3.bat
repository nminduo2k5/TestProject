@echo off
echo =================================================================
echo   DUONGUNIVERSITY SECURESYS - BIEN DICH VA CHAY LAB 3
echo =================================================================

echo [1/3] Bien dich ban VULN (lab3_inventory_vuln.c)...
gcc -Wall -g -o inventory_vuln.exe lab3_inventory_vuln.c

echo [2/3] Bien dich ban SAFE (lab3_secure_inventory.c)...
gcc -Wall -g -o inventory_safe.exe lab3_secure_inventory.c

echo [3/3] Chay kiet thu tu dong 9 test cases...
python lab3_test_memory_safety.py

echo.
echo =================================================================
echo   HOAN THANH! Nhan phim bat ky de thoat...
echo =================================================================
pause
