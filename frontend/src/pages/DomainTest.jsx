import React, { useState, useEffect } from 'react';
import httpService from '../services/http';

const DomainTest = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [apiConfig, setApiConfig] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load API configuration
    import('../config/api.js').then(module => {
      setApiConfig(module.API_CONFIG);
    });
  }, []);

  const testHealthEndpoint = async () => {
    setLoading(true);
    try {
      const result = await httpService.healthCheck();
      setHealthStatus(result);
    } catch (error) {
      setHealthStatus({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  const testUserFeedback = async () => {
    setLoading(true);
    try {
      const result = await httpService.submitUserFeedback({
        user_id: 'test_user_domain',
        feedback: 'Testing domain configuration!',
        test_type: 'domain_test',
        rating: 5
      });
      alert(`Feedback submitted! ID: ${result.feedback_id}`);
    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">🌐 PLAYALTER Domain Configuration Test</h1>
      
      {/* Current Configuration */}
      <div className="bg-blue-50 p-4 rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-3">📡 Current API Configuration</h2>
        {apiConfig && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <strong>Environment:</strong> {import.meta.env.MODE}
            </div>
            <div>
              <strong>Frontend URL:</strong> {apiConfig.BASE_URL}
            </div>
            <div>
              <strong>API URL:</strong> {apiConfig.API_URL}
            </div>
            <div>
              <strong>Domain:</strong> {import.meta.env.VITE_DOMAIN || 'localhost'}
            </div>
          </div>
        )}
      </div>

      {/* Health Check */}
      <div className="bg-white border rounded-lg p-4 mb-6">
        <h2 className="text-xl font-semibold mb-3">🏥 Health Check</h2>
        <button
          onClick={testHealthEndpoint}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Test Health Endpoint'}
        </button>
        
        {healthStatus && (
          <div className="mt-4 p-3 bg-gray-100 rounded">
            <pre className="text-sm overflow-auto">
              {JSON.stringify(healthStatus, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* API Test */}
      <div className="bg-white border rounded-lg p-4 mb-6">
        <h2 className="text-xl font-semibold mb-3">🧪 API Test</h2>
        <button
          onClick={testUserFeedback}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Test User Feedback API'}
        </button>
      </div>

      {/* Domain Information */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-3">🌐 Domain Information</h2>
        <div className="space-y-2 text-sm">
          <div><strong>Production Domain:</strong> www.playalter.com</div>
          <div><strong>Development:</strong> localhost:5173</div>
          <div><strong>Current URL:</strong> {window.location.href}</div>
          <div><strong>User Agent:</strong> {navigator.userAgent}</div>
        </div>
      </div>
    </div>
  );
};

export default DomainTest;
