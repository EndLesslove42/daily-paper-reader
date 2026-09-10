@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0launcher.ps1" -Action workflow
set "RESULT=%ERRORLEVEL%"
if not "%DPR_NO_PAUSE%"=="1" pause
exit /b %RESULT%
