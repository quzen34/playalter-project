#!/bin/bash

# PLAYALTER Environment Setup Script
# This script helps set up different environments safely

echo "🚀 PLAYALTER Environment Setup"
echo "==============================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📋 Creating .env from template..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created from .env.example"
        echo "⚠️  Please edit .env and add your real API keys!"
    else
        echo "❌ .env.example not found! Please create it first."
        exit 1
    fi
else
    echo "✅ .env file found"
fi

# Environment selection
echo ""
echo "🎯 Select Environment:"
echo "1) Development (use real APIs)"
echo "2) Testing (use mock APIs)"
echo "3) Production (use production APIs)"
read -p "Choose (1-3): " choice

case $choice in
    1)
        echo "🔧 Setting up DEVELOPMENT environment..."
        # Use real .env file
        echo "✅ Using .env file for development"
        ;;
    2)
        echo "🧪 Setting up TESTING environment..."
        if [ -f .env.test ]; then
            cp .env.test .env
            echo "✅ Using .env.test (safe mock values)"
        else
            echo "❌ .env.test not found!"
            exit 1
        fi
        ;;
    3)
        echo "🚀 Setting up PRODUCTION environment..."
        echo "⚠️  Make sure all production secrets are properly configured!"
        echo "⚠️  Never commit production secrets to git!"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Git safety check
echo ""
echo "🔒 Git Safety Check..."
if grep -q "\.env$" .gitignore; then
    echo "✅ .env is properly ignored by git"
else
    echo "⚠️  Adding .env to .gitignore for safety..."
    echo "" >> .gitignore
    echo "# Environment files - NEVER COMMIT!" >> .gitignore
    echo ".env" >> .gitignore
    echo "✅ .env added to .gitignore"
fi

# Backend setup
echo ""
echo "🐍 Backend Setup..."
cd backend 2>/dev/null
if [ $? -eq 0 ]; then
    if [ -f requirements.txt ]; then
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
        echo "✅ Backend dependencies installed"
    fi
    cd ..
else
    echo "⚠️  Backend directory not found"
fi

# Frontend setup
echo ""
echo "⚛️  Frontend Setup..."
cd frontend 2>/dev/null
if [ $? -eq 0 ]; then
    if [ -f package.json ]; then
        echo "📦 Installing Node.js dependencies..."
        npm install
        echo "✅ Frontend dependencies installed"
    fi
    cd ..
else
    echo "⚠️  Frontend directory not found"
fi

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit .env with your real API keys (for development)"
echo "2. Start backend: cd backend && python app_enhanced.py"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Visit: http://localhost:5173"
echo ""
echo "📚 Documentation:"
echo "- API: http://localhost:8000"
echo "- Health: http://localhost:8000/health"
echo "- Stripe: Configure webhooks to http://localhost:8000/api/stripe-webhook"
echo "- n8n: Configure workflows at http://localhost:5678"
