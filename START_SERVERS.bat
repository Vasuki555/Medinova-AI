@echo off
echo ========================================
echo   MediNova AI - Starting Servers
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "MediNova Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server...
start "MediNova Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
