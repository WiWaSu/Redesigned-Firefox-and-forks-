@echo off
start "" powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File "%~dp0files\installer.ps1" -Gui -UserAppData "%APPDATA%"
