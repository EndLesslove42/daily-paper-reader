@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\windows\launcher.ps1" -Action menu
if errorlevel 1 pause
