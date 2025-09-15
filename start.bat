@echo off
echo 🚀 Starting PLAYALTER Full-Stack Application
echo ============================================

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  Backend .env file not found. Please check your configuration.
    pause
    exit /b 1
)

if not exist "frontend\.env" (
    echo ⚠️  Frontend .env file not found. Please check your configuration.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo 🐍 Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔄 Activating Python virtual environment...
call .venv\Scripts\activate

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r backend\requirements_enhanced.txt

REM Install Frontend dependencies
echo 📦 Installing Frontend dependencies...
cd frontend
npm install
cd ..

REM Start Docker services in background
echo 🐳 Starting Docker services...
start "Docker Services" docker-compose up

REM Wait for services
echo ⏳ Waiting for Docker services to start...
timeout /t 15 /nobreak > nul

REM Start backend in new window
echo 🌐 Starting Flask backend...
start "PLAYALTER Backend" cmd /k "cd backend && python app_enhanced.py"

REM Wait for backend to start
timeout /t 5 /nobreak > nul

REM Start frontend in new window
echo 🌐 Starting React frontend...
start "PLAYALTER Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo 🎉 PLAYALTER Application is starting!
echo ============================================
echo 🔗 Frontend: http://localhost:5173
echo 🔗 Backend API: http://localhost:5000
echo 🔗 n8n Interface: http://localhost:5678
echo ============================================
echo Press any key to stop all services...
pause

echo 🛑 Stopping all services...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
docker-compose down
echo ✅ All services stopped.
pause
