# PLAYALTER Project Structure

## 📁 Project Overview
A full-stack AI application for face swapping and AR mask operations with n8n workflow automation and Stripe payment integration.

## 🏗️ Architecture
```
playalter-project/
├── 🎛️ backend/                    # Flask API Server
│   ├── app_enhanced.py            # Main application (KEEP)
│   ├── requirements_enhanced.txt  # Python dependencies (KEEP)
│   ├── .env                       # Backend environment variables (KEEP)
│   ├── .env.example              # Environment template (KEEP)
│   ├── README.md                 # Backend documentation (KEEP)
│   └── test_backend.py           # Backend tests (KEEP)
│
├── 🌐 frontend/                   # React Frontend
│   ├── src/                      # Source code (KEEP ALL)
│   │   ├── components/           # Reusable components
│   │   ├── pages/               # Route pages
│   │   ├── services/            # API services
│   │   └── App.jsx              # Main app component
│   ├── package.json             # Node.js dependencies (KEEP)
│   ├── vite.config.js           # Vite configuration (KEEP)
│   ├── tailwind.config.js       # Tailwind CSS config (KEEP)
│   ├── .env                     # Frontend environment variables (KEEP)
│   └── index.html               # HTML entry point (KEEP)
│
├── 🔄 n8n/                       # Workflow automation
│   └── workflows/               # n8n workflow definitions (KEEP)
│
├── 🐳 docker-compose.yml         # Docker services config (KEEP)
├── 📋 .env                       # Global environment variables (KEEP)
├── 🚀 start.bat                  # Full application startup (KEEP)
├── 🌐 start-backend.bat          # Backend only startup (NEW)
├── 🎨 start-frontend.bat         # Frontend only startup (NEW)
├── 🐳 start-docker.bat           # Docker services only (NEW)
├── 📚 README.md                  # Main documentation (KEEP)
└── 🐍 .venv/                     # Python virtual environment (KEEP)
```

## 🧹 Cleanup Actions Performed

### ❌ Removed Files/Folders:
- `app.py` - Redundant basic backend
- `app_simple.py` - Redundant simple backend  
- `requirements.txt` - Redundant basic requirements
- `requirements_simple.txt` - Redundant simple requirements
- `backend/__pycache__/` - Python cache files
- `backend/venv/` - Old virtual environment
- `node_modules/` (root) - Misplaced Node.js modules

### 📁 Moved Files:
- `test_backend.py` → `backend/test_backend.py`

### ✅ Added Files:
- `start-backend.bat` - Backend-only startup script
- `start-frontend.bat` - Frontend-only startup script  
- `start-docker.bat` - Docker services startup script
- `PROJECT_STRUCTURE.md` - This documentation

## 🚀 Quick Start Commands

### Full Application
```bash
start.bat                    # Windows - All services
./start.sh                   # Linux/Mac - All services
```

### Individual Services
```bash
start-backend.bat           # Backend only
start-frontend.bat          # Frontend only  
start-docker.bat           # Docker services only
```

### Development
```bash
# Backend development
cd backend
python app_enhanced.py

# Frontend development  
cd frontend
npm run dev

# Run tests
cd backend
python test_backend.py
```

## 🔗 Service URLs
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:5000  
- **n8n Interface**: http://localhost:5678
- **Health Check**: http://localhost:5000/health

## 📊 Current Status
- ✅ Frontend: React + Vite + Tailwind CSS
- ✅ Backend: Flask + n8n + Stripe + OpenAI
- ✅ Database: PostgreSQL (Docker)
- ✅ Cache: Redis (Docker)
- ✅ Workflows: n8n (Docker)
- ✅ Payments: Stripe integration
- ✅ AI: OpenAI integration

## 🔧 Environment Files Required
- `backend/.env` - Backend configuration
- `frontend/.env` - Frontend configuration  
- `.env` - Global configuration (root)

## 📝 Key Features
- 🔄 Face swap operations
- 🎭 AR mask application
- 💳 Stripe payment processing
- 🤖 n8n workflow automation
- 🧠 OpenAI AI integration
- 📊 Real-time health monitoring
- 🎨 Modern React UI with Tailwind CSS
