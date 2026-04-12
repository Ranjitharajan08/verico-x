@echo off
title VaricoseAI Platform
color 0A
cls

echo.
echo  =========================================
echo   VaricoseAI  ^|  Vascular Diagnostic AI
echo  =========================================
echo.

:: ── Step 1: Check Python ──────────────────
echo  [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found. Install from https://python.org
    pause & exit /b 1
)
echo         OK

:: ── Step 2: Install dependencies ─────────
echo  [2/4] Installing dependencies...
pip install -r requirements.txt -q --disable-pip-version-check
echo         OK

:: ── Step 3: Train model if best.pt missing ─
if not exist "best.pt" (
    echo.
    echo  [3/4] best.pt not found.
    echo        Running training pipeline on your dataset...
    echo        This may take 10-30 minutes depending on your hardware.
    echo.
    python train.py
    if %errorlevel% neq 0 (
        echo.
        echo  WARNING: Training exited with errors. Check output above.
        echo  The server will start with the base YOLOv8n model as fallback.
        echo.
    )
) else (
    echo  [3/4] Trained model found. Skipping training.
)

:: ── Step 4: Start server ──────────────────
echo  [4/4] Clearing port 8001...
for /f "tokens=5" %%P in ('netstat -ano 2^>nul ^| findstr ":8001 "') do (
    taskkill /PID %%P /F >nul 2>&1
)

echo.
echo  Starting VaricoseAI server...
echo  Browser will open in 4 seconds.
echo  Keep this window open while using the app.
echo  Press Ctrl+C to stop the server.
echo  =========================================
echo.

start "" /b cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:8001"

cd /d "%~dp0"
python app.py

echo.
echo  Server stopped. Press any key to exit.
pause >nul
