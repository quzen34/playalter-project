@echo off
REM PLAYALTER Environment Setup Script for Windows
REM This script helps set up different environments safely

echo.
echo 🚀 PLAYALTER Environment Setup
echo ===============================

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo 📋 Creating .env from template...
    
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env created from .env.example
        echo ⚠️  Please edit .env and add your real API keys!
    ) else (
        echo ❌ .env.example not found! Please create it first.
        pause
        exit /b 1
    )
) else (
    echo ✅ .env file found
)

REM Environment selection
echo.
echo 🎯 Select Environment:
echo 1) Development (use real APIs)
echo 2) Testing (use mock APIs)
echo 3) Production (use production APIs)
set /p choice="Choose (1-3): "

if "%choice%"=="1" (
    echo 🔧 Setting up DEVELOPMENT environment...
    echo ✅ Using .env file for development
) else if "%choice%"=="2" (
    echo 🧪 Setting up TESTING environment...
    if exist .env.test (
        copy .env.test .env >nul
        echo ✅ Using .env.test (safe mock values)
    ) else (
        echo ❌ .env.test not found!
        pause
        exit /b 1
    )
) else if "%choice%"=="3" (
    echo 🚀 Setting up PRODUCTION environment...
    echo ⚠️  Make sure all production secrets are properly configured!
    echo ⚠️  Never commit production secrets to git!
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

REM Git safety check
echo.
echo 🔒 Git Safety Check...
findstr /C:".env" .gitignore >nul 2>&1
if %errorlevel%==0 (
    echo ✅ .env is properly ignored by git
) else (
    echo ⚠️  Adding .env to .gitignore for safety...
    echo. >> .gitignore
    echo # Environment files - NEVER COMMIT! >> .gitignore
    echo .env >> .gitignore
    echo ✅ .env added to .gitignore
)

REM Backend setup
echo.
echo 🐍 Backend Setup...
if exist backend (
    cd backend
    if exist requirements.txt (
        echo 📦 Installing Python dependencies...
        pip install -r requirements.txt
        echo ✅ Backend dependencies installed
    )
    cd ..
) else (
    echo ⚠️  Backend directory not found
)

REM Frontend setup
echo.
echo ⚛️  Frontend Setup...
if exist frontend (
    cd frontend
    if exist package.json (
        echo 📦 Installing Node.js dependencies...
        npm install
        echo ✅ Frontend dependencies installed
    )
    cd ..
) else (
    echo ⚠️  Frontend directory not found
)

echo.
echo 🎉 Environment setup complete!
echo.
echo 🔧 Next steps:
echo 1. Edit .env with your real API keys (for development)
echo 2. Start backend: cd backend ^&^& python app_enhanced.py
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo 4. Visit: http://localhost:5173
echo.
echo 📚 Documentation:
echo - API: http://localhost:8000
echo - Health: http://localhost:8000/health
echo - Stripe: Configure webhooks to http://localhost:8000/api/stripe-webhook
echo - n8n: Configure workflows at http://localhost:5678
echo.
pause
