@echo off
echo 🌐 Starting PLAYALTER Backend Only
echo ===================================

REM Activate virtual environment
call .venv\Scripts\activate

REM Start backend
cd backend
python app_enhanced.py

pause
