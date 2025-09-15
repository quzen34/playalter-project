# PLAYALTER Backend

Flask backend for PLAYALTER AI Face Swap & AR Web App with n8n Workflows.

## Features

- **AI Orchestration**: CrewAI-powered agent coordination for face swap, AR masks, and live streaming
- **Payment Processing**: Stripe integration for subscription management
- **Webhook Handling**: Automated payment event processing
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Health Monitoring**: Built-in health check endpoints

## API Endpoints

- `GET /` - Service information and endpoint list
- `GET /health` - Health check
- `POST /api/orchestrate` - Trigger AI crew orchestration
- `POST /api/create-checkout-session` - Create Stripe checkout session
- `POST /api/stripe-webhook` - Stripe webhook endpoint

## Setup

### Prerequisites

- Python 3.8+
- pip or pipenv

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment configuration**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your actual API keys:
   - OpenAI API key for AI agents
   - Stripe keys for payment processing
   - Webhook secret for Stripe events

3. **Run the server**:
   ```bash
   python app.py
   ```
   
   Server will start on `http://localhost:5000`

### API Usage Examples

#### Orchestrate AI Workflow
```bash
curl -X POST http://localhost:5000/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "swap",
    "request": "Apply face swap with provided images"
  }'
```

#### Create Stripe Checkout Session
```bash
curl -X POST http://localhost:5000/api/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{
    "priceId": "price_1S7FP0C41pFAbJdXQMMjixCz",
    "email": "user@example.com"
  }'
```

## Development

- **Debug mode**: Enabled by default in development
- **Hot reload**: Flask automatically reloads on code changes
- **Logging**: INFO level logging for debugging and monitoring

## Production Deployment

For production deployment, consider:

1. **Use Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set environment variables** properly
3. **Configure reverse proxy** (nginx/Apache)
4. **Enable HTTPS** for webhook endpoints
5. **Set up monitoring** and error tracking

## Architecture

- **CrewAI Agents**: Specialized AI agents for different operations
- **Flask Routes**: RESTful API endpoints
- **Stripe Integration**: Secure payment processing
- **Environment Management**: Secure configuration handling
