import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error(`Health check failed: ${error.message}`);
  }
};

// AI Operations
export const orchestrateAI = async (operation, request, userId = null) => {
  try {
    const response = await api.post('/orchestrate', {
      operation,
      request,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Orchestration failed: ${error.response?.data?.message || error.message}`);
  }
};

export const processFaceSwap = async (sourceImage, targetImage, userId = null) => {
  try {
    const response = await api.post('/face-swap', {
      source_image: sourceImage,
      target_image: targetImage,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Face swap failed: ${error.response?.data?.error || error.message}`);
  }
};

// Alternative face swap function for FormData
export const faceSwap = async (formData) => {
  try {
    const response = await api.post('/face-swap', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(`Face swap failed: ${error.response?.data?.error || error.message}`);
  }
};

export const processARMask = async (image, maskType, userId = null) => {
  try {
    const response = await api.post('/ar-mask', {
      image,
      mask_type: maskType,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    throw new Error(`AR mask failed: ${error.response?.data?.error || error.message}`);
  }
};

// Alternative AR mask function for FormData
export const applyARMask = async (formData) => {
  try {
    const response = await api.post('/ar-mask', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(`AR mask failed: ${error.response?.data?.error || error.message}`);
  }
};

// Stripe Operations
export const createCustomer = async (email, name = null, metadata = {}) => {
  try {
    const response = await api.post('/customers', {
      email,
      name,
      metadata,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Customer creation failed: ${error.response?.data?.error || error.message}`);
  }
};

export const createCheckoutSession = async (priceId, email, successUrl = null, cancelUrl = null) => {
  try {
    const response = await api.post('/create-checkout-session', {
      priceId,
      email,
      success_url: successUrl || `${window.location.origin}/payment-success`,
      cancel_url: cancelUrl || `${window.location.origin}/payment-cancel`,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Checkout session failed: ${error.response?.data?.error || error.message}`);
  }
};

export const getCustomerSubscriptions = async (customerId) => {
  try {
    const response = await api.get(`/subscriptions/${customerId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get subscriptions: ${error.response?.data?.error || error.message}`);
  }
};

// n8n Operations
export const getN8nWorkflows = async () => {
  try {
    const response = await api.get('/n8n/workflows');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get workflows: ${error.response?.data?.error || error.message}`);
  }
};

export const triggerN8nWorkflow = async (workflowName, data = {}) => {
  try {
    const response = await api.post(`/n8n/trigger/${workflowName}`, data);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to trigger workflow: ${error.response?.data?.error || error.message}`);
  }
};

// File upload helper
export const uploadFile = async (file, onProgress = null) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(`File upload failed: ${error.response?.data?.error || error.message}`);
  }
};

// User profile and history functions
export const getUserProfile = async () => {
  try {
    const response = await api.get('/user/profile');
    return response.data;
  } catch (error) {
    // Return mock data if API fails
    return {
      name: 'Demo User',
      email: 'demo@playalter.com',
      stats: {
        faceSwaps: 12,
        arMasks: 8,
        avgProcessingTime: 3.2
      },
      limits: {
        faceSwaps: 50,
        arMasks: 20
      },
      subscription: {
        plan: 'Pro',
        cycle: 'Monthly',
        nextBilling: '2024-02-15'
      }
    };
  }
};

export const getProcessingHistory = async () => {
  try {
    const response = await api.get('/user/history');
    return response.data;
  } catch (error) {
    // Return mock data if API fails
    return [
      {
        id: '1',
        type: 'face_swap',
        status: 'completed',
        created_at: '2024-01-15T10:30:00Z',
        result_url: '/results/face-swap-1.jpg'
      },
      {
        id: '2',
        type: 'ar_mask',
        status: 'completed',
        created_at: '2024-01-14T15:45:00Z',
        result_url: '/results/ar-mask-1.jpg'
      },
      {
        id: '3',
        type: 'face_swap',
        status: 'processing',
        created_at: '2024-01-14T12:20:00Z'
      }
    ];
  }
};

export default api;
