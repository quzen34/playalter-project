@echo off
REM PLAYALTER Quick Start Script - Orchestrated Platform Integration

title PLAYALTER - AI Platform Orchestrator

echo.
echo 🎭 PLAYALTER - AI Face Swap ^& AR Platform
echo =============================================
echo.
echo 🚀 Platform Integration Status:
echo   N8N:       Workflow Automation     (Port 5678)
echo   Stripe:    Payment Processing      (API)
echo   Vercel:    Deployment Platform     (Web)
echo   OpenAI:    AI Capabilities         (API)
echo   Replicate: Face Swap AI            (API)
echo   Agora:     Live Streaming          (RTM)
echo.

REM Check if environment is set up
if not exist .env (
    echo ⚠️  Environment not configured! Running setup...
    call setup-env.bat
    echo.
)

REM Create logs directory
if not exist logs mkdir logs

echo 🔍 Checking system requirements...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)

echo ✅ System requirements met
echo.

echo 🎯 Choose startup mode:
echo   1) Full Development (All services)
echo   2) Backend Only (Flask API)
echo   3) Frontend Only (React App)
echo   4) Integration Test
echo   5) Docker Production
echo.
set /p choice="Select mode (1-5): "

if "%choice%"=="1" goto FULL_DEV
if "%choice%"=="2" goto BACKEND_ONLY
if "%choice%"=="3" goto FRONTEND_ONLY
if "%choice%"=="4" goto INTEGRATION_TEST
if "%choice%"=="5" goto DOCKER_PROD
goto FULL_DEV

:FULL_DEV
echo.
echo 🚀 Starting Full Development Environment...
echo.

REM Kill any existing processes
echo 🔄 Cleaning up existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul

REM Start backend in new window
echo � Starting Backend (Flask - Port 8000)...
start "PLAYALTER Backend" cmd /c "cd backend && python app_enhanced.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window  
echo ⚛️  Starting Frontend (React - Port 5173)...
start "PLAYALTER Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo ✅ Development environment started!
echo.
echo 📋 Service URLs:
echo   🌐 Frontend:     http://localhost:5173
echo   🔧 Backend API:  http://localhost:8000
echo   ❤️  Health:       http://localhost:8000/health
echo.

timeout /t 2 /nobreak >nul
start http://localhost:5173
goto END

:BACKEND_ONLY
echo.
echo 🐍 Starting Backend Only...
echo.

cd backend
if not exist ".venv" (
    echo 🔧 Creating Python virtual environment...
    python -m venv .venv
)

echo 🔄 Activating virtual environment...
call .venv\Scripts\activate

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🚀 Starting Platform Orchestrator...
python platform_orchestrator.py

goto END

:FRONTEND_ONLY
echo.
echo ⚛️  Starting Frontend Only...
echo.

cd frontend
echo 📦 Installing dependencies...
npm install

echo 🚀 Starting React development server...
npm run dev

goto END

:INTEGRATION_TEST
echo.
echo 🧪 Running Integration Tests...
echo.

cd backend
if not exist ".venv" (
    echo 🔧 Creating Python virtual environment...
    python -m venv .venv
)

echo 🔄 Activating virtual environment...
call .venv\Scripts\activate

echo 📦 Installing test dependencies...
pip install -r requirements.txt

echo 🧪 Running comprehensive platform tests...
python test_integration.py

echo.
echo 📊 Test Results: Check logs/test_results.log for details
pause
goto END

:DOCKER_PROD
echo.
echo 🐳 Starting Docker Production Environment...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found! Please install Docker Desktop
    pause
    exit /b 1
)

echo 🔧 Building Docker containers...
docker-compose build

echo 🚀 Starting production services...
docker-compose up -d

echo.
echo ✅ Production environment started!
echo.
echo � Service URLs:
echo   🌐 Application:  http://localhost:8000
echo   � N8N:          http://localhost:5678
echo   � Health:       http://localhost:8000/health
echo.

timeout /t 2 /nobreak >nul
start http://localhost:8000
goto END

:END
echo.
echo 🎉 PLAYALTER platform is ready!
echo.
echo � Next Steps:
echo   1. Check health status: http://localhost:8000/health
echo   2. Run integration tests: python test_integration.py
echo   3. Check logs: logs/orchestrator.log
echo.
echo 💡 Pro Tips:
echo   - Use Ctrl+C to stop services
echo   - Check .env.example for configuration
echo   - Run setup-env.bat for fresh setup
echo.
pause
