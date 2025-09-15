/**
 * HTTP Service for PLAYALTER API calls
 * Centralized API communication with error handling
 */

import { API_CONFIG, API_ENDPOINTS, getApiUrl, API_HEADERS, REQUEST_CONFIG } from '../config/api.js';

class HttpService {
  constructor() {
    this.baseURL = API_CONFIG.API_URL;
    this.headers = API_HEADERS;
    this.timeout = REQUEST_CONFIG.timeout;
  }

  /**
   * Generic request method
   */
  async request(endpoint, options = {}) {
    const url = getApiUrl(endpoint);
    
    const config = {
      method: 'GET',
      headers: this.headers,
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      
      return await response.text();
    } catch (error) {
      console.error(`API Request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullEndpoint = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    return this.request(fullEndpoint, {
      method: 'GET',
    });
  }

  /**
   * POST request
   */
  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * PUT request
   */
  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * DELETE request
   */
  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  // Specific API methods for PLAYALTER

  /**
   * Health check
   */
  async healthCheck() {
    return this.get(API_ENDPOINTS.HEALTH);
  }

  /**
   * User feedback submission
   */
  async submitUserFeedback(feedbackData) {
    return this.post(API_ENDPOINTS.USER_TEST, feedbackData);
  }

  /**
   * Face swap operation
   */
  async faceSwap(swapData) {
    return this.post(API_ENDPOINTS.FACE_SWAP, swapData);
  }

  /**
   * AR mask operation
   */
  async arMask(maskData) {
    return this.post(API_ENDPOINTS.AR_MASK, maskData);
  }

  /**
   * AI agents operations
   */
  async getAiAgents() {
    return this.get(API_ENDPOINTS.AI_AGENTS);
  }

  async executeAiAgent(agentData) {
    return this.post(API_ENDPOINTS.AI_AGENTS, agentData);
  }

  /**
   * Live streaming operations
   */
  async getLiveStreamToken(streamData) {
    return this.post(API_ENDPOINTS.LIVE_STREAM, streamData);
  }

  /**
   * Stripe payment operations
   */
  async createCheckoutSession(paymentData) {
    return this.post(API_ENDPOINTS.CREATE_CHECKOUT_SESSION, paymentData);
  }

  async createCustomer(customerData) {
    return this.post(API_ENDPOINTS.CUSTOMERS, customerData);
  }

  /**
   * Face ethics check
   */
  async checkFaceEthics(imageData) {
    return this.post(API_ENDPOINTS.FACE_ETHICS, imageData);
  }

  /**
   * Deployment operations
   */
  async triggerDeploy(deployData) {
    return this.post(API_ENDPOINTS.DEPLOY, deployData);
  }
}

// Create and export singleton instance
const httpService = new HttpService();

export default httpService;

// Named exports for specific methods
export const {
  healthCheck,
  submitUserFeedback,
  faceSwap,
  arMask,
  getAiAgents,
  executeAiAgent,
  getLiveStreamToken,
  createCheckoutSession,
  createCustomer,
  checkFaceEthics,
  triggerDeploy,
} = httpService;
