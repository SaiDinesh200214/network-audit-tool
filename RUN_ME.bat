@echo off
:: ============================================================
::  NetAudit Pro — Double-Click Launcher
::  Just double-click this file. That's it!
::  It will auto-request admin rights and open the app.
:: ============================================================

:: Check if already running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :ALREADY_ADMIN
)

:: Not admin — re-launch this bat file elevated via PowerShell (UAC popup appears)
echo Requesting admin rights...
PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
exit /b

:ALREADY_ADMIN
:: We are admin now — go to the folder where this bat file lives
cd /d "%~dp0"

:: Find Python (try py launcher first, then python, then python3)
set PYTHON=
where py >nul 2>&1     && set PYTHON=py
where python >nul 2>&1 && if "%PYTHON%"=="" set PYTHON=python
where python3 >nul 2>&1 && if "%PYTHON%"=="" set PYTHON=python3

if "%PYTHON%"=="" (
    echo.
    echo  ERROR: Python not found!
    echo  Please install Python from https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

:: Launch the app
echo.
echo  Starting NetAudit Pro...
echo  A browser window will open automatically.
echo.
%PYTHON% launch.py
pause
