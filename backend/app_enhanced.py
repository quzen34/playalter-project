import os
import logging
import stripe
import requests
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
N8N_HOST = os.getenv("N8N_HOST", "http://localhost:5678")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

app.secret_key = FLASK_SECRET_KEY

# Stripe Price Configuration
DEFAULT_PRICE_ID = "price_1S7FP0C41pFAbJdXQMMjixCz"  # New Stripe price ID
STRIPE_DEFAULT_PRICE = os.getenv("STRIPE_DEFAULT_PRICE", DEFAULT_PRICE_ID)

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY or "sk_test_placeholder"
if STRIPE_SECRET_KEY and not STRIPE_SECRET_KEY.startswith("sk_"):
    logger.warning("Invalid Stripe API key format in .env")
else:
    logger.info("Stripe API key configured")
    logger.info(f"Default Stripe Price ID: {STRIPE_DEFAULT_PRICE}")

class N8NService:
    """Service class for n8n integration"""
    
    def __init__(self, host, api_key=None):
        self.host = host
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-N8N-API-KEY': api_key
        } if api_key else {'Content-Type': 'application/json'}
    
    def trigger_workflow(self, workflow_name, data):
        """Trigger an n8n workflow"""
        try:
            webhook_url = f"{self.host}/webhook/{workflow_name}"
            response = requests.post(webhook_url, json=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            logger.info(f"n8n workflow '{workflow_name}' triggered successfully")
            return response.json() if response.content else {"status": "triggered"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to trigger n8n workflow '{workflow_name}': {str(e)}")
            return {"error": str(e)}
    
    def get_workflows(self):
        """Get list of available workflows"""
        try:
            response = requests.get(f"{self.host}/api/v1/workflows", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch n8n workflows: {str(e)}")
            return {"error": str(e)}
    
    def execute_workflow(self, workflow_id, data):
        """Execute a specific workflow by ID"""
        try:
            response = requests.post(
                f"{self.host}/api/v1/workflows/{workflow_id}/execute",
                json=data,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            logger.info(f"n8n workflow {workflow_id} executed successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to execute n8n workflow {workflow_id}: {str(e)}")
            return {"error": str(e)}

# Initialize n8n service
n8n_service = N8NService(N8N_HOST, N8N_API_KEY)

class StripeService:
    """Enhanced Stripe service with comprehensive functionality"""
    
    @staticmethod
    def create_customer(email, name=None, metadata=None):
        """Create a new Stripe customer"""
        try:
            customer_data = {"email": email}
            if name:
                customer_data["name"] = name
            if metadata:
                customer_data["metadata"] = metadata
            
            customer = stripe.Customer.create(**customer_data)
            logger.info(f"Stripe customer created: {customer.id}")
            return customer
        except stripe.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {str(e)}")
            raise
    
    @staticmethod
    def create_product(name, description=None, metadata=None):
        """Create a new Stripe product"""
        try:
            product_data = {"name": name}
            if description:
                product_data["description"] = description
            if metadata:
                product_data["metadata"] = metadata
            
            product = stripe.Product.create(**product_data)
            logger.info(f"Stripe product created: {product.id}")
            return product
        except stripe.StripeError as e:
            logger.error(f"Failed to create Stripe product: {str(e)}")
            raise
    
    @staticmethod
    def create_price(product_id, unit_amount, currency="usd", recurring=None):
        """Create a new Stripe price"""
        try:
            price_data = {
                "product": product_id,
                "unit_amount": unit_amount,
                "currency": currency
            }
            if recurring:
                price_data["recurring"] = recurring
            
            price = stripe.Price.create(**price_data)
            logger.info(f"Stripe price created: {price.id}")
            return price
        except stripe.StripeError as e:
            logger.error(f"Failed to create Stripe price: {str(e)}")
            raise
    
    @staticmethod
    def get_customer_subscriptions(customer_id):
        """Get all subscriptions for a customer"""
        try:
            subscriptions = stripe.Subscription.list(customer=customer_id)
            return subscriptions
        except stripe.StripeError as e:
            logger.error(f"Failed to fetch subscriptions for customer {customer_id}: {str(e)}")
            raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    n8n_status = "connected" if n8n_service.get_workflows().get("error") is None else "disconnected"
    
    return jsonify({
        "status": "healthy",
        "service": "PLAYALTER Backend",
        "version": "2.0.0",
        "integrations": {
            "stripe": "connected" if STRIPE_SECRET_KEY else "not_configured",
            "n8n": n8n_status,
            "openai": "configured" if OPENAI_API_KEY else "not_configured"
        },
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/api/orchestrate', methods=['POST'])
def orchestrate():
    """Enhanced orchestration with n8n integration"""
    try:
        data = request.get_json(silent=True) or {}
        operation_type = data.get('operation', 'general')
        user_request = data.get('request', '')
        user_id = data.get('user_id')
        
        logger.info(f"Orchestration request: {operation_type} - {user_request}")
        
        # Prepare data for n8n workflow
        workflow_data = {
            "operation": operation_type,
            "request": user_request,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "playalter_backend"
        }
        
        # Trigger appropriate n8n workflow based on operation type
        workflow_mapping = {
            "swap": "face-swap-workflow",
            "mask": "ar-mask-workflow", 
            "stream": "live-stream-workflow",
            "payment": "payment-processing-workflow",
            "general": "general-ai-workflow"
        }
        
        workflow_name = workflow_mapping.get(operation_type, "general-ai-workflow")
        n8n_result = n8n_service.trigger_workflow(workflow_name, workflow_data)
        
        response_data = {
            "status": "success",
            "operation": operation_type,
            "message": f"Orchestration completed for {operation_type} operation",
            "n8n_response": n8n_result,
            "workflow_triggered": workflow_name,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Orchestration error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a new Stripe customer"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        metadata = data.get('metadata', {})
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        customer = StripeService.create_customer(email, name, metadata)
        
        # Trigger n8n workflow for new customer
        n8n_service.trigger_workflow("new-customer-workflow", {
            "customer_id": customer.id,
            "email": email,
            "name": name,
            "created_at": datetime.utcnow().isoformat()
        })
        
        return jsonify({
            "status": "success",
            "customer": {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name
            }
        }), 201
        
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new Stripe product"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        metadata = data.get('metadata', {})
        
        if not name:
            return jsonify({"error": "Product name is required"}), 400
        
        product = StripeService.create_product(name, description, metadata)
        
        return jsonify({
            "status": "success",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description
            }
        }), 201
        
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Enhanced checkout session creation"""
    try:
        data = request.get_json()
        price_id = data.get('priceId', STRIPE_DEFAULT_PRICE)  # Use default if not provided
        customer_email = data.get('email')
        success_url = data.get('success_url', 'http://localhost:5173/payment-success')
        cancel_url = data.get('cancel_url', 'http://localhost:5173/payment-cancel')
        mode = data.get('mode', 'subscription')
        
        logger.info(f"Creating checkout session with price ID: {price_id}")
        
        if not price_id:
            return jsonify({"error": "Price ID is required"}), 400
        
        session_data = {
            "payment_method_types": ['card'],
            "line_items": [{
                'price': price_id,
                'quantity': 1,
            }],
            "mode": mode,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
        
        # Add customer email if provided
        if customer_email:
            session_data["customer_email"] = customer_email
        
        # Add subscription-specific options
        if mode == 'subscription':
            session_data["line_items"][0]["adjustable_quantity"] = {"enabled": True}
        
        session = stripe.checkout.Session.create(**session_data)
        
        # Trigger n8n workflow for checkout session creation
        n8n_service.trigger_workflow("checkout-session-created", {
            "session_id": session.id,
            "price_id": price_id,
            "customer_email": customer_email,
            "mode": mode,
            "created_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Checkout session created: {session.id}")
        
        return jsonify({
            "status": "success",
            "clientSecret": session.client_secret,
            "sessionId": session.id,
            "url": session.url
        }), 200

    except stripe.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/subscriptions/<customer_id>', methods=['GET'])
def get_customer_subscriptions(customer_id):
    """Get customer subscriptions"""
    try:
        subscriptions = StripeService.get_customer_subscriptions(customer_id)
        
        return jsonify({
            "status": "success",
            "subscriptions": [{
                "id": sub.id,
                "status": sub.status,
                "current_period_start": sub.current_period_start,
                "current_period_end": sub.current_period_end,
                "price_id": sub.items.data[0].price.id if sub.items.data else None
            } for sub in subscriptions.data]
        }), 200
        
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error fetching subscriptions: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Enhanced Stripe webhook with n8n integration"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            event = stripe.Event.construct_from(request.get_json(), stripe.api_key)

        logger.info(f"Stripe webhook received: {event.type}")

        # Enhanced event handling with n8n integration
        event_data = {
            "event_type": event.type,
            "event_id": event.id,
            "data": event.data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Trigger n8n workflow for each event type
        workflow_triggered = False
        
        if event.type == 'payment_intent.succeeded':
            logger.info("Payment intent succeeded")
            n8n_service.trigger_workflow("payment-succeeded", event_data)
            workflow_triggered = True
            
        elif event.type == 'payment_intent.payment_failed':
            logger.info("Payment intent failed")
            n8n_service.trigger_workflow("payment-failed", event_data)
            workflow_triggered = True
            
        elif event.type == 'checkout.session.completed':
            logger.info("Checkout session completed")
            n8n_service.trigger_workflow("checkout-completed", event_data)
            workflow_triggered = True
            
        elif event.type == 'customer.subscription.created':
            logger.info("Subscription created")
            n8n_service.trigger_workflow("subscription-created", event_data)
            workflow_triggered = True
            
        elif event.type == 'customer.subscription.updated':
            logger.info("Subscription updated")
            n8n_service.trigger_workflow("subscription-updated", event_data)
            workflow_triggered = True
            
        elif event.type == 'customer.subscription.deleted':
            logger.info("Subscription deleted")
            n8n_service.trigger_workflow("subscription-deleted", event_data)
            workflow_triggered = True
            
        elif event.type == 'invoice.payment_succeeded':
            logger.info("Invoice payment succeeded")
            n8n_service.trigger_workflow("invoice-paid", event_data)
            workflow_triggered = True
            
        elif event.type == 'invoice.payment_failed':
            logger.info("Invoice payment failed")
            n8n_service.trigger_workflow("invoice-failed", event_data)
            workflow_triggered = True
        else:
            logger.info(f"Unhandled event type: {event.type}")
            # Trigger generic webhook workflow for unhandled events
            n8n_service.trigger_workflow("stripe-webhook-generic", event_data)
            workflow_triggered = True

        return jsonify({
            'status': 'success',
            'event_type': event.type,
            'n8n_triggered': workflow_triggered,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/n8n/workflows', methods=['GET'])
def get_n8n_workflows():
    """Get available n8n workflows"""
    try:
        workflows = n8n_service.get_workflows()
        return jsonify({
            "status": "success",
            "workflows": workflows
        }), 200
    except Exception as e:
        logger.error(f"Error fetching n8n workflows: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/n8n/trigger/<workflow_name>', methods=['POST'])
def trigger_n8n_workflow(workflow_name):
    """Manually trigger an n8n workflow"""
    try:
        data = request.get_json() or {}
        result = n8n_service.trigger_workflow(workflow_name, data)
        
        return jsonify({
            "status": "success",
            "workflow": workflow_name,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error triggering n8n workflow {workflow_name}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/face-swap', methods=['POST'])
def face_swap():
    """Face swap operation with n8n workflow"""
    try:
        data = request.get_json()
        source_image = data.get('source_image')
        target_image = data.get('target_image')
        user_id = data.get('user_id')
        
        if not source_image or not target_image:
            return jsonify({"error": "Both source_image and target_image are required"}), 400
        
        # Trigger face swap workflow in n8n
        workflow_data = {
            "source_image": source_image,
            "target_image": target_image,
            "user_id": user_id,
            "operation": "face_swap",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = n8n_service.trigger_workflow("face-swap-processing", workflow_data)
        
        return jsonify({
            "status": "success",
            "message": "Face swap processing initiated",
            "workflow_result": result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Face swap error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ar-mask', methods=['POST'])
def ar_mask():
    """AR mask operation with n8n workflow"""
    try:
        data = request.get_json()
        image = data.get('image')
        mask_type = data.get('mask_type')
        user_id = data.get('user_id')
        
        if not image or not mask_type:
            return jsonify({"error": "Both image and mask_type are required"}), 400
        
        # Trigger AR mask workflow in n8n
        workflow_data = {
            "image": image,
            "mask_type": mask_type,
            "user_id": user_id,
            "operation": "ar_mask",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = n8n_service.trigger_workflow("ar-mask-processing", workflow_data)
        
        return jsonify({
            "status": "success",
            "message": "AR mask processing initiated",
            "workflow_result": result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"AR mask error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """API home with comprehensive endpoint documentation"""
    return jsonify({
        "service": "PLAYALTER Backend API",
        "version": "2.0.0",
        "description": "AI Face Swap & AR Web App with n8n Workflows and Stripe Integration",
        "endpoints": {
            "health": "GET /health - Service health check",
            "orchestration": "POST /api/orchestrate - Trigger AI workflow orchestration",
            "stripe": {
                "customers": "POST /api/customers - Create Stripe customer",
                "products": "POST /api/products - Create Stripe product", 
                "checkout": "POST /api/create-checkout-session - Create checkout session",
                "subscriptions": "GET /api/subscriptions/<customer_id> - Get customer subscriptions",
                "webhook": "POST /api/stripe-webhook - Stripe webhook endpoint"
            },
            "n8n": {
                "workflows": "GET /api/n8n/workflows - List available workflows",
                "trigger": "POST /api/n8n/trigger/<workflow_name> - Trigger specific workflow"
            },
            "ai_services": {
                "face_swap": "POST /api/face-swap - Process face swap",
                "ar_mask": "POST /api/ar-mask - Apply AR mask"
            }
        },
        "integrations": ["Stripe", "n8n", "OpenAI"],
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    logger.info("Starting PLAYALTER Backend with n8n and Stripe integration")
    app.run(debug=True, host='0.0.0.0', port=5000)
