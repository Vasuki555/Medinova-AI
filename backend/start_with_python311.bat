@echo off
echo ========================================
echo Starting MediNova Backend with Python 3.11
echo (For real-time MongoDB Atlas connection)
echo ========================================
echo.

REM Use Python 3.11 instead of Python 3.14
py -3.11 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
