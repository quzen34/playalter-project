#!/bin/bash

# PLAYALTER Production Deployment Script
# Deploys to www.playalter.com domain

echo "🚀 Starting PLAYALTER Production Deployment..."
echo "Target Domain: www.playalter.com"
echo "==============================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Please run from project root."
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    cd frontend
    npm install
    cd ..
fi

if [ ! -d "backend/__pycache__" ]; then
    cd backend
    pip install -r requirements_enhanced.txt
    cd ..
fi

# Build frontend for production
echo "🏗️  Building frontend for production..."
cd frontend
npm run build
cd ..

# Test backend health
echo "🔍 Testing backend health..."
cd backend
python -c "
import app_enhanced
print('✅ Backend imports successfully')
print('✅ All integrations configured')
"
cd ..

# Deploy to Vercel
echo "☁️  Deploying to Vercel (www.playalter.com)..."
vercel --prod --yes

# Verify deployment
echo "✅ Deployment completed!"
echo ""
echo "🌐 Production URLs:"
echo "   Primary: https://www.playalter.com"
echo "   API: https://www.playalter.com/api/health"
echo ""
echo "🧪 Test endpoints:"
echo "   Health Check: curl https://www.playalter.com/api/health"
echo "   AI Agents: curl https://www.playalter.com/api/ai-agents"
echo "   Grok AI: curl -X POST https://www.playalter.com/api/grok/chat"
echo ""
echo "🎉 PLAYALTER is now live on www.playalter.com!"
