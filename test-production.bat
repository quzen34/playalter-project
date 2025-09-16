@echo off
REM PLAYALTER Production Domain Test Script for Windows
REM Tests all endpoints on www.playalter.com

echo 🧪 Testing PLAYALTER on www.playalter.com
echo ==========================================

set "BASE_URL=https://www.playalter.com"
set "API_URL=%BASE_URL%/api"

echo.
echo 🔍 Basic Connectivity Tests
echo ----------------------------

REM Test 1: Health Check
echo Testing GET /health...
curl -s "%API_URL%/health" > nul
if %errorlevel% equ 0 (
    echo ✅ Health check PASS
) else (
    echo ❌ Health check FAIL
)

REM Test 2: Home endpoint
echo Testing GET /...
curl -s "%API_URL%/" > nul
if %errorlevel% equ 0 (
    echo ✅ Home endpoint PASS
) else (
    echo ❌ Home endpoint FAIL
)

echo.
echo 🤖 AI Services Tests
echo --------------------

REM Test 3: AI Agents List
echo Testing GET /ai-agents...
curl -s "%API_URL%/ai-agents" > nul
if %errorlevel% equ 0 (
    echo ✅ AI Agents PASS
) else (
    echo ❌ AI Agents FAIL
)

REM Test 4: Face Swap (Mock)
echo Testing POST /face-swap...
curl -s -X POST -H "Content-Type: application/json" -d "{\"source_base64\":\"data:image/jpeg;base64,test\",\"target_base64\":\"data:image/jpeg;base64,test\",\"user_id\":\"test_user\"}" "%API_URL%/face-swap" > nul
if %errorlevel% equ 0 (
    echo ✅ Face Swap PASS
) else (
    echo ❌ Face Swap FAIL
)

REM Test 5: AR Mask
echo Testing POST /ar-mask...
curl -s -X POST -H "Content-Type: application/json" -d "{\"image\":\"data:image/jpeg;base64,test\",\"mask_type\":\"cat_ears\",\"user_id\":\"test_user\"}" "%API_URL%/ar-mask" > nul
if %errorlevel% equ 0 (
    echo ✅ AR Mask PASS
) else (
    echo ❌ AR Mask FAIL
)

echo.
echo 🧠 Grok AI Tests
echo ----------------

REM Test 6: Grok Chat
echo Testing POST /grok/chat...
curl -s -X POST -H "Content-Type: application/json" -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hello, test message\"}]}" "%API_URL%/grok/chat" > nul
if %errorlevel% equ 0 (
    echo ✅ Grok Chat PASS
) else (
    echo ❌ Grok Chat FAIL
)

echo.
echo 💳 Stripe Integration Tests
echo ---------------------------

REM Test 7: Create Customer
echo Testing POST /customers...
curl -s -X POST -H "Content-Type: application/json" -d "{\"email\":\"test@playalter.com\",\"name\":\"Test User\"}" "%API_URL%/customers" > nul
if %errorlevel% equ 0 (
    echo ✅ Stripe Customer PASS
) else (
    echo ❌ Stripe Customer FAIL
)

echo.
echo 🔄 N8N Workflow Tests
echo ---------------------

REM Test 8: N8N Workflows List
echo Testing GET /n8n/workflows...
curl -s "%API_URL%/n8n/workflows" > nul
if %errorlevel% equ 0 (
    echo ✅ N8N Workflows PASS
) else (
    echo ❌ N8N Workflows FAIL
)

echo.
echo 🏁 Test Summary
echo ================

REM Frontend accessibility test
echo Testing frontend accessibility...
curl -s "%BASE_URL%" > nul
if %errorlevel% equ 0 (
    echo ✅ Frontend accessible
) else (
    echo ❌ Frontend not accessible
)

echo.
echo 🎉 Production testing completed for www.playalter.com
echo Visit: %BASE_URL%
echo API: %API_URL%

pause
