@echo off
REM Double-click to launch the autoaim using this project's isolated venv.
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    echo .venv not found. Create it with:  python -m venv .venv
    echo Then install deps:  .venv\Scripts\python.exe -m pip install -r requirements.txt
    python main.py
)
echo.
echo ---- script exited ---- (window stays open so you can read any errors)
pause
