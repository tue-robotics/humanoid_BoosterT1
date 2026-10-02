@echo off
rem Double-click to preview the documentation site. Keep the window open; close it to stop.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0preview.ps1"
if errorlevel 1 pause
