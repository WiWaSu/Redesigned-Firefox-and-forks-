@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0files\installer.ps1" -Action install -UserAppData "%APPDATA%"
echo.
pause
