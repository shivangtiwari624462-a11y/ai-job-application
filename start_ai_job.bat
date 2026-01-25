@echo off
echo ==============================
echo AI JOB APPLICATION SYSTEM STARTING
echo ==============================

cd /d "%~dp0"

call venv\Scripts\activate

python main.py

pause
