@echo off
cd /d "%~dp0"
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --noconfirm --onefile --windowed --name "MKV Tool v1.0.0 by Tokon" MKVTool.py
pause
