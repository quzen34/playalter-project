#!/bin/bash

# PLAYALTER Backend Startup Script

echo "🚀 Starting PLAYALTER Backend with n8n Integration"

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your actual API keys"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements_enhanced.txt

# Start Docker services (n8n, Redis, PostgreSQL)
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if n8n is running
echo "🔍 Checking n8n status..."
curl -f http://localhost:5678/healthz > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ n8n is running"
else
    echo "❌ n8n is not responding"
fi

# Start Flask backend
echo "🌐 Starting Flask backend..."
cd backend
python app_enhanced.py

echo "🎉 PLAYALTER Backend is now running!"
echo "🔗 Backend API: http://localhost:5000"
echo "🔗 Frontend: http://localhost:4001"
echo "🔗 n8n Interface: http://localhost:5678"
echo "🔐 n8n Credentials: admin / playalter123"
