import React from 'react';
import { CheckCircle, Download, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const PaymentSuccess = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const sessionId = urlParams.get('session_id');

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Payment Successful!
          </h1>
          <p className="text-gray-600">
            Thank you for your subscription. Your account has been upgraded and you can now enjoy all the premium features.
          </p>
        </div>

        {sessionId && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">Session ID:</p>
            <p className="text-xs font-mono text-gray-800 break-all">{sessionId}</p>
          </div>
        )}

        <div className="space-y-4">
          <Link
            to="/dashboard"
            className="block w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Dashboard
          </Link>
          
          <div className="flex items-center justify-center space-x-4 text-sm">
            <button className="flex items-center text-gray-600 hover:text-gray-800">
              <Download className="w-4 h-4 mr-1" />
              Download Receipt
            </button>
            <Link to="/" className="flex items-center text-gray-600 hover:text-gray-800">
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Home
            </Link>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Need help? <a href="/contact" className="text-blue-600 hover:text-blue-700">Contact Support</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default PaymentSuccess;
