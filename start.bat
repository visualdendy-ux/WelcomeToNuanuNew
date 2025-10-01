@echo off
echo ========================================
echo   NUANU WiFi Login Portal
echo ========================================
echo.
echo Starting Python FastAPI server...
echo.
echo Login page: http://localhost:8000/
echo Admin dashboard: http://localhost:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app:app --reload --host 0.0.0.0 --port 8000
