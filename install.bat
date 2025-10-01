@echo off
echo ========================================
echo   NUANU WiFi Login Portal
echo   Installation Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit .env with your credentials
echo 3. Run: start.bat
echo.
echo Or run manually:
echo   venv\Scripts\activate
echo   uvicorn app:app --reload --port 8000
echo.
pause
