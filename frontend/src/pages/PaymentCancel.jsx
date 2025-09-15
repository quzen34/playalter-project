import React from 'react';
import { XCircle, ArrowLeft, HelpCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const PaymentCancel = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <XCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Payment Cancelled
          </h1>
          <p className="text-gray-600">
            Your payment was cancelled. No charges were made to your account.
          </p>
        </div>

        <div className="space-y-4">
          <Link
            to="/pricing"
            className="block w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </Link>
          
          <Link
            to="/"
            className="block w-full border border-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Back to Home
          </Link>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="space-y-3">
            <p className="text-sm text-gray-600">
              <HelpCircle className="w-4 h-4 inline mr-1" />
              Having trouble with payment?
            </p>
            <div className="space-y-2 text-sm">
              <p className="text-gray-500">• Check your card details</p>
              <p className="text-gray-500">• Ensure sufficient funds</p>
              <p className="text-gray-500">• Try a different payment method</p>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Still need help? <a href="/contact" className="text-blue-600 hover:text-blue-700">Contact Support</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentCancel;
