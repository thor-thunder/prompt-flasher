@echo off
cd /d "%~dp0"

:: ── Check python ──────────────────────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [Installer Script] python not found.
    echo [Installer Script] Please install Python 3 from https://www.python.org/downloads/
    echo [Installer Script] Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

:: ── Create venv if missing ────────────────────────────────────────────────────
if not exist venv (
    echo [Installer Script] Creating virtual environment...
    python -m venv venv
)

:: ── Install/update dependencies ───────────────────────────────────────────────
echo [Installer Script] Installing dependencies...
venv\Scripts\pip install --quiet --upgrade pip
venv\Scripts\pip install --quiet -r requirements.txt

:: ── Launch ────────────────────────────────────────────────────────────────────
echo [Installer Script] Starting server -^> http://localhost:3000
venv\Scripts\python -m uvicorn server:app --host 0.0.0.0 --port 3000
pause
