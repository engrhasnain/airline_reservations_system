@echo off
title Airline Reservation System - Install Requirements
echo ============================================
echo Installing Python and Node.js.
echo If Windows shows a permission popup, click Yes.
echo ============================================
echo.

where winget >nul 2>nul
if errorlevel 1 goto :no_winget

winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
winget install --id OpenJS.NodeJS.LTS -e --accept-package-agreements --accept-source-agreements

echo.
echo ============================================
echo Done! Please RESTART THE COMPUTER now.
echo After restarting, double-click start-backend.bat
echo and then start-frontend.bat.
echo ============================================
pause
exit /b 0

:no_winget
echo winget was not found on this computer.
echo Please install manually instead:
echo   Python:  https://www.python.org/downloads/
echo            check "Add python.exe to PATH" during install
echo   Node.js: https://nodejs.org/ - the LTS version
pause
exit /b 1
