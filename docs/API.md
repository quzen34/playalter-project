# PLAYALTER API Documentation

## Overview

The PLAYALTER API provides orchestra-level integration across 6 core platforms: N8N, Stripe, Vercel, OpenAI, Replicate, and Agora. This RESTful API enables seamless coordination of AI-powered content creation workflows.

## Base URL

```
Development: http://localhost:8000
Production: https://api.playalter.com
```

## Authentication

All API requests require authentication using API keys or JWT tokens.

### API Key Authentication

```http
Authorization: Bearer your-api-key-here
```

### JWT Authentication

```http
Authorization: Bearer your-jwt-token-here
```

## Core Endpoints

### Health Check

Check the overall system health and platform status.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-16T10:30:00Z",
  "platforms": {
    "n8n": "healthy",
    "stripe": "healthy", 
    "vercel": "healthy",
    "openai": "healthy",
    "replicate": "healthy",
    "agora": "healthy"
  },
  "response_time": "12ms"
}
```

### Platform Status

Get detailed status information for all integrated platforms.

```http
GET /api/platforms/status
```

**Response:**
```json
{
  "platforms": [
    {
      "name": "n8n",
      "status": "healthy",
      "response_time": 8,
      "last_check": "2025-09-16T10:29:00Z",
      "endpoints": 3,
      "workflows_active": 12
    }
  ]
}
```

## Workflow Orchestration

### Face Swap Payment Workflow

Execute a complete face swap workflow with payment processing.

```http
POST /api/workflows/face-swap-payment
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "user_123",
  "source_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "target_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...", 
  "payment_method": "pm_1234567890",
  "quality": "high",
  "options": {
    "preserve_expression": true,
    "enhance_quality": true
  }
}
```

**Response:**
```json
{
  "workflow_id": "wf_face_swap_001",
  "status": "completed",
  "steps": [
    {
      "step": "payment_processing",
      "platform": "stripe",
      "status": "success",
      "duration": "1.2s"
    },
    {
      "step": "face_swap",
      "platform": "replicate", 
      "status": "success",
      "duration": "8.5s"
    }
  ],
  "result": {
    "processed_image": "https://cdn.playalter.com/results/abc123.jpg",
    "thumbnail": "https://cdn.playalter.com/thumbs/abc123.jpg"
  },
  "total_duration": "10.2s"
}
```

### User Onboarding Workflow

Complete user registration and setup workflow.

```http
POST /api/workflows/user-onboarding
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "subscription_plan": "premium",
  "payment_method": "pm_1234567890",
  "profile": {
    "name": "John Doe",
    "preferences": {
      "notifications": true,
      "quality": "high"
    }
  }
}
```

**Response:**
```json
{
  "workflow_id": "wf_onboarding_001",
  "user_id": "user_456",
  "status": "completed",
  "steps": [
    {
      "step": "user_registration",
      "status": "success"
    },
    {
      "step": "stripe_subscription",
      "status": "success",
      "subscription_id": "sub_1234567890"
    },
    {
      "step": "welcome_message",
      "platform": "openai",
      "status": "success"
    }
  ],
  "profile_url": "https://app.playalter.com/user/user_456"
}
```

### Live Stream Setup

Prepare and configure live streaming session.

```http
POST /api/workflows/live-stream-setup
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "user_123",
  "stream_config": {
    "title": "Live AR Stream",
    "description": "Real-time face swap demonstration",
    "effects": ["face_swap", "background_blur"],
    "quality": "1080p",
    "privacy": "public"
  },
  "ar_settings": {
    "face_detection": true,
    "real_time_swap": true,
    "enhancement": true
  }
}
```

**Response:**
```json
{
  "workflow_id": "wf_stream_001",
  "stream_id": "stream_789",
  "status": "ready",
  "agora_config": {
    "app_id": "your_agora_app_id",
    "channel": "stream_789",
    "token": "agora_rtc_token_here",
    "uid": 12345
  },
  "stream_url": "https://live.playalter.com/stream_789",
  "rtmp_url": "rtmp://live.playalter.com/stream_789"
}
```

## Platform-Specific APIs

### N8N Integration

#### List Workflows

```http
GET /api/n8n/workflows
```

#### Execute Workflow

```http
POST /api/n8n/workflows/{workflow_id}/execute
Content-Type: application/json
```

### Stripe Integration

#### Create Payment Intent

```http
POST /api/stripe/payment-intents
Content-Type: application/json
```

#### Manage Subscriptions

```http
GET /api/stripe/subscriptions/{user_id}
POST /api/stripe/subscriptions
PUT /api/stripe/subscriptions/{subscription_id}
DELETE /api/stripe/subscriptions/{subscription_id}
```

### OpenAI Integration

#### Generate Content

```http
POST /api/openai/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "Create a welcome message for a new user",
  "model": "gpt-4",
  "parameters": {
    "max_tokens": 150,
    "temperature": 0.7
  }
}
```

### Replicate Integration

#### Face Swap

```http
POST /api/replicate/face-swap
Content-Type: application/json
```

#### Model Status

```http
GET /api/replicate/predictions/{prediction_id}
```

### Agora Integration

#### Generate Token

```http
POST /api/agora/token
Content-Type: application/json
```

#### Channel Management

```http
GET /api/agora/channels
POST /api/agora/channels
DELETE /api/agora/channels/{channel_id}
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request parameters are invalid",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    },
    "request_id": "req_123456789",
    "timestamp": "2025-09-16T10:30:00Z"
  }
}
```

### Common Error Codes

- `INVALID_REQUEST` (400): Request parameters are invalid
- `UNAUTHORIZED` (401): Authentication required or invalid
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `RATE_LIMITED` (429): Rate limit exceeded
- `INTERNAL_ERROR` (500): Server error
- `SERVICE_UNAVAILABLE` (503): External service unavailable

## Rate Limiting

API requests are rate-limited to ensure fair usage:

- **Free Tier**: 100 requests per hour
- **Premium Tier**: 1,000 requests per hour  
- **Enterprise Tier**: 10,000 requests per hour

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1641024000
```

