@echo off
:: ============================================================
::  NetAudit Pro — Double-Click Launcher
::  Auto-installs dependencies + requests admin rights
:: ============================================================

:: Check if already running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :ALREADY_ADMIN
)

:: Not admin — re-launch elevated via PowerShell (UAC popup)
echo Requesting admin rights...
PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
exit /b

:ALREADY_ADMIN
cd /d "%~dp0"

:: Find Python
set PYTHON=
where py >nul 2>&1      && set PYTHON=py
where python >nul 2>&1  && if "%PYTHON%"=="" set PYTHON=python
where python3 >nul 2>&1 && if "%PYTHON%"=="" set PYTHON=python3

if "%PYTHON%"=="" (
    echo.
    echo  ============================================================
    echo   ERROR: Python not found!
    echo   Please install Python from https://python.org
    echo   Make sure to check "Add Python to PATH" during install.
    echo  ============================================================
    echo.
    pause
    exit /b 1
)

:: ── AUTO INSTALL DEPENDENCIES ─────────────────────────────
echo.
echo  ============================================================
echo   Checking dependencies...
echo  ============================================================
echo.

%PYTHON% -c "import reportlab" >nul 2>&1
if %errorLevel% neq 0 (
    echo  Installing reportlab...
    %PYTHON% -m pip install reportlab --quiet
    echo  reportlab installed!
)

%PYTHON% -c "import scapy" >nul 2>&1
if %errorLevel% neq 0 (
    echo  Installing scapy...
    %PYTHON% -m pip install scapy --quiet
    echo  scapy installed!
)

%PYTHON% -c "import PIL" >nul 2>&1
if %errorLevel% neq 0 (
    echo  Installing pillow...
    %PYTHON% -m pip install pillow --quiet
    echo  pillow installed!
)

echo.
echo  All dependencies ready!
echo  ============================================================
echo.

:: ── LAUNCH APP ────────────────────────────────────────────
echo  Starting NetAudit Pro...
echo  Browser will open automatically.
echo.
%PYTHON% launch.py
pause