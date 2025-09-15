# PLAYALTER: AI Face Swap & AR Web App

A full-stack AI application featuring face swapping and AR mask operations with React frontend, Flask backend, n8n workflow automation, and Stripe payment integration.

## 🚀 Features

### 🎯 Core AI Services
- **Face Swap**: Advanced AI-powered face swapping with real-time processing
- **AR Masks**: Augmented reality mask application with multiple styles
- **AI Orchestration**: Intelligent workflow coordination and task management

### 💳 Payment & Subscription Management
- **Stripe Integration**: Complete payment processing system
- **Subscription Management**: Recurring billing and subscription lifecycle
- **Customer Management**: Comprehensive customer data management

### 🔄 Workflow Automation (n8n)
- **Automated Workflows**: Face swap and AR mask processing pipelines
- **Payment Workflows**: Automated billing and notification systems
- **Email Notifications**: Automated customer communication

### 🌐 Modern Frontend
- **React Interface**: Modern, responsive UI with Tailwind CSS
- **Real-time Updates**: Live status updates and progress tracking
- **Payment Forms**: Integrated Stripe Elements for secure payments

## 📋 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │────│   Flask API     │────│   n8n Workflows │
│   Frontend      │    │   Backend       │    │   (Automation)  │
│   :3001         │    │   :5000         │    │   :5678         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │  Stripe API     │    │  AI Services    │
                    │  (Payments)     │    │  (OpenAI)       │
                    └─────────────────┘    └─────────────────┘
```

## 🛠️ Quick Start

### 🚀 One-Click Startup (Windows)
```bash
start.bat
```

### 🔧 Individual Services
```bash
start-backend.bat     # Backend only
start-frontend.bat    # Frontend only  
start-docker.bat      # Docker services only
```

### 🐧 Manual Setup
```bash
# Clone repository
git clone https://github.com/quzen34/playalter-project.git
cd playalter-project

# Create Python virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install backend dependencies
pip install -r backend/requirements_enhanced.txt

# Install frontend dependencies  
cd frontend
npm install
cd ..

# Start Docker services
docker-compose up -d

# Start backend
cd backend
python app_enhanced.py

# In another terminal, start frontend
cd frontend  
npm run dev
```

## 🔗 Service URLs

- **🌐 Frontend**: http://localhost:4001
- **🔧 Backend API**: http://localhost:5000  
- **🔄 n8n Interface**: http://localhost:5678
- **❤️ Health Check**: http://localhost:5000/health

## 📁 Project Structure

```
playalter-project/
├── 🎛️ backend/                    # Flask API Server
│   ├── app_enhanced.py            # Main application
│   ├── requirements_enhanced.txt  # Python dependencies
│   ├── .env                       # Backend environment variables
│   └── test_backend.py           # Backend tests
│
├── 🌐 frontend/                   # React Frontend
│   ├── src/                      # Source code
│   │   ├── components/           # Reusable components
│   │   ├── pages/               # Route pages
│   │   ├── services/            # API services
│   │   └── App.jsx              # Main app component
│   ├── package.json             # Node.js dependencies
│   ├── .env                     # Frontend environment variables
│   └── vite.config.js           # Vite configuration
│
├── 🔄 n8n/workflows/             # n8n workflow definitions
├── 🐳 docker-compose.yml         # Docker services configuration
├── 🚀 start.bat                  # Full application startup
└── 📚 PROJECT_STRUCTURE.md       # Detailed structure documentation
```

## 🔧 Environment Configuration

### Backend (.env)
```env
OPENAI_API_KEY=sk-proj-your-openai-key
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
```

### Frontend (.env)
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
```

## 🔗 API Endpoints

### Health & Status
- `GET /health` - Service health check with integration status

### AI Operations  
- `POST /api/orchestrate` - Trigger AI workflow orchestration
- `POST /api/face-swap` - Process face swap operation
- `POST /api/ar-mask` - Apply AR mask to image

### Stripe Integration
- `POST /api/customers` - Create new Stripe customer
- `POST /api/create-checkout-session` - Create payment checkout session
- `GET /api/subscriptions/<customer_id>` - Get customer subscriptions

### n8n Integration
- `GET /api/n8n/workflows` - List available n8n workflows
- `POST /api/n8n/trigger/<workflow_name>` - Manually trigger workflow

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_backend.py
```

### API Testing Examples

**Health Check**:
```bash
curl http://localhost:5000/health
```

**Face Swap**:
```bash
curl -X POST http://localhost:5000/api/face-swap \
  -H "Content-Type: application/json" \
  -d '{
    "source_image": "https://example.com/source.jpg",
    "target_image": "https://example.com/target.jpg",
    "user_id": "user123"
  }'
```

## 🐳 Docker Services

- **n8n**: Workflow automation platform (port 5678)
- **Redis**: Caching and queue management (port 6379)  
- **PostgreSQL**: Database for n8n and application data (port 5432)

## 📊 Current Status

- ✅ **Frontend**: React + Vite + Tailwind CSS (Working)
- ✅ **Backend**: Flask + OpenAI + Stripe (Working)
- ✅ **Database**: PostgreSQL via Docker (Working)
- ✅ **Cache**: Redis via Docker (Working)
- ✅ **Workflows**: n8n via Docker (Available)
- ✅ **Payments**: Stripe integration (Connected)
- ✅ **AI**: OpenAI integration (Configured)

## 🛡️ Security

- Environment variables properly configured
- Stripe webhook signature verification
- CORS properly configured
- Input validation on all endpoints
- Secure API key management

## 🚀 Production Deployment

### Recommended Stack
- **Frontend**: Vercel/Netlify static hosting
- **Backend**: Railway/Heroku/AWS with Gunicorn  
- **Database**: Managed PostgreSQL
- **CDN**: Cloudflare for static assets

### Production Commands
```bash
# Backend with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app

