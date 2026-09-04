CC      = gcc
CFLAGS  = -Wall -g

all: inventory_vuln.exe inventory_safe.exe

inventory_vuln.exe: lab3_inventory_vuln.c
	$(CC) $(CFLAGS) -o $@ $<

inventory_safe.exe: lab3_secure_inventory.c
	$(CC) $(CFLAGS) -o $@ $<

test: all
	python lab3_test_memory_safety.py

clean:
	cmd /c "del /f /q inventory_vuln.exe inventory_safe.exe 2>NUL"

.PHONY: all test clean
