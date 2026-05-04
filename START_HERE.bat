@echo off
title Vidyalaya Pro ERP - Setup
color 0A
echo.
echo  ============================================
echo   VIDYALAYA PRO - School Management ERP
echo   Developed by: Saadat (AI Tech Channel)
echo  ============================================
echo.
echo  [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from python.org
    echo  Remember to check "Add Python to PATH"
    pause
    exit
)
echo  Python found OK

echo.
echo  [2/3] Installing required libraries...
pip install flask flask-sqlalchemy werkzeug cryptography --quiet
echo  Libraries installed OK

echo.
echo  [3/3] Starting Vidyalaya Pro ERP...
echo.
echo  Browser will open automatically...
echo  To stop: Close this window or press Ctrl+C
echo.
python launcher.py
pause
