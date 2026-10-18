@echo off
cd /d "%~dp0"
py -3 MKVTool.py
if errorlevel 1 pause
