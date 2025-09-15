/**
 * API Configuration for PLAYALTER
 * Handles environment-based API URL configuration
 */

// Determine if we're in development or production
const isDevelopment = import.meta.env.MODE === 'development';

// API Base URLs
export const API_CONFIG = {
  // Production API (www.playalter.com)
  PRODUCTION_API_URL: 'https://www.playalter.com/api',
  PRODUCTION_BASE_URL: 'https://www.playalter.com',
  
  // Development API (localhost)
  DEVELOPMENT_API_URL: 'http://localhost:5000',
  DEVELOPMENT_BASE_URL: 'http://localhost:5173',
  
  // Current environment URLs
  BASE_URL: isDevelopment 
    ? import.meta.env.VITE_DEV_FRONTEND_URL || 'http://localhost:5173'
    : import.meta.env.VITE_FRONTEND_URL || 'https://www.playalter.com',
    
  API_URL: isDevelopment 
    ? import.meta.env.VITE_DEV_API_BASE_URL || 'http://localhost:5000'
    : import.meta.env.VITE_API_BASE_URL || 'https://www.playalter.com/api',
};

// API Endpoints
export const API_ENDPOINTS = {
  // Health & Status
  HEALTH: '/health',
  
  // User Management
  USER_TEST: '/user-test',
  
  // AI Features
  FACE_SWAP: '/face-swap',
  AR_MASK: '/ar-mask',
  AI_AGENTS: '/ai-agents',
  FACE_ETHICS: '/face-ethics',
  
  // Live Streaming
  LIVE_STREAM: '/live-stream',
  
  // Payment & Stripe
  CREATE_CHECKOUT_SESSION: '/create-checkout-session',
  STRIPE_WEBHOOK: '/stripe-webhook',
  CUSTOMERS: '/customers',
  PRODUCTS: '/products',
  
  // n8n Integration
  N8N_WORKFLOWS: '/n8n/workflows',
  N8N_TRIGGER: '/n8n/trigger',
  
  // Deployment
  DEPLOY: '/deploy',
};

// Full API URLs
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.API_URL}${endpoint}`;
};

// Headers for API requests
export const API_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

// Request configuration
export const REQUEST_CONFIG = {
  timeout: 30000, // 30 seconds
  withCredentials: true, // Include cookies for CORS
};

export default {
  API_CONFIG,
  API_ENDPOINTS,
  getApiUrl,
  API_HEADERS,
  REQUEST_CONFIG,
};