## Webhooks

PLAYALTER supports webhooks for real-time notifications.

### Webhook Events

- `workflow.completed` - Workflow execution completed
- `payment.succeeded` - Payment processed successfully
- `user.created` - New user registered
- `stream.started` - Live stream began
- `ai.processing.completed` - AI processing finished

### Webhook Payload

```json
{
  "id": "evt_1234567890",
  "type": "workflow.completed",
  "data": {
    "workflow_id": "wf_001",
    "status": "success",
    "user_id": "user_123"
  },
  "timestamp": "2025-09-16T10:30:00Z"
}
```

### Webhook Security

All webhooks are signed with HMAC-SHA256. Verify signatures using:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## SDK Examples

### Python SDK

```python
from playalter import PlayalterClient

client = PlayalterClient(api_key="your-api-key")

# Face swap workflow
result = client.workflows.face_swap_payment(
    user_id="user_123",
    source_image=source_image_data,
    target_image=target_image_data,
    payment_method="pm_1234567890"
)

print(f"Workflow completed: {result.workflow_id}")
```

### JavaScript SDK

```javascript
import { PlayalterClient } from '@playalter/sdk';

const client = new PlayalterClient({
  apiKey: 'your-api-key'
});

// Live stream setup
const stream = await client.workflows.liveStreamSetup({
  userId: 'user_123',
  streamConfig: {
    title: 'My Live Stream',
    effects: ['face_swap']
  }
});

console.log(`Stream ready: ${stream.streamUrl}`);
```

## Testing

### Test Environment

```
Base URL: https://api-test.playalter.com
```

### Test API Keys

Use test API keys for development:

```
Test Key: pk_test_1234567890abcdef
```

### Mock Responses

Test endpoints return mock data for development purposes.

## Support

- **Documentation**: https://docs.playalter.com
- **Status Page**: https://status.playalter.com
- **Support**: support@playalter.com
- **GitHub**: https://github.com/quzen34/playalter-project
