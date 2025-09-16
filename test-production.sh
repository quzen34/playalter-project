#!/bin/bash

# PLAYALTER Production Domain Test Script
# Tests all endpoints on www.playalter.com

echo "🧪 Testing PLAYALTER on www.playalter.com"
echo "=========================================="

BASE_URL="https://www.playalter.com"
API_URL="$BASE_URL/api"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=$3
    
    echo -n "Testing $method $endpoint... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" -o /tmp/response "$API_URL$endpoint")
    else
        response=$(curl -s -w "%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" -o /tmp/response "$API_URL$endpoint")
    fi
    
    if [ "$response" -eq 200 ] || [ "$response" -eq 201 ]; then
        echo -e "${GREEN}✅ PASS (HTTP $response)${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL (HTTP $response)${NC}"
        echo "Response: $(cat /tmp/response)"
        return 1
    fi
}

# Start tests
echo ""
echo "🔍 Basic Connectivity Tests"
echo "----------------------------"

# Test 1: Health Check
test_endpoint "/health"

# Test 2: Home endpoint
test_endpoint "/"

echo ""
echo "🤖 AI Services Tests"
echo "--------------------"

# Test 3: AI Agents List
test_endpoint "/ai-agents"

# Test 4: Face Swap (Mock)
test_endpoint "/face-swap" "POST" '{"source_base64":"data:image/jpeg;base64,test","target_base64":"data:image/jpeg;base64,test","user_id":"test_user"}'

# Test 5: AR Mask
test_endpoint "/ar-mask" "POST" '{"image":"data:image/jpeg;base64,test","mask_type":"cat_ears","user_id":"test_user"}'

# Test 6: Face Ethics
test_endpoint "/face-ethics" "POST" '{"image_base64":"data:image/jpeg;base64,test"}'

# Test 7: Live Stream Token
test_endpoint "/live-stream" "POST" '{"channel_name":"test_channel","uid":12345}'

echo ""
echo "🧠 Grok AI Tests"
echo "----------------"

# Test 8: Grok Chat
test_endpoint "/grok/chat" "POST" '{"messages":[{"role":"user","content":"Hello, test message"}]}'

# Test 9: Grok Reasoning
test_endpoint "/grok/reason" "POST" '{"question":"What is AI?","context":"Testing PLAYALTER system"}'

echo ""
echo "💳 Stripe Integration Tests"
echo "---------------------------"

# Test 10: Create Customer
test_endpoint "/customers" "POST" '{"email":"test@playalter.com","name":"Test User"}'

# Test 11: Create Checkout Session
test_endpoint "/create-checkout-session" "POST" '{"email":"test@playalter.com"}'

echo ""
echo "🔄 N8N Workflow Tests"
echo "---------------------"

# Test 12: N8N Workflows List
test_endpoint "/n8n/workflows"

# Test 13: Orchestration
test_endpoint "/orchestrate" "POST" '{"operation":"general","request":"Test orchestration","user_id":"test_user"}'

echo ""
echo "🔧 DevOps Tests"
echo "---------------"

# Test 14: Deploy endpoint
test_endpoint "/deploy" "POST" '{"environment":"production","platform":"vercel"}'

echo ""
echo "📝 User Testing"
echo "---------------"

# Test 15: User Feedback
test_endpoint "/user-test" "POST" '{"user_id":"test_user","feedback":"Great platform! Love the AI features.","test_type":"production","rating":5}'

echo ""
echo "🏁 Test Summary"
echo "================"

# Frontend accessibility test
echo -n "Testing frontend accessibility... "
frontend_response=$(curl -s -w "%{http_code}" -o /dev/null "$BASE_URL")
if [ "$frontend_response" -eq 200 ]; then
    echo -e "${GREEN}✅ Frontend accessible${NC}"
else
    echo -e "${RED}❌ Frontend not accessible (HTTP $frontend_response)${NC}"
fi

# API documentation test
echo -n "Testing API documentation... "
api_docs_response=$(curl -s -w "%{http_code}" -o /dev/null "$API_URL")
if [ "$api_docs_response" -eq 200 ]; then
    echo -e "${GREEN}✅ API docs accessible${NC}"
else
    echo -e "${RED}❌ API docs not accessible (HTTP $api_docs_response)${NC}"
fi

echo ""
echo -e "${YELLOW}🎉 Production testing completed for www.playalter.com${NC}"
echo -e "${YELLOW}Visit: $BASE_URL${NC}"
echo -e "${YELLOW}API: $API_URL${NC}"

# Cleanup
rm -f /tmp/response
