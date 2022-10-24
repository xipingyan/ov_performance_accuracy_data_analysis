# README
The script compares 2 CSV files of OpenVINO accuracy test, and analyze the accuracy difference. At last it will generate a diff result report file.

# Usage
$ compare.py -h
For example:
$ compare.py accuracy.cpu.20221021_15_53.csv accuracy.cpu.20221023_11_09.csv 0.01

Run on Windows:
C:\msys64\mingw64\bin\python3.exe compare.py
C:\msys64\mingw64\bin\python3.exe compare.py accuracy.cpu.20221021_15_53.csv accuracy.cpu.20221023_11_09.csv 0.01
