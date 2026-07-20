@echo off
title Airline Reservation System - Backend
cd /d "%~dp0backend"

python --version > "%TEMP%\airline_pycheck.txt" 2>&1

findstr /c:"was not found" "%TEMP%\airline_pycheck.txt" >nul
if not errorlevel 1 goto :no_python

findstr /b /c:"Python " "%TEMP%\airline_pycheck.txt" >nul
if errorlevel 1 goto :no_python

del "%TEMP%\airline_pycheck.txt" >nul 2>&1
goto :python_ok

:no_python
del "%TEMP%\airline_pycheck.txt" >nul 2>&1
echo ============================================
echo Python is not installed on this computer yet.
echo.
echo Fastest fix - open Command Prompt and run:
echo   winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
echo.
echo Or install manually from https://www.python.org/downloads/
echo and check "Add python.exe to PATH" during install.
echo.
echo Then restart the computer and double-click this file again.
echo ============================================
pause
exit /b 1

:python_ok
if not exist venv (
    echo ============================================
    echo First-time setup - installing backend packages.
    echo This can take a minute or two, please wait.
    echo ============================================
    python -m venv venv
    call "venv\Scripts\activate.bat"
    pip install -r requirements.txt
) else (
    call "venv\Scripts\activate.bat"
)

if not exist .env (
    copy .env.example .env >nul
)

echo.
echo ============================================
echo Backend is starting at http://127.0.0.1:8000
echo Keep this window open. Do not close it.
echo ============================================
echo.
uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
