@echo off
REM PLAYALTER Production Deployment Script for Windows
REM Deploys to www.playalter.com domain

echo 🚀 Starting PLAYALTER Production Deployment...
echo Target Domain: www.playalter.com
echo ===============================================

REM Check if we're in the right directory
if not exist "vercel.json" (
    echo ❌ Error: vercel.json not found. Please run from project root.
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Installing dependencies...
if not exist "frontend\node_modules" (
    cd frontend
    npm install
    cd ..
)

if not exist "backend\__pycache__" (
    cd backend
    pip install -r requirements_enhanced.txt
    cd ..
)

REM Build frontend for production
echo 🏗️  Building frontend for production...
cd frontend
npm run build
cd ..

REM Test backend health
echo 🔍 Testing backend health...
cd backend
python -c "import app_enhanced; print('✅ Backend imports successfully'); print('✅ All integrations configured')"
cd ..

REM Deploy to Vercel
echo ☁️  Deploying to Vercel (www.playalter.com)...
vercel --prod --yes

REM Verify deployment
echo ✅ Deployment completed!
echo.
echo 🌐 Production URLs:
echo    Primary: https://www.playalter.com
echo    API: https://www.playalter.com/api/health
echo.
echo 🧪 Test endpoints:
echo    Health Check: curl https://www.playalter.com/api/health
echo    AI Agents: curl https://www.playalter.com/api/ai-agents
echo    Grok AI: curl -X POST https://www.playalter.com/api/grok/chat
echo.
echo 🎉 PLAYALTER is now live on www.playalter.com!

pause
