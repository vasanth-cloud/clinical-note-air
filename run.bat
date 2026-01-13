@echo off
REM Kill any process listening on 8000 (uses netstat to find PID) and start uvicorn
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing PID %%a
    taskkill /PID %%a /F >nul 2>&1
)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