# Frontend build
cd frontend
npm run build
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Create Pull Request

## 📄 License

This project is licensed under the MIT License.

---

**PLAYALTER** - Transforming digital experiences with AI-powered face swap and AR technology.

## 🔗 API Endpoints

### Health & Status
- `GET /health` - Service health check with integration status

### AI Operations
- `POST /api/orchestrate` - Trigger AI workflow orchestration
- `POST /api/face-swap` - Process face swap operation
- `POST /api/ar-mask` - Apply AR mask to image

### Stripe Integration
- `POST /api/customers` - Create new Stripe customer
- `POST /api/products` - Create new Stripe product
- `POST /api/create-checkout-session` - Create payment checkout session
- `GET /api/subscriptions/<customer_id>` - Get customer subscriptions
- `POST /api/stripe-webhook` - Stripe webhook endpoint

### n8n Integration
- `GET /api/n8n/workflows` - List available n8n workflows
- `POST /api/n8n/trigger/<workflow_name>` - Manually trigger workflow

## 🔄 n8n Workflows

### Pre-configured Workflows

1. **Face Swap Processing** (`face-swap-processing`)
   - Receives face swap requests
   - Calls external AI service
   - Processes results and notifications

2. **Stripe Payment Processing** (`payment-succeeded`)
   - Handles successful payments
   - Sends confirmation emails
   - Updates customer records

3. **AR Mask Processing** (`ar-mask-processing`)
   - Applies AR masks to images
   - Real-time processing pipeline
   - Result delivery and storage

### Workflow Triggers
- Webhook-based triggers from Flask backend
- Stripe webhook events
- Manual triggers via API
- Scheduled workflows (configurable)

## 💳 Stripe Configuration

### Required Stripe Setup
1. **Create Stripe Account**: [stripe.com](https://stripe.com)
2. **Get API Keys**: Dashboard → Developers → API Keys
3. **Configure Webhooks**: 
   - Endpoint: `http://your-domain.com/api/stripe-webhook`
   - Events: `payment_intent.succeeded`, `checkout.session.completed`, `customer.subscription.*`
4. **Create Products & Prices**: Use API or Stripe Dashboard

### Webhook Events Handled
- `payment_intent.succeeded` - Payment completion
- `payment_intent.payment_failed` - Payment failure
- `checkout.session.completed` - Checkout completion
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Subscription changes
- `customer.subscription.deleted` - Subscription cancellation
- `invoice.payment_succeeded` - Invoice payment
- `invoice.payment_failed` - Invoice failure

## 🔧 Development

### Backend Structure
```
backend/
├── app.py                 # Original Flask app
├── app_simple.py         # Simplified version
├── app_enhanced.py       # Full integration version
├── requirements.txt      # Basic dependencies
├── requirements_enhanced.txt  # Full dependencies
├── .env.example         # Environment template
└── README.md           # Backend documentation
```

### Running in Development Mode
```bash
# Backend only (simple)
cd backend
python app_simple.py

# Backend with full integration
python app_enhanced.py

# With n8n and databases
docker-compose up -d
python app_enhanced.py
```

### Testing API Endpoints

**Face Swap Example**:
```bash
curl -X POST http://localhost:5000/api/face-swap \
  -H "Content-Type: application/json" \
  -d '{
    "source_image": "https://example.com/source.jpg",
    "target_image": "https://example.com/target.jpg",
    "user_id": "user123"
  }'
```

**Create Checkout Session**:
```bash
curl -X POST http://localhost:5000/api/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{
    "priceId": "price_1234567890",
    "email": "customer@example.com"
  }'
```

## 🐳 Docker Services

The project includes a complete Docker setup:

- **n8n**: Workflow automation platform (port 5678)
- **Redis**: Caching and queue management (port 6379)
- **PostgreSQL**: Database for n8n and application data (port 5432)

### Docker Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart n8n
```

## 🔐 Security Considerations

1. **Environment Variables**: Never commit actual API keys
2. **Webhook Signatures**: Always verify Stripe webhook signatures
3. **HTTPS**: Use HTTPS in production for webhook endpoints
4. **API Rate Limiting**: Implement rate limiting for public endpoints
5. **Input Validation**: Validate all incoming data
6. **Authentication**: Implement proper user authentication

## 🚀 Production Deployment

### Recommended Production Setup

1. **Use Production Stripe Keys**
2. **Configure Proper Database** (PostgreSQL recommended)
3. **Set up HTTPS/SSL**
4. **Use Production WSGI Server** (Gunicorn)
5. **Implement Monitoring** (Sentry, DataDog)
6. **Set up Load Balancing**
7. **Configure Backup Strategy**

### Production Deployment Commands
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app

# With environment variables
export FLASK_ENV=production
export STRIPE_SECRET_KEY=sk_live_...
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app
```

## 📊 Monitoring & Logging

The system includes comprehensive logging:
- Flask request/response logging
- Stripe webhook event logging
- n8n workflow execution logging
- Error tracking and reporting

### Log Levels
- `INFO`: General operation information
- `WARNING`: Non-critical issues
- `ERROR`: Error conditions
- `DEBUG`: Detailed debugging information

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add new feature"`
5. Push to branch: `git push origin feature/new-feature`
6. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in each service directory
- Review the API endpoint documentation

## 🔄 Version History

- **v2.0.0**: Full n8n integration, enhanced Stripe features
- **v1.0.0**: Basic Flask backend with simple Stripe integration

---

**PLAYALTER** - Transforming digital experiences with AI-powered face swap and AR technology.
